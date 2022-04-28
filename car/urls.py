from django.urls import path
from django.contrib.auth import views as auth_views
from .views import SignInView, SignUpView, AddCarView, CarListView, CarDetailsView


urlpatterns = [
    path('login/', SignInView.as_view(), name="login"),
    path('logout/', auth_views.LogoutView.as_view(template_name="home.html"), name='logout'),
    path('register/', SignUpView.as_view(), name="register"),
    path('add/', AddCarView.as_view(), name="add"),
    path('', CarListView.as_view(), name="car_list"),
    path('car/<int:pk>', CarDetailsView.as_view(), name="car_details"),
]
