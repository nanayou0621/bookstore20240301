from django.urls import path
from .views import *
 
app_name = 'contacts'
urlpatterns = [
    path('home/', Home.as_view(), name='home'),
    path('individual_input/', IndividualContactInput.as_view(), name='individual_input'),
    path('individual_confirm/', IndividualContactConfirm.as_view(), name='individual_confirm'),
    path('individual_create/', IndividualContactCreate.as_view(), name='individual_create'),
    path('form_send_complete/', FormSendComplete.as_view(), name='form_send_complete'),
]