from contextlib import ContextDecorator
from dataclasses import field
from math import log
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import (ListView, DetailView, CreateView, UpdateView, DeleteView) 
from .models import Post
# Create your views here.


# SENDING EMAIL 
from django.core.mail import send_mail
def send_simple_email(request):
    send_mail(
        subject='Welcome!', # Subject
        message='Hello, Thanks for Visiting Our Website!', # Plain Text Body
        from_email='DEFAULT_FROM_EMAIL',
        recipient_list=['example@gmail.com'], # To Whom
        fail_silently=False, #if Fails raise exception.
    )
    return HttpResponse("Email Sent!")
# -------------


#Logger instance
import logging 
logger = logging.getLogger(__name__)

def home(request):
    context = {
        'posts': Post.objects.all()
    }
    logger.info("We Opened a Home Page")
    # return HttpResponse('<h1>Blog Home</h1>')
    return render(request, '/home.html', context)

class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html' #<app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5

class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html' #<app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    # ordering = ['-date_posted']
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')

class PostDetailView(DetailView):
    model = Post

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user 
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content'] 

    def form_valid(self, form):
        form.instance.author = self.request.user 
        return super().form_valid(form)

    def test_func(self):
        posts = self.get_object()
        if self.request.user == posts.author:
            return True
        return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin,DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        posts = self.get_object()
        if self.request.user == posts.author:
            return True
        return False

def about(request):
    # return HttpResponse('<h1>Blog About</h1>')
    return render(request, 'blog/about.html', {'title' : 'About' })


