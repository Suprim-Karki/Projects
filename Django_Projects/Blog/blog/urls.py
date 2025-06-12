from django.urls import path
from . import views

urlpatterns=[
    path('',views.index,name='index'),
    path('post/<str:x>',views.post,name='post'),
    path('addpost',views.addpost,name='addpost'),

]