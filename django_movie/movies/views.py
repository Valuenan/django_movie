from django.db.models import Q
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView, DetailView

from .models import Movie, Category, Actor, Genre
from .forms import ReviewForm


class GenreYear():
    '''Жанры и года фильмов'''

    def get_genres(self):
        return Genre.objects.only('name').all()

    def get_years(self):
        return Movie.objects.filter(draft=False).values('year')


class MovieView(GenreYear, ListView):
    '''Список фильмов'''

    model = Movie
    context_object_name = 'movies_list'
    queryset = Movie.objects.only('title', 'poster', 'tagline', 'draft', 'url').filter(draft=False)


class MovieDetailView(DetailView):
    '''Полное описание'''

    model = Movie
    slug_field = 'url'


class AddReview(GenreYear, View):
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
        print(queryset)
        return queryset
