from django import template
from core.models import Category, ProductAttributeValue
register = template.Library()

@register.filter(name = 'filtering')
def filtering(value):
    categories = Category.objects.filter(category_wraper__name = value)
    return categories

@register.filter(name = 'PSFiltering')
def PSFiltering(value):
    if value.product.ProductType.typeName == "Cloth"  or value.product.ProductType.typeName == "Shoe":
        stock = value.product.productattributevalue_set.get(attributeValue__attributeValue = value.size).productStock
    else:
        stock = value.product.productattributevalue_set.first().productStock
    return stock