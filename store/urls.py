from django.urls import path
from store import views

app_name = 'store'

urlpatterns =[
    path("",views.Home.as_view(), name ="home"),
    path('add_cart/',views.SessionAddCart.as_view(),name ='add_cart'),
    path('content/',views.SessionCartContent.as_view(),name = 'content'),
    path('add_modelcart/',views.ModelAddCart.as_view(),name = 'add_modelcart'),
    path('modelcontent/<int:pk>/',views.ModelCartContent.as_view(),name ='modelcontent'),
    path('delete_modelcart/',views.ModelCartDelete.as_view(),name = 'modelcart_delete'),
    path('delete_cart/',views.SessionCartDelete.as_view(),name = 'delete_cart'),
    path('preview/',views.PurchasePreview.as_view(),name = 'preview'),
    path('process/', views.PurchaseProcess.as_view(), name='process'),
    path('done/', views.PurchaseDone.as_view(), name='done'),
    
]
