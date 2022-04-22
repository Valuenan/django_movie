from django import template
from movies.models import Category, Movie

register = template.Library()


@register.simple_tag()
def get_categories():
    '''Вывод всех категорий'''

    return Category.objects.only("name", "url").all()


@register.inclusion_tag('movies/tags/last_movies.html')
def get_last_movies(count=5):
    '''Вывод последних фильмов'''
    movies = Movie.objects.only("poster", "title").order_by("-id")[:count]
    return {"last_movies": movies}
