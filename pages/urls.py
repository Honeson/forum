from django.urls import path

from .views import (
    HomePageView,
    contactView,
    SuccessView,
)


urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('contact/', contactView, name='contact'),
    path('success', SuccessView.as_view(), name='success'),
]