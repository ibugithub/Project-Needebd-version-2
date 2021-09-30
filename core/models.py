from django.db import models
from ProjectNeedeBd import settings
from django.core.validators import MinValueValidator,  MaxValueValidator
# Create your models here.

class DisplayWraper(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return str(self.name)
class CategoryWraper(models.Model):
    name = models.CharField(max_length=40)
    category_image = models.ImageField(upload_to = 'category_wraper_image', null=True, blank=True)
    display_wraper = models.ForeignKey(DisplayWraper, on_delete=models.CASCADE, null=True, blank=True)
    def __str__(self):
        return str(self.name)


DEVICE_CHOICES = (
    ('Mobile', 'Mobile'),
    ('Desktop', 'Desktop')
)

class Slider(models.Model):
    title = models.CharField(max_length=100, null=True)
    slider_image = models.ImageField(upload_to = 'slider_image')
    device = models.CharField(choices=DEVICE_CHOICES, max_length=20)

class Brand_Logo_row1(models.Model):
    title = models.CharField(max_length=100, null=True)
    logo = models.ImageField(upload_to = 'brand_logo')

class Brand_Logo_row2(models.Model):
    title = models.CharField(max_length=100, null=True)
    logo = models.ImageField(upload_to = 'brand_logo')

class Brand_Logo_row3(models.Model):
    title = models.CharField(max_length=100, null=True)
    logo = models.ImageField(upload_to = 'brand_logo')

class Mobile_Category(models.Model):
    title = models.CharField(max_length=100)
    mobile_category_image = models.ImageField(upload_to = 'Mcataegory_image')

class Footer_Colum1(models.Model):
    content = models.CharField(max_length=200)

class Footer_Colum2(models.Model):
    content = models.CharField(max_length=200)

class Footer_Colum3(models.Model):
    content = models.CharField(max_length=200)

class Footer_Colum4(models.Model):
    content = models.CharField(max_length=200)


# Cart functionality will be from here

class Category(models.Model):
    title= models.CharField(max_length=100)
    category_image = models.ImageField(upload_to = 'simages', null= True, blank=True)
    category_wraper = models.ForeignKey(CategoryWraper, on_delete=models.CASCADE, null=True, blank=True)
    display_wraper = models.ForeignKey(DisplayWraper, on_delete=models.CASCADE, null=True, blank=True)
    def __str__(self):
        return str(self.title)

class Product(models.Model):
    title = models.CharField(max_length=100)
    product_image = models.ImageField(upload_to = 'product_image')
    product_category = models.ForeignKey(Category, on_delete= models.CASCADE, null=True)
    selling_prize =models.FloatField()
    discounted_prize = models.FloatField()
    description = models.TextField()
    brand = models.CharField(max_length=100, null=True, blank=True)
    display_wraper = models.ForeignKey(DisplayWraper, on_delete=models.CASCADE, null=True, blank=True)   
    discount = models.IntegerField(null=True, blank=True)
    sell_amount= models.IntegerField(null=True, blank=True)
    def __str__(self):
        return str(self.title)
    Unit_Choices = (
                        ("Kg", "Kg"),
                        ("Liter", "Liter"),
                        ("ClothSize", "ClothSize"),
                        ("ClothPicesSize", "ClothPicesSize"),
                        ("ShoeSize", "ShoeSize"),
                        ("Packet", "Packet")
                      )
    unit = models.CharField(max_length=30, choices = Unit_Choices, null = True)
   
class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(0)],  default = 1)
    unit = models.CharField(max_length = 30, null = True)
    unit_amount = models.IntegerField(null = True)
    color = models.CharField(max_length = 30, null = True)
    size  = models.CharField(max_length = 40, null = True)
   
    def __str__(self):
        return str(self.id)
    
    @property
    def products_cost(self):
        return self.quantity * self.product.discounted_prize

    