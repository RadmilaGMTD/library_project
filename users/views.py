from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth import login
from django.core.mail import send_mail
from .forms import CustomUserCreationForm


class RegisterView(CreateView):
    template_name = "users/register.html"
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("library:books_list")

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        self.send_welcome_email()
        return super().form_valid(form)

    def send_welcome_email(self):
        subject = "Добро пожаловать в наш сервис"
        message = "Спасибо, что зарегистрировались в нашем сервисе!"
        from_email = "rmiftyaeva@mail.ru"
        recipient_list = ["raf1507@mail.ru"]
        send_mail(subject, message, from_email, recipient_list)
