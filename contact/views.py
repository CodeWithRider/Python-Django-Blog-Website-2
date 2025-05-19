from django.shortcuts import render
from django.views import View
from .models import Contact
from django.core.mail import send_mail
from django.conf import settings



# Create your views here.
class ContactUsView(View):
    def get(self, request):
        return render(request, "contact/contact.html")

    def post(self, request):
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        context = {}
        if name and email and message:
            Contact.objects.create(name=name, email=email, subject=subject, message=message)

            send_mail(
                subject=f"New Contact Form Submission: {subject}",
                message=f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=['priyankapal8823@gmail.com', email],
                fail_silently=False,
            )

            context['message'] = f"Dear {name}, thanks for your message!"
        else:
            context['error'] = "All fields are required."

        return render(request, "contact/contact.html", context)