import os
import requests
from django.core.files.base import ContentFile
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Image, Comment, Like
from django.conf import settings
from users.models import CustomUser
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
@login_required
def upload_image(request):
    if request.method == 'POST':
        url = request.POST.get('url')
        caption = request.POST.get('caption', '')

        if not url:
            messages.error(request, 'Molimo unesite URL slike.')
            return render(request, 'pictures/upload.html')

        try:
            response = requests.get(url)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            messages.error(request, 'Nije moguće dohvatiti sliku. Provjerite URL.')
            return render(request, 'core/upload_via_url.html')

        image = Image(user=request.user, caption=caption, url=url)
        image.save()

        messages.success(request, 'Slika uspješno učitana.')
        return redirect('home')

    return render(request, 'pictures/upload.html')

@login_required
def all_images(request):
    images = Image.objects.all()

    context = {
        'images': images
    }
    return render(request, 'pictures/picturelist.html', context)


@login_required
def image_detail(request, image_id):
    image = get_object_or_404(Image, id=image_id)

    if request.method == 'POST':
        if 'comment' in request.POST:
            comment_text = request.POST.get('comment')
            if comment_text:
                Comment.objects.create(post=image, user=request.user, text=comment_text)

        elif 'like' in request.POST:
            like, created = Like.objects.get_or_create(post=image, user=request.user)
            if not created:
                like.delete()

        return HttpResponseRedirect(reverse('image_detail', args=[image.id]))

    is_liked = image.likes.filter(user=request.user).exists()

    context = {
        'image': image,
        'comments': image.comments.all(),
        'likes': image.likes.count(),
        'is_liked': is_liked,
    }

    return render(request, 'pictures/image_detail.html', context)