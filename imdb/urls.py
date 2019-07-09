from django.urls import path
from imdb import views

urlpatterns = [
    path('', views.review_list, name='review_list'),
    path('new/', views.review_new, name='review_new'),
]
