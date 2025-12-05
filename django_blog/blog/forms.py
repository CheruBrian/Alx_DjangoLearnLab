# blog/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile 
from .models import Post, Comment
class CustomUserCreationForm(UserCreationForm):
    """Extend default form to include email."""
    email = forms.EmailField(required=True, help_text="Required. Enter a valid email address.")

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")


class UserUpdateForm(forms.ModelForm):
    """Edit built-in user fields (username, email)."""
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email")


# Only if you added Profile model
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ("bio", "avatar_url")
        widgets = {
            "bio": forms.Textarea(attrs={"rows": 3}),
            "avatar_url": forms.URLInput(),
        }
    
    class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "content"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "w-full p-2 border rounded"}),
            "content": forms.Textarea(attrs={"class": "w-full p-2 border rounded h-48"}),
        }
    
    class PostForm(forms.ModelForm):
    # ... existing PostForm ...

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Write your comment here...',
                'rows': 3,
                'maxlength': 1000
            }),
        }
        labels = {
            'content': 'Your Comment'
        }
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        self.post = kwargs.pop('post', None)
        super().__init__(*args, **kwargs)
    
    def clean_content(self):
        content = self.cleaned_data.get('content')
        if not content or content.strip() == '':
            raise forms.ValidationError("Comment cannot be empty.")
        if len(content) < 3:
            raise forms.ValidationError("Comment must be at least 3 characters long.")
        return content

class CommentUpdateForm(CommentForm):
    """Form for updating comments"""
    class Meta(CommentForm.Meta):
        pass