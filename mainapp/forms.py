from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

from .models import *

class FormTransaksi(ModelForm):
	class Meta:
		model = Transaksi
		fields = '__all__'

class FormBarang(ModelForm):
	class Meta:
		model = Barang
		fields = '__all__'

class FormEditBarang(ModelForm):
	pk = forms.IntegerField()
	class Meta:
		model = Barang
		fields = '__all__'

class FormKategori(ModelForm):
	class Meta:
		model = Kategori
		fields = '__all__'

class FormEditKategori(ModelForm):
	pk = forms.IntegerField()
	class Meta:
		model = Kategori
		fields = '__all__'

class CreateUserForm(UserCreationForm):
	class Meta:
		model = User
		fields = ['username', 'email', 'password1', 'password2']