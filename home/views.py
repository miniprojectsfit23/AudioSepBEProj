from django.shortcuts import render
import numpy as np
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.contrib import messages
from .models import User, Song
from slugify import slugify
# Modules for Seperation
from mir_eval import separation
import subprocess
import os
import shutil
from pydub import AudioSegment
from pydub.silence import split_on_silence
# Create your views here.


def analyse(path):
    song = AudioSegment.from_wav(path)
    print("Processing: "+os.path.basename(path))
    audio_chunks = split_on_silence(
        song, min_silence_len=1, silence_thresh=-50, keep_silence=0)
    combined = AudioSegment.empty()
    for chunk in audio_chunks:
        combined += chunk
    return (combined.duration_seconds/song.duration_seconds)*100


def seperate(path):
    output = subprocess.run(
        "spleeter separate -o "+os.path.dirname(path)+" -p spleeter:5stems "+path, shell=True)
    print(output)
    directory = os.path.dirname(path)+"\\source\\"
    for file_name in os.listdir(directory):
        source = directory+file_name
        shutil.move(source, os.path.dirname(path))
    shutil.rmtree(directory)


def home(request):
    if request.method == "POST":
        name = request.POST.get("songName")
        file = request.FILES.get("songFile")
        if file is not None:
            url = slugify(name)
            while Song.objects.filter(url=url).exists():
                url = slugify(name)+str(np.random.randint(10000, 99999))
            if request.user.is_authenticated:
                user = request.user
                song = Song.objects.create(
                    url=url, name=name, user=user, upload=file)
            else:
                song = Song.objects.create(
                    url=url, name=name, user=None, upload=file)
            seperate(song.upload.path)
            song.vocals = round(analyse(os.path.dirname(
                song.upload.path)+"\\vocals.wav"), 2)
            song.bass = round(analyse(os.path.dirname(
                song.upload.path)+"\\bass.wav"), 2)
            song.drums = round(analyse(os.path.dirname(
                song.upload.path)+"\\drums.wav"), 2)
            song.piano = round(analyse(os.path.dirname(
                song.upload.path)+"\\piano.wav"), 2)
            song.save()
            messages.success(
                request, "Song Uploaded Successfully. Processing....")
            return redirect("/song/"+url)
        else:
            messages.error(
                request, "Please Upload a file before submitting.")
    response = render(request, "home/Home.html", {"title": "Seperate"})
    return response


def login(request):
    if request.user.is_authenticated:
        return redirect("home:home")
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect("home:home")
        else:
            messages.error(request, "Invalid Credentials.")
            return redirect("home:login")
    return render(request, "home/Login.html", {"title": "Login"})


def register(request):
    if request.user.is_authenticated:
        return redirect("home:home")
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirmPassword = request.POST.get("confirmPassword")
        print(username, email, password, confirmPassword)
        if password == confirmPassword:
            if User.objects.filter(username=username).exists():
                messages.error(
                    request, "This username already Exists. Please try a different username.")
                return render(request, "home/Register.html", {"title": "Register"})
            elif User.objects.filter(email=email).exists():
                messages.error(
                    request, "This email is already registered. Please try with a different email.")
                return render(request, "home/Register.html", {"title": "Register"})
            user = User.objects.create(
                username=username, email=email)
            user.set_password(password)
            user.save()
            messages.success(
                request, "Your Account has been created successfully.")
            return redirect("home:login")
        else:
            messages.error(
                request, "Password and Confirm Password do not match. Please try again.")
    return render(request, "home/Register.html", {"title": "Register"})


@login_required
def profile(request):
    songs = Song.objects.filter(user=request.user)
    return render(request, "home/Profile.html", {"title": "My Account", "songs": songs})


@login_required
def change_password(request):
    if request.method == "POST":
        oldPassword = request.POST.get("oldPassword")
        newPassword = request.POST.get("newPassword")
        confirmPassword = request.POST.get("confirmPassword")
        if request.user.check_password(oldPassword):
            if oldPassword != newPassword:
                if newPassword == confirmPassword:
                    request.user.set_password(newPassword)
                    request.user.save()
                    messages.success(
                        request, "Password Changed Successfully. Please login again.")
                    logout(request)
                    return redirect("home:login")
                else:
                    messages.error(
                        request, "New Password and Confirm Password do not match. Please try again.")
            else:
                messages.error(
                    request, "Old Password and New Password cannot be same. Please try again.")
        else:
            messages.error(
                request, "Old Password is incorrect. Please try again.")
    return render(request, "home/ChangePassword.html", {"title": "Change Password"})


@login_required
def song(request, url):
    song = Song.objects.get(url=url)
    path = os.path.dirname(str(song.upload))
    response = render(request, "home/Song.html",
                      {"title": "Song", "song": song, "path": path})
    response['Accept-Ranges'] = 'bytes'
    print(response['Accept-Ranges'])
    return response


@login_required
def delete_song(request, url):
    song = Song.objects.get(url=url)
    if request.user == song.user:
        song.delete()
        messages.success(request, "Song Deleted Successfully.")
    return redirect("home:profile")


@login_required
def edit_song(request, url):
    song = Song.objects.get(url=url)
    if request.method == "POST":
        name = request.POST.get("songName")
        song.name = name
        song.save()
        messages.success(request, "Song Updated Successfully.")
        return redirect("home:profile")
    return render(request, "home/EditSong.html", {"title": "Edit Song", "song": song})


@login_required
def delete_account(request):
    user = request.user
    user.delete()
    messages.success(request, "Account Deleted Successfully.")
    return redirect("home:login")


@login_required
def logout_view(request):
    logout(request)
    return redirect('home:home')
