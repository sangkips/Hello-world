from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField

# Here are my models
""" Abstract User """
class User(AbstractUser):
    email = models.EmailField(unique=True, max_length=50)
    phone_number = PhoneNumberField(blank=True, help_text='Contact phone number', null=True)
    verification_code = models.CharField(max_length=100, blank=True)
   
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'username', 'phone_number'] # add phone number as a requirement while signing up

    def __str__(self) -> str:
        return f'{self.first_name} {self.last_name}'
        

""" User Accounts """
class Account(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)#Referencing the customized user
    alias = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    display_picture = models.ImageField(blank=True, null=True)
    bio = models.TextField(blank=True, null=True)

    def __str__(self) -> str:
        return self.alias

""" Stori_category """
class Stori_category(models.Model):
    category = models.CharField(max_length=100)
    about = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f'{self.category}: {self.about}'

    class Meta:
        verbose_name_plural = "Categories"

""" Stori """
class Stori(models.Model): #stori is swahili for story. was thinking of get the slang version 'risto'/'riba' in there..
    title = models.CharField(max_length=50)
    stori = models.CharField(max_length=280)#Using 280 here since its twitter's max characters for a single tweet 
    description = models.CharField(max_length=100, blank=True)
    created_by = models.ForeignKey(Account, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(Stori_category, on_delete=models.CASCADE)

    def __str__(self):
         return f'{self.title} created by: {self.created_by}'
    
    class Meta:
        verbose_name_plural = "Mastori"

""" Stori_comments """
class Stori_comment(models.Model):
    stori = models.ForeignKey(Stori, related_name='mastori', on_delete=models.CASCADE)
    reaction_by = models.ForeignKey(Account, on_delete=models.CASCADE)
    comment = models.CharField(max_length=100)
    
    def __str__(self):
        return f'{self.reaction_by} commented on: {self.stori.title} with: {self.comment}'

""" Reaction_choice """
class Reaction_choice(models.Model):
    reaction_choice = models.CharField(max_length=50)

    def __str__(self):
        return self.reaction_choice

""" Stori_reactions """        
class Stori_reaction(models.Model):
    stori = models.ForeignKey(Stori,  on_delete=models.CASCADE)
    reaction_by = models.ForeignKey(Account, on_delete=models.CASCADE)
    reaction = models.ForeignKey(Reaction_choice, on_delete=models.CASCADE)# Do I realy have to keep this here?

    def __str__(self):
        return f'{self.reaction_by} reacted with a  {self.reaction} on {self.stori.title} by {self.stori.created_by}'

    class Meta:
        unique_together = ("stori", "reaction_by")

""" Comment Reactions """
class Comment_reaction(models.Model):
    comment = models.ForeignKey(Stori_comment, related_name='comments', on_delete=models.CASCADE)
    reaction_by = models.ForeignKey(Account, on_delete=models.CASCADE)
    reaction = models.ForeignKey(Reaction_choice, on_delete=models.CASCADE)# Do I realy have to keep this here?

    def __str__(self):
        return f'{self.reaction_by} reacted with a {self.reaction} on {self.comment.comment} '

    class Meta:
        unique_together = ("comment", "reaction_by")

