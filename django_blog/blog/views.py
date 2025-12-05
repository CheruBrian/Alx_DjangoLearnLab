# blog/views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, UserUpdateForm, ProfileUpdateForm  # import accordingly
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from .models import Post
from .forms import PostForm
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import FormMixin
from django.urls import reverse_lazy
from .models import Post, Comment
from .forms import PostForm, CommentForm, CommentUpdateForm

def home(request):
    return render(request, "blog/home.html")


def register(request):
    """
    User registration view. Uses CustomUserCreationForm to create a user.
    After successful registration, user is redirected to login page.
    """
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, "Account created successfully. You can now log in.")
            return redirect("login")
    else:
        form = CustomUserCreationForm()
    return render(request, "blog/register.html", {"form": form})


@login_required
def profile(request):
    """
    Profile view to view & edit user's profile and basic info.
    Uses UserUpdateForm and ProfileUpdateForm (if Profile model is present).
    """
    if request.method == "POST":
        user_form = UserUpdateForm(request.POST, instance=request.user)
        if hasattr(request.user, "profile"):
            profile_form = ProfileUpdateForm(request.POST, instance=request.user.profile)
        else:
            profile_form = None

        if user_form.is_valid() and (profile_form is None or profile_form.is_valid()):
            user_form.save()
            if profile_form:
                profile_form.save()
            messages.success(request, "Your profile has been updated.")
            return redirect("profile")
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile) if hasattr(request.user, "profile") else None

    context = {
        "user_form": user_form,
        "profile_form": profile_form,
    }
    return render(request, "blog/profile.html", context)

class PostListView(ListView):
    model = Post
    template_name = "blog/post_list.html"
    context_object_name = "posts"
    paginate_by = 10  # optional

class PostDetailView(DetailView):
    model = Post
    template_name = "blog/post_detail.html"
    context_object_name = "post"
    form_class = CommentForm
    
     def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        
        # Get all active comments for this post
        comments = post.comments.filter(is_active=True).select_related('author')
        
        # Add comment form and comments to context
        context['comments'] = comments
        context['comment_form'] = self.get_form()
        context['comment_count'] = comments.count()
        
        # Check if user can comment
        context['can_comment'] = self.request.user.is_authenticated
        
        return context
    
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'You must be logged in to comment.')
            return redirect('login')
        
        self.object = self.get_object()
        form = self.get_form()
        
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
    
    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.post = self.object
        comment.author = self.request.user
        comment.save()
        
        messages.success(self.request, 'Your comment has been posted!')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('post-detail', kwargs={'pk': self.object.pk})

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = "blog/post_form.html"

    def form_valid(self, form):
        # set author to logged-in user before saving
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = "blog/post_form.html"

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = "blog/post_confirm_delete.html"
    success_url = reverse_lazy("post-list")

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author
    
class CommentCreateView(LoginRequiredMixin, CreateView):
    """Alternative view for creating comments via AJAX or separate page"""
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment_form.html'
    
    def form_valid(self, form):
        post = get_object_or_404(Post, pk=self.kwargs['post_pk'])
        comment = form.save(commit=False)
        comment.post = post
        comment.author = self.request.user
        comment.save()
        
        messages.success(self.request, 'Comment posted successfully!')
        return redirect('post-detail', pk=post.pk)

class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    form_class = CommentUpdateForm
    template_name = 'blog/comment_form.html'
    
    def test_func(self):
        comment = self.get_object()
        return comment.can_edit(self.request.user)
    
    def handle_no_permission(self):
        messages.error(self.request, "You don't have permission to edit this comment.")
        return redirect('post-detail', pk=self.get_object().post.pk)
    
    def form_valid(self, form):
        messages.success(self.request, 'Comment updated successfully!')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('post-detail', kwargs={'pk': self.object.post.pk})

class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'blog/comment_confirm_delete.html'
    
    def test_func(self):
        comment = self.get_object()
        return comment.can_delete(self.request.user)
    
    def handle_no_permission(self):
        messages.error(self.request, "You don't have permission to delete this comment.")
        return redirect('post-detail', pk=self.get_object().post.pk)
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Comment deleted successfully!')
        return super().delete(request, *args, **kwargs)
    
    def get_success_url(self):
        return reverse_lazy('post-detail', kwargs={'pk': self.object.post.pk})

@login_required
def comment_reply(request, pk):
    """View for replying to a comment"""
    parent_comment = get_object_or_404(Comment, pk=pk)
    post = parent_comment.post
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.parent = parent_comment  # If you add parent field for nested comments
            comment.save()
            messages.success(request, 'Reply posted successfully!')
            return redirect('post-detail', pk=post.pk)
    else:
        form = CommentForm()
    
    return render(request, 'blog/comment_reply.html', {
        'form': form,
        'parent_comment': parent_comment,
        'post': post
    })
