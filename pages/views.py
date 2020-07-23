from django.views.generic import TemplateView
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import ContactForm

# Create your views here.


class HomePageView(TemplateView):
    template_name = 'home.html'


def contactView(request):
    if request.method == 'GET':
        form = ContactForm()
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            subject = form.cleaned_data['subject']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            try:
                send_mail(subject, message, email, ['admin@codes-hub.com'])
            except BadHeaderError:
                return HttpResponse('Invalid Header')
            return redirect('success')
    return render(request, 'contact_email.html', {'form':form})


class SuccessView(TemplateView):
    template_name = 'contact_success.html'
'''
def successView(request):
    return HttpResponse("Success! Thank you for your message.")
'''


class AboutUsView(TemplateView):
    template_name = 'about_us.html'
