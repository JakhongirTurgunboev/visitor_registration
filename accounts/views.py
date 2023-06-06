from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import NewUserForm, ReservationForm, BuildingForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Reservation, Building


def homepage(request):
	if request.user.is_authenticated:
		if request.user.is_superuser:
			if request.method == 'POST':
				for k, v in request.POST.items():
					if "accept" in k:
						r = Reservation.objects.get(id=int(v))
						r.status = 1
						r.save()
					elif "reject" in k:
						r = Reservation.objects.get(id=int(v))
						r.status = -1
						r.save()
			reservations = Reservation.objects.all()
			return render(request, "main/visitor_check.html", context={"reservations": reservations})

		else:
			if request.method=='POST':
				form = ReservationForm(request.POST)
				if form.is_valid():
					form = form.save(commit=True)
					form.user = request.user
					form.save()
					messages.success(request, "Reservation successful.")
				else:
					messages.error(request, "Unsuccessful reservation.")
			form = ReservationForm()
			reservations = Reservation.objects.filter(user=request.user)
			return render(request, "main/visitor.html", context={"reservation_form": form, "reservations": reservations})
	else:
		return redirect("login")


def register_request(request):
	if request.method == "POST":
		form = NewUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			messages.success(request, "Registration successful." )
			return redirect("/login")
		messages.error(request, "Unsuccessful registration. Invalid information.")
	form = NewUserForm()
	return render(request=request, template_name="main/register.html", context={"register_form":form})


def login_request(request):
	if request.method == "POST":
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				messages.info(request, f"You are now logged in as {username}.")
				return redirect("/")
			else:
				messages.error(request,"Invalid username or password.")
		else:
			messages.error(request,"Invalid username or password.")
	form = AuthenticationForm()
	return render(request=request, template_name="main/login.html", context={"login_form":form})


def logout_request(request):
	logout(request)
	messages.info(request, "You have successfully logged out.")
	return redirect("homepage")


@login_required
def buildings(request):
	if request.user.is_superuser:
		if request.method == 'POST':
			form = BuildingForm(request.POST)
			if form.is_valid():
				building = form.save(commit=True)
				building.save()
				messages.success(request, "Building successful.")
			else:
				messages.error(request, "Can't add building.")
	form = BuildingForm()
	buildings = Building.objects.all()
	return render(request, "main/buildings.html", context={"building_form": form,
															   "buildings": buildings})