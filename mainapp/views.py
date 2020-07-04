from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.contrib import messages
from django.db.models import signals
from django.db.models import Sum, Count, Q
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.forms import inlineformset_factory

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group

from .models import *
from .forms import *
from .filters import *
from .signals import *
from .decorators import unauthenticated_user, allowed_users

from datetime import date

def logoutUser(request):
	logout(request)
	return redirect('login')
	
@unauthenticated_user
def registerPage(request):

	form = CreateUserForm()
	if request.method == 'POST':
		form = CreateUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			username = form.cleaned_data.get('username')


			messages.success(request, 'Account was created for ' + username)

			return redirect('login')
		

	context = {'form':form}
	return render(request, 'admin/registerPage.html', context)


@unauthenticated_user
def loginPage(request):

	if request.method == 'POST':
		username = request.POST.get('username')
		password =request.POST.get('password')

		user = authenticate(request, username=username, password=password)

		if user is not None:
			login(request, user)
			return redirect('index')
		else:
			messages.info(request, 'Username OR password is incorrect')

	context = {}
	return render(request, 'admin/loginPage.html', context)


@login_required(login_url='login')
def index(request):
	# 'SELECT count(harga) FROM mainapp_rekaptransaksi GROUP BY idtrx'
	x = date.today()
	
	totalomset = RekapTransaksi.objects.filter(created_at__year=x.year, created_at__month=x.month, created_at__day=x.day).aggregate(Sum('total'))

	tottrans = RekapTransaksi.objects.values('idtrx').filter(created_at__year=x.year, created_at__month=x.month, created_at__day=x.day, status='Keluar').order_by('idtrx').annotate(Count('idtrx'))

	totprod = Barang.objects.all().count()

	totunt = RekapTransaksi.objects.filter(created_at__year=x.year, created_at__month=x.month, created_at__day=x.day, status='Keluar')

	most = RekapTransaksi.objects.values('barang__nama').filter(created_at__year=x.year, created_at__month=x.month, created_at__day=x.day, status='Keluar').annotate(dcount=Sum('qty')).order_by('-dcount')[:1]

	inout = RekapTransaksi.objects.values('barang__nama', 'barang__stok').filter(created_at__year=x.year, created_at__month=x.month, created_at__day=x.day).annotate(dcount=Sum('qty', filter=Q(status='Keluar'))).annotate(din=Sum('qty', filter=Q(status='Masuk')))

	
	# laris = []
	# for i in most:
	# 	x = i.dcount
	# 	laris.append(x)

	listunt = []

	tanggalprint = str(x.day)+ "-" +str(x.month)+ "-" +str(x.year)

	for i in totunt:
		jual = i.harga_jual * i.qty
		beli = i.harga_beli * i.qty
		untung = jual - beli
		listunt.append(untung)

	totaluntung = sum(listunt)

	context = {'act':'Dashboard', 'totalomset':totalomset, 'totprod':totprod, 'tottrans':tottrans, 'totaluntung':totaluntung, 'most':most, 'inout':inout, 'tanggalprint':tanggalprint}
	return render(request, 'admin/home.html', context)

################   BARANG   ######################


@login_required(login_url='login')
def PageBarang(request):
	dbarang = Barang.objects.all()
	form = FormBarang()
	formup = FormEditBarang()

	if request.method == 'POST':
		form = FormBarang(request.POST)
		if form.is_valid():
			form.save()
			return redirect('/barang/')
	
	context = {'dbarang': dbarang, 'act':'Barang', 'form':form, 'formup':formup}
	return render(request, 'admin/barang.html', context)

@login_required(login_url='login')
def deleteBarang(request, pk):
	dbarang = Barang.objects.get(id=pk)
	form = FormBarang()

	if request.method == 'POST':
		dbarang.delete()
		return redirect('barang')

@login_required(login_url='login')
def updateBarang(request):
	formup = FormEditBarang()

	if request.method =='POST':
		formup = FormEditBarang(request.POST)
		if formup.is_valid():
			idb = formup.cleaned_data['pk']
			nama = formup.cleaned_data['nama']
			kategori = formup.cleaned_data['kategori']
			stok = formup.cleaned_data['stok']
			harga_jual = formup.cleaned_data['harga_jual']
			harga_beli = formup.cleaned_data['harga_beli']
			
			Barang.objects.filter(id=idb).update(nama=nama, kategori=kategori, stok=stok, harga_jual=harga_jual, harga_beli=harga_beli)

			return redirect('barang')


