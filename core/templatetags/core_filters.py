from django import template
from core.models import Category
register = template.Library()

@register.filter(name = 'filtering')
def filtering(value):
    categories = Category.objects.filter(category_wraper__name = value)
    return categories