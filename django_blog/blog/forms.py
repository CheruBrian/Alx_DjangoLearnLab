# blog/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile 
from .models import Post, Comment
from django.utils.text import slugify
from taggit.forms import TagWidget()
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
         tag_input = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control tag-input',
            'placeholder': 'Enter tags separated by commas',
            'data-role': 'tagsinput'  # For Bootstrap Tags Input
        }),
        help_text='Separate tags with commas'
    )
    class Meta:
        model = Post
        fields = ['title', 'content', 'meta_description', 'tag_input']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter post title'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Write your post content here...',
                'rows': 12,
                'id': 'post-content-editor'
            }),
            'meta_description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Brief description for SEO (optional, auto-generated if empty)',
                'rows': 3,
                'maxlength': 160
            }),
        }
         labels = {
            'meta_description': 'Meta Description (SEO)'
        }
         def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # If editing existing post, pre-fill tag_input with current tags
        if self.instance and self.instance.pk:
            tags = self.instance.tags.all()
            self.initial['tag_input'] = ', '.join(tag.name for tag in tags)
    
    def clean_tag_input(self):
        """Validate and clean tags"""
        tag_input = self.cleaned_data.get('tag_input', '')
        # Split by comma and clean each tag
        tags = [tag.strip() for tag in tag_input.split(',') if tag.strip()]
        
        # Limit number of tags
        if len(tags) > 10:
            raise forms.ValidationError("Maximum 10 tags allowed.")
        
        # Validate each tag
        for tag in tags:
            if len(tag) > 50:
                raise forms.ValidationError(f"Tag '{tag[:20]}...' is too long (max 50 chars).")
            if not all(c.isalnum() or c in ' -_' for c in tag):
                raise forms.ValidationError(f"Tag '{tag}' contains invalid characters.")
        
        return tags
    
    def save(self, commit=True):
        post = super().save(commit=False)
        
        if commit:
            post.save()
            # Clear existing tags
            post.tags.clear()
            # Add new tags
            tags = self.cleaned_data.get('tag_input', [])
            if tags:
                post.tags.add(*tags)
            self.save_m2m()
        
        return post
    
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
    class SearchForm(forms.Form):
    q = forms.CharField(
        required=False,
        label='Search',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search posts...',
            'aria-label': 'Search'
        })
    )
    
    tags = forms.CharField(
        required=False,
        widget=forms.HiddenInput()
    )
    
    search_in = forms.MultipleChoiceField(
        required=False,
        choices=[
            ('title', 'Title'),
            ('content', 'Content'),
            ('tags', 'Tags'),
            ('author', 'Author'),
        ],
        initial=['title', 'content', 'tags'],
        widget=forms.CheckboxSelectMultiple(attrs={
            'class': 'form-check-input'
        })
    )
    
    sort_by = forms.ChoiceField(
        required=False,
        choices=[
            ('relevance', 'Relevance'),
            ('newest', 'Newest First'),
            ('oldest', 'Oldest First'),
        ],
        initial='relevance',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
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