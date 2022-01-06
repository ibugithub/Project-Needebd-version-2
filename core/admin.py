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
    CustomerProfile,
    Districts,
    Divisions,
    Unions,
    Upazilas,
    CustomerAddress,
    CourierServices,
    Order,
    OrderSummary,
    ProductType,
    Attribute,
    AttributeValue,
    PTAttributeValue,
    ProductAttributeValue
)

@admin.register(ProductType)
class ProductTypeAdmin(admin.ModelAdmin):
    list_display = ('typeName',)

@admin.register(Attribute)
class AttributeAdmin(admin.ModelAdmin):
    list_display = ("attributeName",)

@admin.register(AttributeValue)
class AttributeValueAdmin(admin.ModelAdmin):
    list_display = ("attribute","attributeValue")

@admin.register(PTAttributeValue)
class PTAValueAdmin(admin.ModelAdmin):
    list_display = ('productType','attributeValue')

@admin.register(ProductAttributeValue)
class PAValueAdmin(admin.ModelAdmin):
    list_display = ('product','attributeValue', 'productStock')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'category_image')

@admin.register(CategoryWraper)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'category_image', 'display_wraper')

@admin.register(DisplayWraper)
class DisplayWraperAdmin(admin.ModelAdmin):
    list_display = ['name',]
    
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('ProductType','title','product_image', 'product_category','selling_prize', 'discounted_prize', 'description', 'brand')

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

@admin.register(CustomerProfile)
class CustomerProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'full_name','phone_number','email', 'birthdate', 'gender', 'image']

@admin.register(Divisions)
class DivisionsAdmin(admin.ModelAdmin):
    list_display = ['id','name','bn_name','url']

@admin.register(Districts)
class DistrictsAdmin(admin.ModelAdmin):
    list_display = ['id','division_id', 'name','bn_name', 'lat','lon', 'url']

@admin.register(Upazilas)
class UpazilasAdmin(admin.ModelAdmin):
    list_display = ['id','district_id', 'name', 'bn_name', 'url']

@admin.register(Unions)
class UnionsAdmin(admin.ModelAdmin):
    list_display = ['id','upazilla_id', 'name', 'bn_name','url']

@admin.register(CustomerAddress)
class CustomerAddressAdmin(admin.ModelAdmin):
    list_display = ['user','full_name','phone_number', 'divisions', 'districts','upazilas', 'unions', 'address', 'isDefault']

@admin.register(CourierServices)
class UnionsAdmin(admin.ModelAdmin):
    list_display = ['name', 'courierImage']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['ordered_date','user','profile','address', 'product', 'quantity','unit', 'unitAmount', 'size','ordered_date', 'status', 'is_summuried']

@admin.register(OrderSummary)
class OrderAdmin(admin.ModelAdmin):
    filter_horizontal = ('orderItem',)