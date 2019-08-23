from django.contrib.auth.views import LoginView
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views.decorators.http import require_http_methods

from .forms import SignUpForm, PasswordResetForm

class SignIn(LoginView):
    """
    Uses the built-in login view.
    I only change template name.
    """
    template_name = 'account/sign_in.html'
    
def sign_up_end(request):
    return HttpResponse('Your account successfully created')

def main(request):
    return HttpResponse("Main website")
    
@require_http_methods(request_method_list=["GET", "POST"])
def sign_up_view(request):
    """
    This view show fields for sign up (username, nick, email, first name and last name, birth data and password).
    If user will enter the data correctly new user is create and user is redirected to the address 'sign_up/success/'.
    If user will enter the daata incorrectly user recevies information about error.
    """
    if request.method == 'POST':
        form = SignUpForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(to=reverse('authentication:sign_up_end'))
        else:
            return render(
                request=request,
                template_name='account/sign_up.html', 
                context=dict(error_f=form.errors)
            )
    else:        
        form = SignUpForm()
        return render(
            request=request, 
            template_name='account/sign_up.html', 
            context=dict(form=form)
        )


@require_http_methods(request_method_list=["GET", "POST"])
def reset_password_view(request):
    """
    This view show fields for reset password (username, email).
    If user will enter the data correctly user has the password reset and sent to the email address provided.
    If user will enter the daata incorrectly user recevies information about error.
    """
    if request.method == 'POST':
        form = PasswordResetForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(to=reverse('authentication:main'))
        else:
            return render(
                request=request,
                template_name='account/reset_password.html', 
                context=dict(error_f=form.errors)
            )
    else:      
        form = PasswordResetForm()
        return render(
            request=request, 
            template_name='account/reset_password.html', 
            context=dict(form=form)
        )
    


        
