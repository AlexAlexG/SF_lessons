from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import *
from .filters import PostFilter
from datetime import datetime
from .forms import PostForm

class PostList(ListView):
    model = Post
    ordering = 'title'
    template_name = 'news.html'
    context_object_name = 'news'
    paginate_by = 10

    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     self.filterset = PostFilter(self.request.GET, queryset)
    #     return self.filterset.qs
    #
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     # context['time_now'] = datetime.utcnow()
    #     # context['next_sale'] = None
    #     # context['sorted_posts'] = Post.objects.filter().order_by('-dateCreation')
    #     context['filterset'] = self.filterset
    #     return context

class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'

class PostSearch(ListView):
    model = Post
    ordering = ['dateCreation']
    template_name = 'search.html'
    context_object_name = 'news'
    paginate_by = 10
    form_class = PostForm

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        # context['']
        return context

# class PostSearch(ListView):
#     model = Post
#     template_name = "search.html"
#     context_object_name = "news"
#     ordering = ["dateCreation"]
#     paginate_by = 10
#     form_class = PostForm
#
#     def get_filter(self):
#         return PostFilter(self.request.GET, queryset=super().get_queryset())
#
#     def get_queryset(self):
#         return self.get_filter().qs
#
#     def get_context_data(self, *args, **kwargs):
#         return {
#             **super().get_context_data(*args, **kwargs),
#             "filterset": self.get_filter(),
#         }

# def create_post(request):
#     if request.method == 'POST':
#         form = PostForm(request.POST)
#         form.save()
#         return HttpResponseRedirect('/news/')
#     form = PostForm()
#     return render(request, 'post_edit.html', {'form':form})

class PostCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post',)
    raise_exception = True
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'

    # def form_valid(self, form):
    #     product = form.save(commit=False)
    #     post.categoryType.choices = 'NW'
    #     return super().form_valid(form)

class PostUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post',)
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'

class PostDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('news.delete_post',)
    model = Post
    template_name='post_delete.html'
    success_url= reverse_lazy('post_list')