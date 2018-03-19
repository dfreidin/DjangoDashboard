# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
import bcrypt

# Create your views here.
def index(request):
    return render(request, "user_dashboard/index.html")

def signin(request):
    form = LoginForm()
    return render(request, "user_dashboard/signin.html", {"form": form})

def register(request):
    form = RegistrationForm()
    return render(request, "user_dashboard/register.html", {"form": form})

def login(request):
    if request.method != "POST":
        return redirect(dashboard)
    form = LoginForm(request.POST)
    if form.is_valid():
        users = User.objects.filter(email=form.cleaned_data["email"])
        if len(users) < 1:
            messages.error(request, "Email or password is incorrect")
            return redirect(signin)
        user = users[0]
        pw = form.cleaned_data["password"]
        if bcrypt.checkpw(pw.encode(), user.password.encode()):
            request.session["user_id"] = user.id
            return redirect(dashboard)
    return redirect(signin)

def new(request):
    if not "user_id" in request.session:
        return redirect(signin)
    current_user = User.objects.get(id=request.session["user_id"])
    if current_user.user_level != 9:
        return redirect(dashboard)
    form = RegistrationForm()
    return render(request, "user_dashboard/new.html", {"form": form, "id": current_user.id})

def dashboard(request):
    if not "user_id" in request.session:
        return redirect(signin)
    current_user = User.objects.get(id=request.session["user_id"])
    if current_user.user_level == 9:
        return redirect(adminDashboard)
    users = User.objects.all()
    return render(request, "user_dashboard/dashboard.html", {"users": users, "id": current_user.id, "admin": False})

def adminDashboard(request):
    if not "user_id" in request.session:
        return redirect(signin)
    current_user = User.objects.get(id=request.session["user_id"])
    if current_user.user_level != 9:
        return redirect(dashboard)
    users = User.objects.all()
    return render(request, "user_dashboard/dashboard.html", {"users": users, "id": current_user.id, "admin": True})

def editSelf(request):
    if not "user_id" in request.session:
        return redirect(signin)
    user = User.objects.get(id=request.session["user_id"])
    initial_data = {
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name
    }
    edit_form = EditForm(initial=initial_data)
    pass_form = PassChangeForm()
    desc_form = DescriptionForm(initial={"description": user.description})
    return render(request, "user_dashboard/edit.html", {"user": user, "eform": edit_form, "pform": pass_form, "dform": desc_form, "admin": False})

def editUser(request, id):
    if not "user_id" in request.session:
        return redirect(signin)
    current_user = User.objects.get(id=request.session["user_id"])
    if current_user.user_level != 9:
        return redirect(dashboard)
    users = User.objects.filter(id=id)
    if len(users) < 1:
        messages.error("No such user found")
        return redirect(adminDashboard)
    target_user = users[0]
    initial_data = {
        "email": target_user.email,
        "first_name": target_user.first_name,
        "last_name": target_user.last_name,
        "user_level": target_user.user_level
    }
    edit_form = AdminEditForm(initial=initial_data)
    pass_form = PassChangeForm()
    return render(request, "user_dashboard/edit.html", {"user": target_user, "eform": edit_form, "pform": pass_form, "id": current_user.id, "admin": True})

def show(request, id):
    if not "user_id" in request.session:
        return redirect(signin)
    users = User.objects.filter(id=id)
    if len(users) < 1:
        messages.error(request, "No such user found")
        return redirect(dashboard)
    target_user = users[0]
    c_form = CommentForm()
    m_form = MessageForm()
    return render(request, "user_dashboard/show.html", {"user": target_user, "m_form": m_form, "c_form": c_form, "id": request.session["user_id"]})

def createUser(request, login=None):
    if request.method != "POST":
        return redirect(dashboard)
    form = RegistrationForm(request.POST)
    if form.is_valid():
        new_user = form.save(commit=False)
        if len(User.objects.all()) < 1:
            new_user.user_level = 9
        else:
            new_user.user_level = 1
        new_user.password = bcrypt.hashpw(form.cleaned_data["password"].encode(), bcrypt.gensalt())
        new_user.save()
        if login == "reg":
            request.session["user_id"] = new_user.id
    return redirect(dashboard)

def logout(request):
    request.session.flush()
    return redirect(signin)

def remove(request, id):
    if not "user_id" in request.session:
        return redirect(signin)
    current_user = User.objects.get(id=request.session["user_id"])
    if current_user.user_level != 9:
        return redirect(dashboard)
    users = User.objects.filter(id=id)
    if len(users) < 1:
        messages.error("No such user found")
        return redirect(dashboard)
    users[0].delete()
    return redirect(adminDashboard)

def addMessage(request, id):
    if not "user_id" in request.session:
        return redirect(signin)
    if request.method != "POST":
        return redirect(dashboard)
    form = MessageForm(request.POST)
    if form.is_valid():
        new_msg = form.save(commit=False)
        new_msg.poster = User.objects.get(id=request.session["user_id"])
        new_msg.posted_to = User.objects.get(id=id)
        new_msg.save()
    return redirect(show, id=id)

def addComment(request, msg_id, usr_id):
    if not "user_id" in request.session:
        return redirect(signin)
    if request.method != "POST":
        return redirect(dashboard)
    form = CommentForm(request.POST)
    if form.is_valid():
        new_cmt = form.save(commit=False)
        new_cmt.poster = User.objects.get(id=request.session["user_id"])
        new_cmt.message = Message.objects.get(id=msg_id)
        new_cmt.save()
    return redirect(show, id=usr_id)

def updateForm(request, id, FormClass, auth_condition):
    if not "user_id" in request.session:
        return redirect(signin)
    if request.method != "POST":
        return redirect(show, id=id)
    current_user = User.objects.get(id=request.session["user_id"])
    if auth_condition(current_user, id):
        return redirect(show, id=id)
    form = FormClass(request.POST, instance=User.objects.get(id=id))
    if form.is_valid():
        new_user = form.save(commit=False)
        if FormClass == PassChangeForm:
            new_user.password = bcrypt.hashpw(form.cleaned_data["password"].encode(), bcrypt.gensalt())
        new_user.save()
    return redirect(show, id=id)

def updateInfo(request, id):
    direction = updateForm(request, id, EditForm, lambda cu, id: str(cu.id) != str(id))
    return direction

def adminUpdateInfo(request, id):
    direction = updateForm(request, id, AdminEditForm, lambda cu, id: cu.user_level != 9)
    return direction

def updatePassword(request, id):
    direction = updateForm(request, id, PassChangeForm, lambda cu, id: str(cu.id) != str(id) and cu.user_level != 9)
    return direction
    
def updateDescription(request, id):
    direction = updateForm(request, id, DescriptionForm, lambda cu, id: str(cu.id) != str(id))
    return direction