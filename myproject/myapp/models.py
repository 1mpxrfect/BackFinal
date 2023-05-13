from django.contrib.auth.models import User
from django.db import models
from django.contrib import auth


class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Products(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=26)
    price = models.IntegerField(null=True)
    date_created = models.DateTimeField(auto_now_add=True, blank=True)
    description = models.TextField(help_text='Description for this product', null=True)
    picture = models.ImageField(upload_to='media', blank=True)
    id = models.AutoField(primary_key=True)

    def __str__(self):
        return self.name


class Comment(models.Model):

    RATING = (
        ('Soo bad', 1),
        ('Badly', 2),
        ('Not bad', 3),
        ('Well', 4),
        ('Soo well', 5),
    )

    product = models.ForeignKey(Products, on_delete=models.CASCADE, related_name='product_comment')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_text = models.TextField(help_text='Write here')
    rating = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

# class Customer(models.Model):
#     first_name = models.CharField(max_length=50)
#     last_name = models.CharField(max_length=50)
#     email = models.EmailField(help_text='Email')
#     city = models.ForeignKey(City, on_delete=models.CASCADE)
#     phone_num = models.CharField(max_length=20)
#
#     def __str__(self):
#         return self.first_name
#
#
# class Order(models.Model):
#     customer_name = models.ForeignKey(Customer, on_delete=models.CASCADE)
#     date_ordered = models.DateTimeField(auto_now_add=True, blank=True)
#     product_name = models.ForeignKey(Products, on_delete=models.CASCADE)
#
#
