from django.forms import *
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

class FormRekap(forms.Form):
	BULAN =( 
	('', '----------'),
	("1", "Januari"), 
	("2", "Februari"), 
	("3", "Maret"), 
	("4", "April"), 
	("5", "Mei"), 
	("6", "Juni"), 
	("7", "Juli"), 
	("8", "Agustus"), 
	("9", "September"), 
	("10", "Oktober"), 
	("11", "November"), 
	("12", "Desember"),)

	TAHUN=(
	('', '----------'),
	("2020", "2020"),
	("2021", "2021"),
	("2022", "2022"),
	("2023", "2023"),
	("2024", "2024"),
	("2025", "2025"),)

	STATUS=(
		('', '----------'),
		("Keluar", "Keluar"),
		("Masuk", "Masuk")) 

	bulan = forms.ChoiceField(choices=BULAN, required=False)
	tahun = forms.ChoiceField(choices=TAHUN, required=False)
	status = forms.ChoiceField(choices=STATUS, required=False)