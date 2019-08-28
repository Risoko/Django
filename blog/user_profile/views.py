from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import FormView 

from .forms import ChangeEmailForm, ChangePasswordForm

@method_decorator(
    decorator=login_required(login_url=reverse_lazy('authentication:login')),
    name='dispatch'
    )
class MyFormView(FormView):
    http_method_names = ['get', 'post']
    success_url = reverse_lazy('authentication:main')

    def get_form(self, form_class=None):
        """Return an instance of the form to be used in this view."""
        if form_class is None:
            form_class = self.get_form_class()
        return form_class(user=self.request.user, **self.get_form_kwargs())

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

class ChangePasswordView(MyFormView):
    template_name = 'user_operation/change_password.html'
    form_class = ChangePasswordForm
    
class ChangeEmailView(MyFormView):
    template_name = 'user_operation/change_email.html'
    form_class = ChangeEmailForm
