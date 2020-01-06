from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db.models.signals import post_save
from django.dispatch import receiver 


class Product(models.Model):
	CATEGORY = (
		("Fruit", "Fruit"),
		("Vegetable", "Vegetable")
	)
	name=models.CharField(max_length=120)
	price=models.DecimalField(max_digits=6, decimal_places=3, validators=[MinValueValidator(0.0)])
	img=models.ImageField()
	stock=models.PositiveIntegerField()
	description=models.TextField()
	active=models.BooleanField(default=True)
	date_added=models.DateField(auto_now=True)
	origin = models.ForeignKey("Origin", null=True, related_name="products", on_delete=models.SET_NULL)
	category = models.CharField(choices=CATEGORY, max_length=50, null=True, blank=True)

	def __str__ (self):
		return self.name

class Origin(models.Model):
	country = models.CharField(max_length=100)

	def __str__(self):
		return self.country


class Profile(models.Model):
	GENDER = (
		("F", "Female"),
		("M", "Male")
	)
	user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
	phone = models.PositiveIntegerField(null=True)
	gender = models.CharField(choices=GENDER, max_length=2, null=True)
	age = models.PositiveIntegerField(null=True)
	image = models.ImageField(null=True)


	def __str__(self):
		return self.user.username

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user= instance)

class Address(models.Model):
	profile = models.ForeignKey("Profile",on_delete=models.CASCADE, null=True, blank=True, related_name='addresses')
	name = models.CharField(max_length=150, default="Home")
	area = models.CharField(max_length=150)
	street = models.CharField(max_length=200)
	block = models.CharField(max_length=50)
	building_number = models.CharField(max_length=50)
	optional = models.CharField(max_length=200)

class Order(models.Model):
	order_ref = models.CharField(max_length=10)
	address =models.ForeignKey(Address, on_delete=models.CASCADE, related_name='address')
	customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
	date_time = models.DateTimeField(auto_now_add=True)
	total = models.DecimalField(max_digits=8, decimal_places=3, validators=[MinValueValidator(0.0)])


class Basket(models.Model):
	product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='products')
	quantity = models.PositiveIntegerField()
	order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='baskets')

@receiver(post_save, sender=Basket)
def reduce_inventory(instance, created, **kwargs):
	if created:
		product = Product.objects.get(id=instance.product.id)
		product.stock -= instance.quantity
		product.save()
