from django.urls import path

from . import views

app_name = 'authentication'
urlpatterns = [
    path(route='sign_up/', view=views.SignUpView.as_view(), name='sign_up'),
    path(route='sign_up/success/', view=views.sign_up_end, name='sign_up_end'),
    path(route='login/', view=views.SignIn.as_view(), name='login'),
    path(route='reset_password/', view=views.ResetPasswordView.as_view(), name='reset_password'),
    path(route='', view=views.main, name='main')
]
