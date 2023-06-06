from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Building, Reservation


# Create your forms here.


class NewUserForm(UserCreationForm):
	email = forms.EmailField(required=True)

	class Meta:
		model = User
		fields = ("username", "email", "password1", "password2")

	def save(self, commit=True):
		user = super(NewUserForm, self).save(commit=True)
		user.email = self.cleaned_data['email']
		if commit:
			user.save()
		return user


class ReservationForm(forms.ModelForm):
	class Meta:
		model = Reservation
		fields = ("building", "planned_date", "first_name", "last_name")
		widgets = {
			'planned_date': forms.widgets.DateInput(attrs={'type': 'date'})
		}


class BuildingForm(forms.ModelForm):
	class Meta:
		model = Building
		fields = ("name", "address")
