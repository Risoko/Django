from django.urls import path

from .views import (
    sign_up_view, sign_up_end, SignIn, main, reset_password_view
)

app_name = 'authentication'
urlpatterns = [
    path(route='sign_up/', view=sign_up_view, name='sign_up'),
    path(route='sign_up/success/', view=sign_up_end, name='sign_up_end'),
    path(route='login/', view=SignIn.as_view(), name='login'),
    path(route='reset_password/', view=reset_password_view, name='reset_password'),
    path(route='', view=main, name='main')
]
