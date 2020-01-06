from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Product, Profile, Basket, Order, Address
from .base64 import decode_base64


class UserCreateSerializer(serializers.ModelSerializer):
	password = serializers.CharField(write_only=True)
	class Meta:
		model = User
		fields = ['username', 'password']

	def create(self, validated_data):
		new_user = User(**validated_data)
		new_user.set_password(validated_data['password'])
		new_user.save()
		return validated_data


class ProductsListSerializer(serializers.ModelSerializer):
	country = serializers.SerializerMethodField()

	class Meta:
		model = Product
		fields = ["id","name", "price", "img","stock", "date_added","country"]
	def get_country(self, obj):
		return "%s"%(obj.origin.country)	

class ProductHistorySerializer(serializers.ModelSerializer):
	class Meta:
		model = Product
		fields = ['name', 'price']

class ProductDetailsSerializer(serializers.ModelSerializer):
	country = serializers.SerializerMethodField()

	class Meta:
		model = Product
		fields = ["id","name", "price", "img","stock", "description", "date_added", "country"]

	def get_country(self, obj):
		return "%s"%(obj.origin.country)
		
class AddressSerializer(serializers.ModelSerializer):
	class Meta:
		model= Address
		fields = "__all__"

class UserSerializer(serializers.ModelSerializer):

	class Meta:
		model = User
		fields = ["username", "first_name", "last_name", "email"]
		read_only_fields = ['username']


class UpdateProfileSerializer(serializers.ModelSerializer):
	user = UserSerializer()
	addresses = serializers.SerializerMethodField()
	order_history = serializers.SerializerMethodField()


	class Meta:
		model = Profile
		fields = ["user","phone","gender","age", "order_history", "addresses"]

	def update(self, instance, validated_data):
		"""
		removing (user) key from validated_data dictionary to use update the
		user which has read only username field
		"""
		user_field = validated_data.pop('user', None)
		temp_user_serializer = UserSerializer()
		# profile_image = validated_data['image']
		# instance.image = decode_base64(profile_image)
		# instance.save()
		super().update(instance, validated_data)
		super(UserSerializer, temp_user_serializer).update(instance.user, user_field)
		return instance

	def get_addresses(self, obj):
		addresses = AddressSerializer(obj.addresses.all(), many=True) 
		return addresses.data

	def get_order_history(self, obj):
		orders = OrderSerializer(obj.user.orders.all().order_by('-date_time'), many=True)
		return orders.data


class BasketSerializer(serializers.ModelSerializer):
	product = ProductHistorySerializer()
	class Meta:
		model = Basket
		fields = '__all__'



class OrderSerializer(serializers.ModelSerializer):
	baskets= BasketSerializer(many=True)
	
	class Meta:
		model = Order
		fields = ["id", "order_ref", "customer", "address",  "baskets", "date_time", "total"]
		