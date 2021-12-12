from django.urls import path

from . import views

urlpatterns = [
    # /siteapp/
    path('', views.IndexView.as_view(), name='index'),
    path('faq/', views., name='faq'),
    path('u/', views.UserInfoView.as_view(), name='info'),
    path('customvision/', views.BackgroundImageAnalyze.as_view(), name="customvision"),
    path('foodanalize/', views.BackgroundFoodAnalzeView.as_view(), name="foodanalize")
]