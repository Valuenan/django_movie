from django.db.models import Q, Avg
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView, DetailView

from .models import Movie, Category, Actor, Genre, Rating
from .forms import ReviewForm, RatingForm


class GenreYear():
    '''Жанры и года фильмов'''

    def get_genres(self):
        return Genre.objects.only('name').all()

    def get_years(self):
        return Movie.objects.filter(draft=False).values('year').distinct('year')


class MovieView(GenreYear, ListView):
    '''Список фильмов'''

    model = Movie
    context_object_name = 'movies_list'
    queryset = Movie.objects.only('title', 'poster', 'tagline', 'draft', 'url').filter(draft=False)
    ordering = ['id']
    paginate_by = 1


class MovieDetailView(GenreYear, DetailView):
    '''Полное описание'''

    model = Movie
    slug_field = 'url'

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARD_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def get_context_data(self, **kwargs):
        context = super(MovieDetailView, self).get_context_data(**kwargs)
        movie_id = self.model.objects.get(url=self.kwargs['slug']).id
        context["form"] = ReviewForm()

        context["star_form"] = RatingForm()

        rating = Rating.objects.filter(movie=movie_id, ip=self.get_client_ip(self.request))

        if rating:
            rating = rating[0]
        else:
            rating = 0
        context["user_rating"] = rating

        avg_star = Rating.objects.filter(movie=movie_id).aggregate(Avg('star__value'))
        context["average_stars"] = lambda avg: round(avg_star['star__value__avg'], 1) if avg_star else 0

        return context


class AddReview(View):
    '''Отзыв'''

    def post(self, request, pk):
        form = ReviewForm(request.POST)
        movie = Movie.objects.get(id=pk)
        if form.is_valid():
            form = form.save(commit=False)
            if request.POST.get("parent", None):
                print(int(request.POST.get("parent")))
                form.parent_id = int(request.POST.get("parent"))
            form.movie = movie
            form.save()
        return redirect(movie.get_absolute_url())


class ActorView(GenreYear, DetailView):
    '''Вывод информации об актере'''

    model = Actor
    context_object_name = 'actor'
    template_name = 'movies/actor.html'
    slug_field = 'name'


class FilterMovieView(GenreYear, ListView):
    '''Фильтрация фильмов'''

    context_object_name = 'movies_list'
    paginate_by = 1

    def get_queryset(self):
        genre = self.request.GET.getlist('genre')
        year = self.request.GET.getlist('year')
        if genre and year:
            queryset = Movie.objects.only('title', 'tagline', 'poster').filter(
                Q(genres__in=genre),
                Q(year__in=year)).distinct('title')
        else:
            queryset = Movie.objects.only('title', 'tagline', 'poster').filter(
                Q(genres__in=genre) |
                Q(year__in=year)).distinct('title')
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super(FilterMovieView, self).get_context_data(*args, **kwargs)
        context["year"] = ''.join(f'year={x}&' for x in self.request.GET.getlist("year"))
        context["genre"] = ''.join(f'genre={x}&' for x in self.request.GET.getlist("genre"))
        return context


class AddStarRating(View):
    '''Добавление рейтинга фильму'''

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARD_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def post(self, request):
        form = RatingForm(request.POST)
        if form.is_valid():
            Rating.objects.update_or_create(
                ip=self.get_client_ip(request),
                movie_id=int(request.POST.get('movie')),
                defaults={'star_id': int(request.POST.get('star'))}
            )
            return HttpResponse(status=201)
        else:
            return HttpResponse(status=400)


class SearchView(GenreYear, ListView):
    '''Поиск по названию'''
    paginate_by = 1
    context_object_name = 'movies_list'

    def get_queryset(self):
        res = Movie.objects.filter(title__contains=self.request.GET.get('q'))
        if not res:
            res = Movie.objects.filter(title__contains=self.request.GET.get('q').capitalize())
        return res

    def get_context_data(self, *args, **kwargs):
        context = super(SearchView, self).get_context_data(*args, **kwargs)
        context['q'] = f'q={self.request.GET.get("q")}&'
        return context
