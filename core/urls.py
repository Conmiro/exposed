from django.urls import path

from . import views

urlpatterns = [
    path('profile/<int:profile_id>', views.profile_view, name='profile'),
    path('new_profile/', views.new_profile),
    path('browse/', views.browse),

]