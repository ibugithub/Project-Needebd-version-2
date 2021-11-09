from django.db import models
from django.db.models.deletion import SET_NULL
from ProjectNeedeBd import settings
from django.core.validators import MinValueValidator
from django.core.validators import RegexValidator
import math
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
    category_wraper = models.ForeignKey(CategoryWraper, models.SET_NULL, null=True, blank=True)
    display_wraper = models.ForeignKey(DisplayWraper, models.SET_NULL, null=True, blank=True)
    def __str__(self):
        return str(self.title)

class Product(models.Model):
    title = models.CharField(max_length=100)
    product_image = models.ImageField(upload_to = 'product_image')
    product_category = models.ForeignKey(Category, models.SET_NULL, blank = True, null=True)
    selling_prize =models.FloatField()
    discounted_prize = models.FloatField()
    description = models.TextField()
    brand = models.CharField(max_length=100, null=True, blank=True)
    display_wraper = models.ForeignKey(DisplayWraper, models.SET_NULL, null=True, blank=True)   
    discount = models.FloatField(null=True, blank=True)
    sell_amount= models.IntegerField(null=True, blank=True)
    def __str__(self):
        return str(self.title)
    UnitGroup_Choices = (
                        ("SolidWeight", "SolidWeight"),
                        ("LiquidWeight", "LiquidWeight"),
                        ("KgPacket", "KgPacket"),
                        ("LiterPacket", "LiterPacket"),
                        ("ClothSize", "ClothSize"),
                        ("ClothPicesSize", "ClothPicesSize"),
                        ("ShoeSize", "ShoeSize"),
                        ("Packet", "Packet")
                      )
    Unit_Choices = (
                        ("Kg", "Kg"),
                        ("Gram", "Gram"),
                        ("Pound", "Pound"),
                        ("Liter", "Liter"),
                        ("MiliLiter", "MiliLiter")
                      )
    unitGroup = models.CharField(max_length=30, choices = UnitGroup_Choices, null = True, blank = True)
    unit = models.CharField(max_length=30, choices= Unit_Choices, null=True, blank = True)
    unitValue_On_Increase_or_Decrease = models.IntegerField(null = True, blank = True)
    MinimumUnitValue = models.IntegerField(null = True, blank = True)
    MaximumUnitValue = models.IntegerField(null = True, blank = True)
    ProductStock = models.IntegerField(null = True)
    
    def save(self, *args, **kwargs):
        prizeGap =  self.selling_prize - self.discounted_prize
        sellingPrizePercent = self.selling_prize / 100 
        PrizeGapPercent = prizeGap / sellingPrizePercent 
        self.discount = round(PrizeGapPercent, 2)
        super().save(*args, **kwargs) 
   
class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(0)],  default = 1)
    unit = models.CharField(max_length = 30,  default = "none")
    unit_amount = models.FloatField( default=0)
    color = models.CharField(max_length = 30,  default = "none")
    size  = models.CharField(max_length = 40,  default = "none")
  
    def __str__(self):
        return str(self.id)
    
    @property
    def products_total_selling_cost(self):
         # <---This is for the product of having Kg or Liter or Area Unit--->
        if self.product.unitGroup == "SolidWeight" or self.product.unitGroup == "LiquidWeight" or self.product.unitGroup == "ClothPicesSize":
            if self.unit == "Gram" or self.unit == "MiliLiter":
                # Adjusting the prize according to the absolute unit....
                converted_amount = self.unit_amount * 0.001
            elif self.unit == "Pound":
                converted_amount = self.unit_amount * 0.45359237
            elif self.unit == "SqureYeard":
                converted_amount = self.unit_amount * 0.83612736
        # Keeping the Liter and Kg the unit of weight.....
            elif self.unit == "Kg" or self.unit == "Liter" or self.unit == "SqureMeter":
                converted_amount = self.unit_amount
            Total_Cost = self.quantity * self.product.selling_prize * converted_amount     
        # For the products which doesn't have the extra unit option....
        if self.product.unitGroup == "ClothSize" or self.product.unitGroup == "Packet" or self.product.unitGroup == "ShoeSize":
            Total_Cost = self.quantity * self.product.selling_prize        
        return Total_Cost

    @property
    def products_total_cost(self):
        # <---This is for the product of having Kg or Liter or Area Unit--->
        if self.product.unitGroup == "SolidWeight" or self.product.unitGroup == "LiquidWeight" or self.product.unitGroup == "ClothPicesSize":
            if self.unit == "Gram" or self.unit == "MiliLiter":
                # Adjusting the prize according to the absolute unit....
                converted_amount = self.unit_amount * 0.001
            elif self.unit == "Pound":
                converted_amount = self.unit_amount * 0.45359237
            elif self.unit == "SqureYeard":
                converted_amount = self.unit_amount * 0.83612736
        # Keeping the Liter and Kg the unit of weight.....
            elif self.unit == "Kg" or self.unit == "Liter" or self.unit == "SqureMeter":
                converted_amount = self.unit_amount
            Total_Cost = round(self.quantity * self.product.discounted_prize * converted_amount)  
        # For the products which doesn't have the extra unit option....
        if self.product.unitGroup == "ClothSize" or self.product.unitGroup == "Packet" or self.product.unitGroup == "ShoeSize":
            Total_Cost = self.quantity * self.product.discounted_prize
        return Total_Cost
    
