from datetime import date
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

#  FOOD = 1
# FURNITURE = 3
# CLOTHING = 4
# ELECTRONICES = 5

# PRPDUCT_CATEGORT = [
#     (FOOD, 'food'),
#     (FURNITURE, 'Furniture'),
#     (CLOTHING, 'Clothing'),
#     (ELECTRONICES, 'Electronices'),
# ]
# ACTIVE = 1
# BLOCKED = 2
# CUSTOMER_STATUS = [
#     (ACTIVE, 'Active'),
#     (BLOCKED, 'Block')
# ]
# class ShopKeeper(models.Model):
#     name = models.CharField(max_length=100)
#     address = models.CharField(max_length=200, null=True, default=True)
#     phone = models.CharField(max_length=50)
    
# class Shop(models.Model):
#     name = models.CharField(max_length=100)
#     address = models.CharField(max_length=200)
#     shop_keeper = models.ForeignKey(ShopKeeper,related_name='shop_keeper', on_delete=models.CASCADE)
    
# class Products(models.Model):
#     title = models.CharField(max_length=200)
#     category = models.SmallIntegerField(choices=PRPDUCT_CATEGORT, default=FOOD)
#     price = models.PositiveIntegerField()
#     shop = models.ManyToManyField(Shop,related_name='products')

# class Customer(models.Model):
#     name = models.CharField(max_length=100)
#     phone = models.CharField(max_length=50)

# @receiver(post_save, sender=Customer)
# def video_comment_count(sender, instance, created, **kwargs):
#     if created:
#         CustomerActivitys.objects.create(customer=instance)

# class CustomerActivitys(models.Model):
#     customer = models.OneToOneField(Customer,related_name='customer_activity', on_delete=models.CASCADE) 
#     total_pay = models.PositiveIntegerField(null=True,blank=True,default=0)
#     due_amount = models.PositiveIntegerField(null=True,blank=True,default=0)
#     status = models.SmallIntegerField(choices=CUSTOMER_STATUS, default=ACTIVE)

#     # @Property
#     # def customer_details(self):
#     #    return '{} {}'.format(self.due_amount, self.return_amount)
    
#     # @customer_details.setter
#     # def calculate(self,amount):
#     #     total_price, recive_amount = int(amount.split(' '))
#     #     if total_price <= recive_amount:
#     #         self.total_pay += total_price
#     #         self.return_amount = recive_amount - total_price
#     #     else:
#     #         self.due_amount = total_price - recive_amount
#     #         self.total_pay += recive_amount
#     #         self.return_amount = 0

# class ShoppingDetails(models.Model):
#     customer_activitys = models.ForeignKey(CustomerActivitys, related_name='shopping_details', on_delete=models.CASCADE)
#     product = models.ManyToManyField(Products, related_name='shopping_details')
#     date = models.DateField(auto_now_add=True)







#---------------------------------------------------------------------------------------------------#


















class Teacher(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=500, null=True, blank=True)
    phone = models.CharField(max_length=20)

    def __str__(self) -> str:
        return self.name

class Student(models.Model):
    name = models.CharField(max_length=100)
    student_id = models.CharField(max_length=20, unique=True)

    def __str__(self) -> str:
        return self.name

class Course(models.Model):
    title = models.CharField(max_length=250)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    exam_date = models.DateField()
    def __str__(self) -> str:
        return self.title

class Enrollmet(models.Model):
    student = models.ForeignKey(Student,on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollment')
    result = models.CharField(max_length=20,blank=True,null=True)
    date = models.DateField(auto_now_add=True)

class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course,related_name='attendance', on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    attend = models.BooleanField(default=False)

    def __str__(self) -> str:
        return '{}, {}'.format(self.course, self.date)


   

class Quiz(models.Model):
    question = models.CharField(max_length=200,null=True)
    option_1 = models.CharField(max_length=200,null=True)
    option_2 = models.CharField(max_length=200,null=True)
    option_3 = models.CharField(max_length=200,null=True)
    option_4 = models.CharField(max_length=200,null=True)
    answer = models.CharField(max_length=200,null=True)
    
class Questions(models.Model):
    course = models.ForeignKey(Course,related_name='questions', on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, related_name='questions', on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    


    
