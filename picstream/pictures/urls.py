from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_image, name='upload_image'),
    path('images/', views.all_images, name='all_images'),
    path('image/<int:image_id>/', views.image_detail, name='image_detail'),
]
