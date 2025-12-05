from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from django.utils import timezone


class Comment(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)  # For comment moderation

    class Meta:
        ordering = ["-published_date"]
        indexes = [
            models.Index(fields=['created_at']),
            models.Index(fields=['post', 'created_at']),
        ]
        
    def __str__(self):
        return self.title
    
     def get_absolute_url(self):
        return reverse("post-detail", kwargs={"pk": self.pk})
    
    def __str__(self):
        return f'Comment by {self.author.username} on {self.post.title}'
    
    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.post.pk})
    
    def can_edit(self, user):
        """Check if user can edit this comment"""
        return user.is_authenticated and (user == self.author or user.is_staff)
    
    def can_delete(self, user):
        """Check if user can delete this comment"""
        return user.is_authenticated and (user == self.author or user.is_staff or user == self.post.author)

class Profile(models.Model):
    """
    Simple user profile extending the built-in User model via OneToOne.
    Stores extra info like bio and avatar_url. Optional — you may omit this
    if you only need username/email for now.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    bio = models.TextField(blank=True)
    avatar_url = models.URLField(blank=True)

    def __str__(self):
        return f"Profile: {self.user.username}"

# Automatically create or save profile when user is created/updated
@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        instance.profile.save()