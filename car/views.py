from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.template.loader import render_to_string
from django.views.generic.edit import CreateView, FormView, UpdateView
from django.views.generic import TemplateView, ListView
from .forms import UserRegisterForm, AddCarForm
from django.urls import reverse_lazy
from .task import send_mail


from .models import Car


class SignInView(LoginView):
    template_name = 'login.html'


class SignUpView(SuccessMessageMixin, CreateView):
    template_name = 'register.html'
    success_url = reverse_lazy('login')
    form_class = UserRegisterForm
    success_message = "Your profile was created successfully"


class HomeView(TemplateView):
    template_name = "home.html"


class AddCarView(FormView):
    form_class = AddCarForm
    template_name = 'add_car.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        car_obj = form.save(commit=False)
        car_obj.seller = self.request.user
        car_obj.save()
        return HttpResponseRedirect(self.get_success_url())


class CarListView(ListView):
    template_name = "car_list.html"
    context_object_name = "cars"

    def get_queryset(self):
        queryset = Car.objects.all()
        if self.request.GET:
            make = self.request.GET.get('make')
            year = self.request.GET.get('year')
            clear_filter = self.request.GET.get('clear')
            if make:
                queryset = queryset.filter(make=make)
            if year:
                queryset = queryset.filter(year=year)
            if clear_filter:
                queryset = Car.objects.all()
        return queryset


class CarDetailsView(UpdateView):
    template_name = "car_details.html"
    model = Car
    form_class = AddCarForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        car_obj = form.save(commit=False)
        car_obj.is_sold = True
        car_obj.buyer = self.request.user
        car_obj.save()
        obj = self.get_object()
        message = render_to_string('send_email.html', {
            'obj': obj
        })
        send_mail.delay(message, obj.seller.email)

        return HttpResponseRedirect(self.get_success_url())

