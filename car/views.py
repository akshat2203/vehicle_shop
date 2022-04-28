from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.template.loader import render_to_string
from django.views.generic.edit import CreateView, FormView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import UserRegisterForm, AddCarForm
from django.urls import reverse_lazy
from .task import send_mail
from .models import Car
from el_pagination.views import AjaxListView


class SignInView(LoginView):
    template_name = 'login.html'


class SignUpView(SuccessMessageMixin, CreateView):
    template_name = 'register.html'
    success_url = reverse_lazy('login')
    form_class = UserRegisterForm
    success_message = "Your profile was created successfully"


class AddCarView(LoginRequiredMixin, FormView):
    form_class = AddCarForm
    template_name = 'add_car.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        car_obj = form.save(commit=False)
        car_obj.seller = self.request.user
        car_obj.save()
        return HttpResponseRedirect(self.get_success_url())


class CarListView(LoginRequiredMixin, AjaxListView):
    template_name = "car_list.html"
    context_object_name = "entry_list"

    def get_queryset(self):
        queryset = Car.objects.all()
        if self.request.GET:
            make = self.request.GET.get('make')
            year = self.request.GET.get('year')
            car_id = self.request.GET.get('car_id')
            clear_filter = self.request.GET.get('clear')
            if make:
                queryset = queryset.filter(make=make)
            if year:
                queryset = queryset.filter(year=year)
            if clear_filter:
                queryset = Car.objects.all()
            if car_id:
                obj = Car.objects.filter(id=car_id).first()
                obj.is_sold = False
                obj.save()
        return queryset


class CarDetailsView(LoginRequiredMixin, UpdateView):
    template_name = "car_details.html"
    model = Car
    form_class = AddCarForm
    success_url = reverse_lazy('car_list')

    def form_valid(self, form):
        car_obj = form.save(commit=False)
        car_obj.is_sold = True
        car_obj.buyer = self.request.user
        car_obj.save()
        obj = self.get_object()
        message = render_to_string('send_email.html', {'obj': obj})
        send_mail.delay(message, obj.seller.email)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, *args, **kwargs):
        ctx = super(CarDetailsView, self).get_context_data()
        ctx['car_obj'] = self.get_object()
        return ctx
