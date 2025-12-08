from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from django.db.models import Q
from django.contrib import messages
from django.utils.translation import gettext as _  
from django.views.decorators.cache import cache_page
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.utils.translation import gettext as _

from .models import Club, Post, Comment
from .forms import CommentForm
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import logout as auth_logout
from django.contrib import messages
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _


# === ГЛАВНАЯ СТРАНИЦА: ПРОСТО СПИСОК КЛУБОВ ===
@method_decorator(cache_page(60 * 5), name='dispatch')
class HomeClubListView(ListView):
    model = Club
    template_name = 'club_list.html' 
    context_object_name = 'clubs'
    paginate_by = 12

    def get_queryset(self):
        return Club.objects.all().order_by('name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recent_posts'] = Post.objects.order_by('-date_posted')[:5]
        return context


# === СТРАНИЦА ГЛОБАЛЬНОГО ПОИСКА + ФИЛЬТРЫ ===
@method_decorator(cache_page(60 * 5), name='dispatch')
class SearchView(ListView):
    template_name = 'search_results.html'
    context_object_name = 'results'
    paginate_by = 12

    def get_queryset(self):
        q = self.request.GET.get('q', '').strip()
        club_id = self.request.GET.get('club')
        country = self.request.GET.get('country')
        post_club = self.request.GET.get('post_club')
        author = self.request.GET.get('author')
        year = self.request.GET.get('year')
        month = self.request.GET.get('month')

        clubs = Club.objects.all()
        posts = Post.objects.select_related('club').all()

        if q:
            clubs = clubs.filter(Q(name__icontains=q) | Q(country__icontains=q))
            posts = posts.filter(Q(title__icontains=q) | Q(content__icontains=q))

        if club_id:
            clubs = clubs.filter(id=club_id)
        if country:
            clubs = clubs.filter(country=country)
        if post_club:
            posts = posts.filter(club_id=post_club)
        if author:
            posts = posts.filter(author__icontains=author)
        if year:
            posts = posts.filter(date_posted__year=year)
        if month:
            posts = posts.filter(date_posted__month=month)

        # Объединяем и сортируем: клубы по имени, посты по дате
        results = list(clubs.order_by('name')) + list(posts.order_by('-date_posted'))
        return results

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('q', '')
        context['clubs'] = Club.objects.all().order_by('name')
        context['countries'] = Club.objects.values_list('country', flat=True).distinct().order_by('country')

        dates = Post.objects.dates('date_posted', 'month', order='DESC')
        context['available_dates'] = [(d.year, d.month, d.strftime('%B %Y')) for d in dates]

        context['selected_club'] = self.request.GET.get('club', '')
        context['selected_country'] = self.request.GET.get('country', '')
        context['selected_post_club'] = self.request.GET.get('post_club', '')
        context['selected_author'] = self.request.GET.get('author', '')
        context['selected_year'] = self.request.GET.get('year', '')
        context['selected_month'] = self.request.GET.get('month', '')

        return context


# === ПРОСТО ВСЕ ПОСТЫ (БЕЗ ФИЛЬТРОВ) ===
@method_decorator(cache_page(60 * 5), name='dispatch')
class PostListView(ListView):
    model = Post
    template_name = 'post_list.html'
    context_object_name = 'posts'
    paginate_by = 10
    ordering = ['-date_posted']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recent_posts'] = Post.objects.order_by('-date_posted')[:5]
        return context


# === ДЕТАЛИ КЛУБА ===
@method_decorator(cache_page(60 * 5), name='dispatch')
class ClubDetailView(DetailView):
    model = Club
    template_name = 'club_detail.html'
    context_object_name = 'club'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recent_posts'] = Post.objects.order_by('-date_posted')[:5]
        return context
    
# === РЕГИСТРАЦИЯ ===
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, _("Регистрация прошла успешно! Добро пожаловать!"))
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


# === ДЕТАЛИ ПОСТА + КОММЕНТАРИИ ===
@login_required(login_url='login')
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.filter(is_published=True).order_by('-created_at')

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()

            # === УВЕДОМЛЕНИЕ НА EMAIL ===
            send_mail(
                subject=f"Новый комментарий: {comment.subject}",
                message=(
                    f"Пользователь: {request.user.username}\n"
                    f"Пост: {post.title}\n\n"
                    f"Тема: {comment.subject}\n"
                    f"Текст:\n{comment.text}\n"
                ),
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[settings.ADMIN_EMAIL],
                fail_silently=False,
            )

            messages.success(request, _("Ваш комментарий отправлен на модерацию!"))
            return redirect('post_detail', pk=pk)
    else:
        form = CommentForm()

    return render(request, 'post_detail.html', {
        'post': post,
        'comments': comments,
        'form': form,
        'recent_posts': Post.objects.order_by('-date_posted')[:5],
    })

def custom_logout(request):
    auth_logout(request)
    messages.success(request, _("Вы успешно вышли из аккаунта."), extra_tags="logout")
    return redirect('home')