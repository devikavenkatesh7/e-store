from django.contrib.auth.models import User
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import PROTECT, CASCADE


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='profile_pics/', blank=True)
    dob = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10,
                              choices=[
                                  ('M', 'Male'), ('F', 'Female'), ('O', 'Other')
                              ], blank=True)
    place = models.CharField(max_length=100, blank=True)
    recovery_email = models.EmailField(blank=True)
    mobile_number = models.CharField(max_length=15, blank=True,
                                     validators=[RegexValidator
                                                 (r'^[6-9]\d{9}$', 'Invalid Indian mobile number')])

    def __str__(self):
        return self.user.username

class Location(models.Model):
    user = models.ForeignKey(to=User, on_delete=CASCADE, null=True, blank=False,related_name='locations')
    phone = models.CharField(validators=[RegexValidator("^[6-9]{1}\d{9}$")], max_length=15)
    address = models.TextField()
    landmark = models.CharField(max_length=45, null=True, blank=True)
    city = models.CharField(max_length=45)
    pincode = models.IntegerField(validators=[MinValueValidator(111111), MaxValueValidator(999999)])
    state = models.CharField(max_length=45)

    def __str__(self):
        return "%s(%s, %s, %s - %s)" % (self.user, self.address, self.city, self.state, self.state)


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    brand = models.CharField(max_length=45)
    price = models.FloatField(validators=(MinValueValidator(99), MaxValueValidator(9999999)))
    in_stock = models.IntegerField(default=0)
    color = models.CharField(max_length=45)
    size = models.CharField(max_length=5, choices=(('XL', 'XL'), ('L', 'L'), ('XXL', 'XXL'), ('M', 'M'), ('S', 'S')))
    image = models.ImageField(upload_to='uploads/%Y/%M/%D')
    created_date = models.DateTimeField(auto_now_add=True)
    added_by = models.ForeignKey(to=User, on_delete=PROTECT)

    def __str__(self):
        return f"{self.name}(price : {self.price}, brand: {self.brand}, in-stock : {self.in_stock})"


class Review(models.Model):
    product = models.ForeignKey(to=Product, on_delete=CASCADE)
    user = models.ForeignKey(to=User, on_delete=CASCADE)
    rating = models.FloatField(validators=(MinValueValidator(1), MaxValueValidator(5)))
    comments = models.TextField()

    def __str__(self):
        return "%s - %s - %s" % (self.product, self.user, self.rating)


class Cart(models.Model):
    user = models.ForeignKey(to=User, on_delete=PROTECT)
    product = models.ForeignKey(to=Product, on_delete=PROTECT)
    quantity = models.IntegerField(default=1)
    is_purchased = models.BooleanField(default=False)

    def __str__(self):
        return "%s - %s - %s" % (self.product, self.quantity, self.is_purchased)


class Order(models.Model):
    ordered_by = models.ForeignKey(to=User, on_delete=PROTECT)
    ordered_items = models.JSONField()
    total_price = models.FloatField()
    delivery_address = models.ForeignKey(to=Location, on_delete=PROTECT)
    status = models.CharField(default='ordered', max_length=25)
    ordered_date = models.DateTimeField(auto_now_add=True)


class OrderHistory(models.Model):
    order = models.JSONField()
    user = models.ForeignKey(to=User, on_delete=PROTECT)