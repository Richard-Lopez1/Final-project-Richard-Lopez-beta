from django.db import models
from datetime import datetime

# Create your models here.
import re
import bcrypt
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
class UserManager(models.Manager):
    def validate(self, form):
        errors = {}
        if len(form['first_name']) < 2:
            errors['first_name'] = 'First name must be at least 2 characters'

        if len(form['last_name']) < 2:
            errors['last_name'] = 'Last name must be at least 2 characters'

        # test if the email_regex field matches the pattern, if not send Invalid email address.
        if not EMAIL_REGEX.match(form['email']):
            errors['email'] = 'Invalid email address'
        
        email_check = self.filter(email=form['email'])
        if email_check:
            errors['email'] = "Email already in use"

        if len(form['password']) < 8:
            errors['password'] = 'Password must be at least 8 characters'
        
        # confirm email check routine
        if form['password'] != form['confirm']:
            errors['password'] = 'Passwords do not match'
        
        return errors
    
    def authenticate(self, email, password):
        users = self.filter(email=email)
        if not users:
            return False

        user = users[0]
        return bcrypt.checkpw(password.encode(), user.password.encode())

    def register(self, form):
        pw = bcrypt.hashpw(form['password'].encode(), bcrypt.gensalt()).decode()
        return self.create(
            first_name = form['first_name'],
            last_name = form['last_name'],
            email = form['email'],
            password = pw,
        )
        
# Create your models here.
# creating a user in the database
class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)

    # the line below gives the user class access to the validate method
    objects = UserManager()

# start of stock monitor program

class StockManager(models.Manager):
    def validate(self, form):
        errors = {}
        if len(form['title']) < 2:
            errors['title'] = 'Stock field should be at least 2 characters'
        if len(form['network']) < 3:
            errors['network'] = 'Stock symbol should be at least 3 characters'
        if form['description'] != '' and len(form['description']) < 10:
            errors['description'] = 'Description should be at least 10 characters'
        if datetime.strptime(form['release_date'], '%Y-%m-%d') > datetime.now():
            errors['release_date'] = 'Purchase Date should be in the past'
        return errors

# Create your models here.
class Stock(models.Model):
    title = models.CharField(max_length=255)
    network = models.CharField(max_length=45)
    release_date = models.DateTimeField()
    description = models.CharField(max_length=255)
    user_likes = models.ManyToManyField(User, related_name='liked_stocks')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = StockManager()

# class Like(models.Model):
#     message = models.CharField(max_length=255)
#     user_likes = models.ManyToManyField(Stock, related_name='liked_posts')
