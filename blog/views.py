from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.views.generic import ListView, DetailView
from django.db.models import Q  # For search functionality
from .models import Post, Category, Comment, Profile  # ← ADDED Profile
from .forms import CommentForm, PostForm, ProfileForm

def home(request):
    recent_posts = Post.objects.all().order_by('-published_date')[:3]
    categories = Category.objects.all()
    return render(request, 'blog/home.html', {
        'recent_posts': recent_posts,
        'categories': categories
    })

def about(request):
    return render(request, 'blog/about.html')

class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 5
    ordering = ['-published_date']
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['recent_posts'] = Post.objects.all().order_by('-published_date')[:5]
        return context

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        context['comments'] = self.object.comments.filter(approved=True)
        return context

def category_posts(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    posts = Post.objects.filter(category=category).order_by('-published_date')
    return render(request, 'blog/category_posts.html', {
        'category': category,
        'posts': posts
    })

@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, 'Post created successfully!')
            return redirect('blog:post_detail', pk=post.id)
    else:
        form = PostForm()
    
    categories = Category.objects.all()
    return render(request, 'blog/create_post.html', {
        'form': form,
        'categories': categories
    })

@login_required
def add_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            
            # Send email notification to post author
            if post.author != request.user:  # Don't notify if commenting on own post
                try:
                    from .utils import send_comment_notification
                    send_comment_notification(comment)
                except Exception as e:
                    # If email fails, just continue without error
                    print(f"Email notification failed: {e}")
            
            messages.success(request, 'Your comment has been added!')
            return redirect('blog:post_detail', pk=post.pk)
    
    # If form is invalid or GET request, redirect back to post detail
    return redirect('blog:post_detail', pk=post.pk)

# ADD THIS MISSING LIKE POST VIEW
@login_required
def like_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    
    # Check if user already liked the post
    from .models import Like  # Import here to avoid circular imports
    like, created = Like.objects.get_or_create(
        post=post,
        user=request.user
    )
    
    if not created:
        # User already liked, so unlike
        like.delete()
        messages.info(request, 'Post unliked!')
    else:
        messages.success(request, 'Post liked!')
    
    return redirect('blog:post_detail', pk=post.pk)

def search_posts(request):
    query = request.GET.get('q')
    if query:
        posts = Post.objects.filter(
            Q(title__icontains=query) | 
            Q(content__icontains=query) |
            Q(author__username__icontains=query)
        ).distinct().order_by('-published_date')
    else:
        posts = Post.objects.none()
    
    return render(request, 'blog/search_results.html', {
        'posts': posts,
        'query': query
    })

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            # Send welcome email
            try:
                from .utils import send_welcome_email
                send_welcome_email(user)
            except Exception as e:
                print(f"Welcome email failed: {e}")
            
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now log in.')
            return redirect('blog:login')
    else:
        form = UserCreationForm()
    return render(request, 'blog/register.html', {'form': form})

@login_required
def profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('blog:profile')
    else:
        form = ProfileForm(instance=request.user.profile)
    
    return render(request, 'blog/profile.html', {'form': form})

@login_required
def my_posts(request):
    posts = Post.objects.filter(author=request.user).order_by('-published_date')
    return render(request, 'blog/my_posts.html', {'posts': posts})