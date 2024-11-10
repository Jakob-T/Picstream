from django.db import models
from users.models import CustomUser

class Image(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='images')
    url = models.TextField(max_length=300, default="")
    caption = models.TextField(max_length=500, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Post by {self.user.username}'

class Comment(models.Model):
    post = models.ForeignKey(Image, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    text = models.TextField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.user.username} on {self.post}'

class Like(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    post = models.ForeignKey(Image, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Like by {self.user.username} on {self.post}'
