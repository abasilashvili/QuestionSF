from .models import Post, PostCategory
from datetime import datetime
from django.shortcuts import get_object_or_404, render
from .filters import PostFilter
from .forms import NewsForm, ArticleForm
from django.urls import reverse_lazy
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView)
from django.urls import reverse
from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'protect/index.html'


class PostListView(ListView):
    model = Post

    ordering = '-creation_date_time'

    template_name = 'posts.html'

    context_object_name = 'posts'

    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['next_sale'] = "Репортаж в среду!"
        context['news'] = Post.objects.all()
        context['filterset'] = self.filterset
        return context


def news_detail(request, pk):
    news = get_object_or_404(Post, pk=pk, post_type=Post.NEWS)
    return render(request, 'news_detail.html', {'post': news})


def article_detail(request, pk):
    article = get_object_or_404(Post, pk=pk, post_type=Post.ARTICLE)
    return render(request, 'article_detail.html', {'post': article})


class PostDetailView(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['next_sale'] = "Репортаж в среду!"
        context['news'] = Post.objects.all()
        return context


class NewsCreate(CreateView):
    form_class = NewsForm
    model = Post
    template_name = 'news_edit.html'

    def form_valid(self, form):
        form.instance.post_type = Post.NEWS
        response = super().form_valid(form)
        self.success_url = reverse('news_detail', kwargs={'pk': self.object.pk})
        return response


class NewsUpdate(UpdateView):
    form_class = NewsForm
    model = Post
    template_name = 'news_edit.html'


class NewsDelete(DeleteView):
    model = Post
    template_name = 'news_delete.html'
    success_url = reverse_lazy('news_list')


class ArticleCreate(CreateView):
    form_class = ArticleForm
    model = Post
    template_name = 'article_edit.html'

    def form_valid(self, form):
        form.instance.post_type = Post.ARTICLE
        response = super().form_valid(form)
        self.success_url = reverse('article_detail', kwargs={'pk': self.object.pk})
        return response


class ArticleUpdate(UpdateView):
    form_class = ArticleForm
    model = Post
    template_name = 'article_edit.html'


class ArticleDelete(DeleteView):
    model = Post
    template_name = 'article_delete.html'
    success_url = reverse_lazy('news_list')


class NewsListView(PostListView):
    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset.filter(post_type=Post.NEWS))
        return self.filterset.qs


class ArticleListView(PostListView):
    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset.filter(post_type=Post.ARTICLE))
        return self.filterset.qs