#################### KATEGORI ########################
@login_required(login_url='login')
def PageKategori(request):
	dkategori = Kategori.objects.all()
	form = FormKategori()
	formup = FormEditKategori()

	if request.method == 'POST':
		form = FormKategori(request.POST)
		if form.is_valid():
			form.save()
			return redirect('/kategori/')

	context = {'dkategori': dkategori, 'act':'Kategori', 'form':form, 'formup':formup}
	return render(request, 'admin/kategori.html', context)


@login_required(login_url='login')
def deleteKategori(request, pk):
	dkategori = Kategori.objects.get(id=pk)
	form = FormKategori()

	if request.method == 'POST':
		dkategori.delete()
		return redirect('kategori')

@login_required(login_url='login')
def updateKategori(request):
	formup = FormEditKategori()

	if request.method =='POST':
		formup = FormEditKategori(request.POST)
		if formup.is_valid():
			idk = formup.cleaned_data['pk']
			nama = formup.cleaned_data['nama']
			
			Kategori.objects.filter(id=idk).update(nama=nama)

			return redirect('kategori')

######################## TRANSAKSI  ########################

@login_required(login_url='login')
def PageTransaksi(request):
	dtransaksi = Transaksi.objects.all()
	form = FormTransaksi()

	totalg = Transaksi.objects.aggregate(Sum('total'))

	totali = Transaksi.objects.aggregate(Sum('qty'))

	if request.method == 'POST':
		formset = FormTransaksi(request.POST)
		if formset.is_valid():
			idbarang = request.POST['barang']
			barang = Barang.objects.get(id=int(idbarang))
			if formset.cleaned_data['status'] == 'Keluar':
				if int(formset.cleaned_data['qty']) > int(barang.stok):
					messages.info(request, 'Stok '+barang.nama+' tidak mencukupi!')
				else:
					formset.save()
					return redirect('/transaksi/')
			else:
				formset.save()
				return redirect('/transaksi/')


	context = {'dtransaksi': dtransaksi, 'act':'Transaksi', 'form':form, 'total':totalg, 'totali':totali}
	return render(request, 'admin/transaksi.html', context)

@login_required(login_url='login')
def deleteTransaksi(request, pk):
	dtransaksi = Transaksi.objects.get(id=pk)
	form = FormTransaksi()

	if request.method == 'POST':
		dtransaksi.delete()
		return redirect('transaksi')

@login_required(login_url='login')
def selesaiTransaksi(request):
	dtrans = Transaksi.objects.all()

	for i in dtrans:
		x = Barang.objects.filter(id = i.barang.id).get()
		p1 = i.idtrx
		p2 = i.barang
		p3 = i.status
		p4 = x.harga_jual
		p5 = i.qty
		p6 = i.total
		p7 = x.harga_beli
		rt = RekapTransaksi(idtrx=p1, barang=p2, status=p3, harga_jual=p4, harga_beli=p7, qty=p5, total=p6)
		rt.save()

	signals.pre_delete.disconnect(undostok, sender=Transaksi)
	Transaksi.objects.all().delete()
	signals.pre_delete.connect(undostok, sender=Transaksi)
	messages.info(request, 'Transaksi Selesai')
	return redirect('/transaksi/')

@login_required(login_url='login')
def rekapTransaksi(request):
	drekap = RekapTransaksi.objects.raw('SELECT * FROM mainapp_rekaptransaksi GROUP BY idtrx')
	context = {'drekap':drekap, 'act':'Rekap Transaksi'}

	return render(request, 'admin/rekaptransaksi.html', context)

######################### REKAP ###########################
@login_required(login_url='login')
def detailRekap(request, idtrx):
	drekap = RekapTransaksi.objects.filter(idtrx = idtrx)
	totalg = RekapTransaksi.objects.filter(idtrx = idtrx).aggregate(Sum('total'))
	totali = RekapTransaksi.objects.filter(idtrx = idtrx).aggregate(Sum('qty'))
	getact = drekap.first()
	act = getact.idtrx

	listunt = []

	for i in drekap:
		jual = i.harga_jual * i.qty
		beli = i.harga_beli * i.qty
		untung = jual - beli
		listunt.append(untung)

	totaluntung = sum(listunt)

	context = {'drekap': drekap, 'act':act, 'totalg':totalg, 'totali':totali, 'totaluntung':totaluntung}

	return render(request, 'admin/detailrekap.html', context)