from django.urls import path
from . import views
from .views import *
from tourist_app import views as profile_views

urlpatterns = [
    path('', views.profile_view, name='profile'),
    path('profile/', profile_views.profile_view, name='profile'),
    path('signup/', views.signup, name='signup'),
    # path('create/', DestinationCreateView.as_view(), name="create-destination"),
    # path('detail/<int:pk>', DestinationDetails.as_view, name="detail"),
    # path('update/<int:pk>', DestinationUpdateView.as_view, name="update-destination"),
    # path('delete/<int:pk>', DestinationDetailsDelete.as_view, name="delete-destination"),
    
    path('create_destination/', views.create_destination, name='create_destination'),
    path('destination_fetch/<int:id>/', views.destination_fetch, name='destination_fetch'),
    path('update_destination/<int:id>/', views.destination_update, name='update_destination'),
    path('destination_delete/<int:id>', views.destination_delete, name='destination_delete'),
]