from django.contrib import admin
from .models import (
    CategoryWraper,
    Category,
    DisplayWraper,
    Product,
    Slider,
    Brand_Logo_row1,
    Brand_Logo_row2,
    Brand_Logo_row3,
    Mobile_Category,
    Footer_Colum1,
    Footer_Colum2,
    Footer_Colum3,
    Footer_Colum4,
    Cart,
    
)
@admin.register(CategoryWraper)
class WaraperCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'category_image')

@admin.register(DisplayWraper)
class DisplayWraperAdmin(admin.ModelAdmin):
    list_display = ['name',]
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title','product_image', 'product_category','selling_prize', 'discounted_prize', 'description', 'brand')

@admin.register(Slider)
class SliderAdmin(admin.ModelAdmin):
    list_display = ('device', 'title', 'slider_image')

@admin.register(Brand_Logo_row1)
class BrandLogoAdmin(admin.ModelAdmin):
    list_display = ('title','logo')

@admin.register(Brand_Logo_row2)
class BrandLogoAdmin(admin.ModelAdmin):
    list_display = ('title','logo')

@admin.register(Brand_Logo_row3)
class BrandLogoAdmin(admin.ModelAdmin):
    list_display = ('title','logo')

@admin.register(Mobile_Category)
class MobileCategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'mobile_category_image')

@admin.register(Footer_Colum1)
class FooterColumAdmin(admin.ModelAdmin):
    list_display = ('content',)

@admin.register(Footer_Colum2)
class FooterColum2Admin(admin.ModelAdmin):
    list_display = ('content',)

@admin.register(Footer_Colum3)
class FooterColum3Admin(admin.ModelAdmin):
    list_display = ('content',)

@admin.register(Footer_Colum4)
class FooterColum4Admin(admin.ModelAdmin):
    list_display = ('content',)

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'product','unit', 'unit_amount', 'color', 'quantity','size']

# Register your models here.
