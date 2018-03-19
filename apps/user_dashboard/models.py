# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django import forms

# Create your models here.
class User(models.Model):
    email = models.EmailField()
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    USER_LEVEL_CHOICES = (
        (1, "normal"),
        (9, "admin")
    )
    user_level = models.IntegerField(choices=USER_LEVEL_CHOICES)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Message(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    poster = models.ForeignKey(User, related_name="messages")
    posted_to = models.ForeignKey(User, related_name="wall_messages")

class Comment(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    poster = models.ForeignKey(User, related_name="comments")
    message = models.ForeignKey(Message, related_name="comments")

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = [
            "email",
            "first_name",
            "last_name",
            "password"
        ]
    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        pw = cleaned_data.get("password")
        pc = cleaned_data.get("confirm_password")
        if pw != pc:
            raise forms.ValidationError("Password does not match")
        return cleaned_data

class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())

class EditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            "email",
            "first_name",
            "last_name"
        ]

class AdminEditForm(forms.ModelForm):
    user_level = forms.ChoiceField(choices=User.USER_LEVEL_CHOICES)
    class Meta:
        model = User
        fields = [
            "email",
            "first_name",
            "last_name",
            "user_level"
        ]

class PassChangeForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ["password"]
    def clean(self):
        cleaned_data = super(PassChangeForm, self).clean()
        pw = cleaned_data.get("password")
        pc = cleaned_data.get("confirm_password")
        if pw != pc:
            raise forms.ValidationError("Password does not match")
        return cleaned_data

class MessageForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea(attrs={"cols": "100", "rows": "4"}), label="")
    class Meta:
        model = Message
        fields = ["content"]

class CommentForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea(attrs={"cols": "100", "rows": "4"}), label="")
    class Meta:
        model = Comment
        fields = ["content"]

class DescriptionForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea(attrs={"cols": "100", "rows": "6"}), label="")
    class Meta:
        model = User
        fields = ["description"]