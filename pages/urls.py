from django.urls import path

from .views import (
    HomePageView,
    contactView,
    SuccessView,
    AboutUsView,
)


urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('contact/', contactView, name='contact'),
    path('success/', SuccessView.as_view(), name='success'),
    path('about-us/', AboutUsView.as_view(), name='about_us'),
]