# Account Related Models...
GENDER_CHOICES = (
    ("Male", "Male"),
    ("Female", "Female"),
    ("Others", "Others")
)
class CustomerProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
    email = models.EmailField( null = True, blank=True)
    full_name = models.CharField(max_length= 20 ,null=True)
    phone_reg = RegexValidator(regex=r'^\+?1?\d{9,15}$', message = "phone_number must be entered in the format: ' +99999999'. Up to 15 digits allowed")
    phone_number =  models.CharField(validators = [phone_reg], max_length = 16, unique=True)
    birthdate = models.DateField( null = True, blank = True)
    gender = models.CharField(choices=GENDER_CHOICES, max_length=10, null = True, blank = True)
    image = models.ImageField(upload_to = 'customerimages', null = True, blank = True)

# These model is for all the location information of bangladash....
class Divisions(models.Model):
    name = models.CharField(max_length = 25)
    bn_name = models.CharField(max_length = 25)
    url = models.CharField(max_length = 50)
    def __str__(self):
        return self.name

class Districts(models.Model):
    division_id = models.IntegerField()
    name = models.CharField(max_length=40)
    bn_name = models.CharField(max_length= 25, null=True)
    lat = models.CharField(max_length = 15, null=True)
    lon = models.CharField(max_length = 15, null = True)
    url = models.CharField(max_length=50, null=True)
    def __str__(self):
        return self.name

class Upazilas(models.Model):
    district_id = models.IntegerField()
    name = models.CharField(max_length = 25)
    bn_name = models.CharField(max_length = 25)
    url  = models.CharField(max_length = 50)
    def __str__(self):
        return self.name

class Unions(models.Model):
    upazilla_id = models.IntegerField()
    name  = models.CharField(max_length= 25)
    bn_name = models.CharField(max_length = 25)
    url = models.CharField(max_length = 50)
    def __str__(self):
        return self.name

class CustomerAddress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, null = True)
    full_name = models.CharField(max_length = 20)
    phone_reg = RegexValidator(regex=r'^\+?1?\d{9,15}$', message = "phone_number must be entered in the format: ' +99999999'. Up to 15 digits allowed")
    phone_number =  models.CharField(validators = [phone_reg], max_length = 16)
    divisions = models.ForeignKey(Divisions, on_delete=models.CASCADE)
    districts = models.ForeignKey(Districts, on_delete=models.CASCADE)
    upazilas = models.ForeignKey(Upazilas, on_delete=models.CASCADE)
    unions = models.ForeignKey(Unions, on_delete=models.CASCADE)
    address = models.CharField(max_length = 100)
    isDefault = models.BooleanField(null = True, blank = True, default = False)

STATUS_CHOICE = (
    ('Accepted', 'Accepted'),
    ('Packed', 'Packed'),
    ('On the Way', 'On the Way'),
    ('Delivered', 'Delivered'),
    ('Cencel', 'Cencel'),
    ('Pending', 'pending'),
)

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    profile = models.ForeignKey(CustomerProfile, models.SET_NULL, null=True)
    address = models.ForeignKey(CustomerAddress, models.SET_NULL, null=True)
    product = models.ForeignKey(Product, models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField(default = 1)
    unit = models.CharField(max_length=20)
    unitAmount = models.FloatField()
    size = models.CharField(max_length=20)
    subTotal = models.FloatField()
    Total = models.FloatField()
    discount = models.FloatField(null=True)
    ordered_date = models.DateTimeField(auto_now_add = True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICE, default='Pending')
