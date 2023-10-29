from django.http import HttpResponseRedirect
from django.shortcuts import render
from datetime import datetime

from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post
from .filters import PostFilter
from .forms import PostForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

class PostList(ListView):
    model = Post
    ordering = '-title',
    template_name = 'PostCategory.html'
    context_object_name ='PostCategory'
    paginate_by = 3  # вот так мы можем указать количество записей на странице

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['next_sale'] = None
        context['filterset'] = self.filterset
        return context

class PostDetail(DetailView):
    # Модель всё та же, но мы хотим получать информацию по отдельному товару
    model = Post
    # Используем другой шаблон — product.html
    template_name = 'PostCategoryOneByOne.html'
    # Название объекта, в котором будет выбранный пользователем продукт
    context_object_name = 'PostCategoryOneByOne'



def create_news(request):
    form = PostForm()

    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/news/')

    return render(request, 'post_create.html', {'form': form})

# Добавляем новое представление для создания товаров.
class PostCreate(CreateView):
    # Указываем нашу разработанную форму
    form_class = PostForm
    # модель товаров
    model = Post
    # и новый шаблон, в котором используется форма.
    template_name = 'post_create.html'

class PostUpdate(LoginRequiredMixin,UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'post_create.html'

class PostDelete(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('news')


@method_decorator(login_required(login_url = '/login/'), name='dispatch')
class ProtectedView(TemplateView):
    template_name = 'prodected_page.html'

class ProtectedView(LoginRequiredMixin, TemplateView):
    template_name = 'prodected_page.html'