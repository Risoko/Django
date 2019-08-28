from django.http import HttpResponse
from django.urls import reverse_lazy
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.views.generic.edit import FormView 

from .forms import SignUpForm, PasswordResetForm

class SignIn(LoginView):
    http_method_names = ['get', 'post']
    template_name = 'account/sign_in.html'
    success_url = reverse_lazy('authentication:main')

    def get_success_url(self):
        return self.success_url

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            logout(request)
        return super().dispatch(request, *args, **kwargs)

class MyFormView(FormView):
    http_method_names = ['get', 'post']
    success_url = reverse_lazy('authentication:main')

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests: instantiate a form instance with the passed
        POST variables and then check if it's valid and then save data.
        """
        form = self.get_form()
        if form.is_valid():
            form.save()
            return self.form_valid(form=form)
        self.extra_context = dict(error_f=form.errors)
        return self.form_invalid(form)

class SignUpView(MyFormView):
    template_name = 'account/sign_up.html'
    success_url = reverse_lazy('authentication:sign_up_end')
    form_class = SignUpForm

class ResetPasswordView(MyFormView):
    form_class = PasswordResetForm
    template_name = 'account/reset_password.html'
    
def sign_up_end(request):
    return HttpResponse('Your account successfully created')

def main(request):
    return HttpResponse("Main website")
    



        
