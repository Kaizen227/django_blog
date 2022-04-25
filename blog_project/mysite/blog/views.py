from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.utils import timezone
from blog.models import Post, Comment
from blog.forms import PostForm, CommentForm
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (TemplateView, ListView,
                                    DetailView, CreateView,
                                    UpdateView, DeleteView)

################################
##      Class Based Views     ##
################################

class AboutView(TemplateView):
    template_name = 'about.html'

class PostListView(ListView):
    model = Post


    def get_queryset(self):
        return Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')

class PostDetailView(DetailView):
    model = Post

class CreatePostView(LoginRequiredMixin,CreateView):
    login_url = '/login/'
    redirect_field_name = 'blog/post_detail.html'
    form_class = PostForm
    model = Post

class PostUpdateView(LoginRequiredMixin, UpdateView):
    login_url = '/login/'
    redirect_field_name = 'blog/post_detail.html'
    form_class = PostForm
    model = Post

class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('post_list')

class DraftListView(LoginRequiredMixin,ListView):
    login_url = '/login/'
    redirect_field_name = 'blog/post_list.html'
    model = Post

    def get_queryset(self):
        return Post.objects.filter(published_date__isnull=True).order_by('created_date')


################################
##        Function Views      ##
################################


@login_required
def post_publish(request,pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('post_detail', pk=pk)

@login_required
def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/comment_form.html',{'form':form})

@login_required
def comment_approve(request,pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('post_detail', pk=comment.post.pk)


@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post_pk = comment.post.pk
    comment.delete()
    return redirect('post_detail', pk=post_pk)


# def create(request):
#     if request.method=='POST':
#         form=UserCreationForm(request.POST)
#         if form.is_valid():
#             user=form.save(UserCreationForm)
#             username=form.cleaned_data.get('username')
#             login(request,user)

#             member = member(user=user)
#             member.save()
#             return redirect('post_list', pk=Post.pk)
#         else:
#             u = user=form.save(UserCreationForm)
#             u.delete()
#     form=UserCreationForm()
#     return render(request,'registration/create.html',context={'form':form})

# def login_user(request):
#     if request.method=='POST':
#         form=AuthenticationForm(request,request.POST)
#         if form.is_valid():
#             username=form.cleaned_data.get('username')
#             password=form.cleaned_data.get('password')
#             user= authenticate(username=username,password=password)
#             # user.is_staff = False
#             # user.is_superuser = False
#             if user is not None:
#                 if user.is_active:
#                     login(request, user)
#                     return redirect('post_list', pk=post.pk)
#         else:
#             form.error('Invalid')
#     form=AuthenticationForm()
#     return render(request,'registration/login_user.html',context={'form':form})

# def login_user(request):
#     post = Post
#     if request.method == 'POST':
#         form = AuthenticationForm(request=request, data=request.POST)
#         if form.is_valid():
#             username = form.cleaned_data.get('username')
#             password = form.cleaned_data.get('password')
#             user = authenticate(username=username, password=password)
#             if user is not None:
#                 login(request, user)
#                 messages.info(request, f"You are now logged in as {username}")
#                 return redirect('post_list', pk=post.pk)
#             else:
#                 messages.error(request, "Invalid username or password.")
#         else:
#             messages.error(request, "Invalid username or password.")
#     form = AuthenticationForm()
#     return render(request = request,
#                     template_name = "registration/login_user.html",
#                     context={"form":form})

def logout(request):
    post = Post
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect('http://127.0.0.1:8000/')
