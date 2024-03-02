from django.urls import path
# from .views import Home
from . import views

app_name = 'books'

urlpatterns = [
    path('book_list/', views.BookList.as_view(), name='book_list'),
    path('group_create/',views.GroupCreateView.as_view(),name ='group_create'),
    path('goods_create/',views.BookCreateView.as_view(),name = 'goods_create'),
    path('detail/<int:pk>/', views.BookDetail.as_view(), name='detail'),
]
    