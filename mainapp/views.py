from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.contrib import messages
from django.db.models import signals
from django.db.models import Sum, Count, Q
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.forms import inlineformset_factory

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group

###############print########################
from io import BytesIO
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.views import View


from .models import *
from .forms import *
from .filters import *
from .signals import *
from .decorators import unauthenticated_user, allowed_users

from datetime import date

######################print#################################
def render_to_pdf(template_src, context_dict={}):
	template = get_template(template_src)
	html  = template.render(context_dict)
	result = BytesIO()
	pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
	if not pdf.err:
		return HttpResponse(result.getvalue(), content_type='application/pdf')
	return None

class ViewPDF(View):
	def get(self, request, *args, **kwargs):
		idtrx = RekapTransaksi.objects.last()
		trx = RekapTransaksi.objects.filter(idtrx=idtrx).order_by('-idtrx')
		totalg = RekapTransaksi.objects.filter(idtrx = idtrx).aggregate(Sum('total'))
		tgl = RekapTransaksi.objects.filter(idtrx=idtrx)[:1].get()
		
		user = request.user	
		context = {'user':user ,'trx':trx, 'totalg':totalg,'tgl':tgl}
		pdf = render_to_pdf('admin/pdf_template.html', context)
		return HttpResponse(pdf, content_type='application/pdf')


class ViewPDFMasuk(View):
	def get(self, request, *args, **kwargs):
		idtrx = RekapTransaksi.objects.last()
		trx = RekapTransaksi.objects.filter(idtrx=idtrx).order_by('-idtrx')
		totalg = RekapTransaksi.objects.filter(idtrx = idtrx).aggregate(Sum('total'))
		tgl = RekapTransaksi.objects.filter(idtrx=idtrx)[:1].get()
		
		user = request.user	
		context = {'user':user ,'trx':trx, 'totalg':totalg,'tgl':tgl}
		pdf = render_to_pdf('admin/pdfMasuk.html', context)
		return HttpResponse(pdf, content_type='application/pdf')


def updateUserPage(request):
	user = request.user
	formup = UpdateUserForm(instance=user)
	
	if request.method == 'POST':
		password_1=request.POST['password1']
		password_2=request.POST['password2']
		formup = UpdateUserForm(request.POST, instance=user)
		if formup.is_valid():
			user.set_password(password_1)
			user.save()
	context = {'formup':formup} 
	return render(request, 'admin/edituserPage.html',context)


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
	
	totalomset = RekapTransaksi.objects.filter(created_at__year=x.year, created_at__month=x.month, created_at__day=x.day,status='Keluar').aggregate(Sum('total'))

	tottrans = RekapTransaksi.objects.values('idtrx').filter(created_at__year=x.year, created_at__month=x.month, created_at__day=x.day, status='Keluar').order_by('idtrx').annotate(Count('idtrx'))

	# totprod = Barang.objects.all().count()

	totunt = RekapTransaksi.objects.filter(created_at__year=x.year, created_at__month=x.month, created_at__day=x.day, status='Keluar')

	most = RekapTransaksi.objects.values('barang').filter(created_at__year=x.year, created_at__month=x.month, created_at__day=x.day, status='Keluar').annotate(dcount=Sum('qty')).order_by('-dcount')[:1]

	inout = LogBarang.objects.values('barang__nama', 'supplier__nama', 'stok').filter(created_at__year=x.year, created_at__month=x.month, created_at__day=x.day).annotate(dcount=Sum('qty', filter=Q(status='Keluar'))).annotate(din=Sum('qty', filter=Q(status='Masuk')))

	# inout = SupplierRelationship.objects.all()

	
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
	print(most.count)
	context = {'act':'Dashboard', 'totalomset':totalomset, 'tottrans':tottrans, 'most':most, 'totaluntung':totaluntung,'tanggalprint':tanggalprint, 'inout':inout,}
	# context = {'act':'Dashboard', 'totalomset':totalomset, 'totprod':totprod, 'tottrans':tottrans, 'totaluntung':totaluntung, 'most':most, 'inout':inout, 'tanggalprint':tanggalprint}
	return render(request, 'admin/home.html',context)


################ SUPPLIER   ######################
def PageSupplier(request):
	dsupplier = Supplier.objects.all()
	form = FormSupplier()
	formup = FormEditSupplier()

	if request.method == 'POST':
		form = FormSupplier(request.POST)
		if form.is_valid():
			form.save()
			messages.success(request, 'Berhasil Menambahkan Supplier')
			return redirect('Supplier')
	context = {'dsupplier':dsupplier, 'act':'Supplier', 'form':form,'formup':formup}
	return render(request,'admin/suplier.html',context)


# @login_required(login_url='login')
def deleteSupplier(request, pk):
	dsupplier = Supplier.objects.get(id=pk)
	form = FormSupplier()

	if request.method == 'POST':
		dsupplier.delete()
		messages.success(request, 'Berhasil Menghapus Supplier')
		return redirect('Supplier')

# @login_required(login_url='login')
def updateSupplier(request, pk):
	dsupplier = Supplier.objects.get(id=pk)
	formup = FormEditSupplier(instance=dsupplier)
	if request.method == 'POST':
		formup = FormEditSupplier(request.POST, instance=dsupplier)
		if formup.is_valid():
			formup.save()
			messages.success(request, 'Berhasil Melakukan Perubahan pada Supplier')
			return redirect('/supplier')

		

################   BARANG   ######################

def load_table(request):
	dtransaksi = Transaksi.objects.all()
	return render(request, 'admin/partial/tabletransaksikeluar.html', {'dtransaksi': dtransaksi})

def load_log(request):
	barang_id = request.GET.get('barang')
	barang = LogBarang.objects.filter(barang__id=barang_id)
	return render(request, 'admin/partial/logbarang.html', {'barang': barang})

def load_kategori(request):
	kategori_id = request.GET.get('kategori')
	kategori = Kategori.objects.get(id = kategori_id)
	formup = FormEditKategori(instance=kategori)
	context = {'formup': formup, 'kategori_id':kategori_id}

	return render(request, 'admin/partial/updatekategori.html', context)

def load_supplier_edit(request):
	supplier_id = request.GET.get('supplier')
	supplier = Supplier.objects.get(id = supplier_id)
	formup = FormEditSupplier(instance=supplier)
	context = {'formup': formup}

	return render(request, 'admin/partial/updatesupplier.html', context)

@login_required(login_url='login')
def PageBarang(request):
	dbarang = Barang.objects.all()
	form = FormBarang()
	formup = FormEditBarang()
	

	if request.method == 'POST':
		form = FormBarang(request.POST)
		if form.is_valid():
			form.save()
			messages.success(request, 'Berhasil Menambahkan Barang')
			return redirect('/barang/')
	
	context = {'dbarang': dbarang, 'act':'Barang', 'form':form, 'formup':formup}
	return render(request, 'admin/barang.html', context)

@login_required(login_url='login')
def deleteBarang(request, pk):
	dbarang = Barang.objects.get(id=pk)
	form = FormBarang()

	if request.method == 'POST':
		dbarang.delete()
		messages.success(request, 'Berhasil Menghapus Barang')
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
			supplier = formup.cleaned_data['supplier']
			print(supplier)

			barang = Barang.objects.get(id=idb)
			Barang.objects.filter(id=idb).update(nama=nama, kategori=kategori, stok=stok, harga_jual=harga_jual, harga_beli=harga_beli)
			
			for i in supplier:
				print(i.supplier)

			return redirect('barang')


#################### KATEGORI ########################
@login_required(login_url='login')
def PageKategori(request):
	dkategori = Kategori.objects.all()
	form = FormKategori()
	formup = FormEditKategori()
	data = 'komputer'

	if request.method == 'POST':
		form = FormKategori(request.POST)
		if form.is_valid():
			form.save()
			messages.success(request, 'Berhasil Menambahkan Kategori')
			return redirect('/kategori/')

	context = {'dkategori': dkategori, 'act':'Kategori', 'form':form, 'formup':formup, 'data':data}
	return render(request, 'admin/kategori.html', context)


@login_required(login_url='login')
def deleteKategori(request, pk):
	dkategori = Kategori.objects.get(id=pk)
	form = FormKategori()

	if request.method == 'POST':
		dkategori.delete()
		messages.success(request, 'Berhasil Menghapus Kategori')
		return redirect('kategori')

@login_required(login_url='login')
def updateKategori(request, pk):
	dkategori = Kategori.objects.get(id=pk)
	formup = FormEditKategori(instance=dkategori)
	if request.method == 'POST':
		formup = FormEditKategori(request.POST, instance=dkategori)
		if formup.is_valid():
			formup.save()
			messages.success(request, 'Berhasil melakukan perubahan pada kategori')
			return redirect('/kategori/')

######################## TRANSAKSI  ########################
def gettotal(request):
	keranjang = Transaksi.objects.all()
	
	if keranjang.count() == 0:
		total = 0
		return render(request, 'admin/partial/total.html', {'total':total, 'status':'status'})

	total = Transaksi.objects.aggregate(Sum('total'))
	status = Transaksi.objects.all()[:1].get()


	return render(request, 'admin/partial/total.html', {'total':total, 'status':status})

def load_supplier(request):
	barang_id = request.GET.get('barang')
	suppliers = SupplierRelationship.objects.filter(barang__id=barang_id)
	return render(request, 'admin/optionsuppliertransaksi.html', {'suppliers': suppliers})

def load_stok(request):
	barang_id = request.GET.get('barang')
	supplier_id = request.GET.get('supplier')
	stok = SupplierRelationship.objects.get(barang__id=barang_id, supplier__id=supplier_id)
	return render(request, 'admin/partial/alertstok.html', {'stok': stok})

@login_required(login_url='login')
def PageTransaksiMasuk(request):

	dtransaksi = Transaksi.objects.all()
	form = FormTransaksi(initial={'status': 'Masuk'})

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
					return redirect('/transaksi/masuk')
			else:
				formset.save()
				return redirect('/transaksi/masuk')
		else:
			print(formset.errors)


	context = {'dtransaksi': dtransaksi, 'act':'Transaksi', 'form':form, 'total':totalg, 'totali':totali}
	return render(request, 'admin/transaksimasuk.html', context)

def PageTransaksiKeluar(request):
	dtransaksi = Transaksi.objects.all()
	form = FormTransaksi()

	totalg = Transaksi.objects.aggregate(Sum('total'))

	totali = Transaksi.objects.aggregate(Sum('qty'))

	if request.method == 'POST':
		formset = FormTransaksi(request.POST)
		if formset.is_valid():
			idbarang = request.POST['barang']
			idsupplier = request.POST['supplier']
			barang = SupplierRelationship.objects.get(barang_id=int(idbarang), supplier_id=int(idsupplier))
			if formset.cleaned_data['status'] == 'Keluar':
				if int(formset.cleaned_data['qty']) > int(barang.stok):
					messages.info(request, 'Stok '+barang.barang.nama+' tidak mencukupi!')
				else:
					formset.save()
					return redirect('/transaksi/keluar')
			else:
				formset.save()
				return redirect('/transaksi/keluar')
	context = {'dtransaksi': dtransaksi, 'act':'Transaksi', 'form':form, 'total':totalg, 'totali':totali}
	return render(request, 'admin/transaksikeluar.html', context)

def PageTransaksiKeluarAdd(request):
	dtransaksi = Transaksi.objects.all()
	form = FormTransaksi()

	totalg = Transaksi.objects.aggregate(Sum('total'))

	totali = Transaksi.objects.aggregate(Sum('qty'))

	if request.method == 'POST' and request.is_ajax():
		formset = FormTransaksi(request.POST)
		if formset.is_valid():
			idbarang = request.POST['barang']
			idsupplier = request.POST['supplier']
			barang = SupplierRelationship.objects.get(barang_id=int(idbarang), supplier_id=int(idsupplier))
			if formset.cleaned_data['status'] == 'Keluar':
				if int(formset.cleaned_data['qty']) > int(barang.stok):
					messages.info(request, 'Stok '+barang.barang.nama+' tidak mencukupi!')
					return JsonResponse({"success":False}, status=400)
				else:
					formset.save()
					return JsonResponse({"success":True}, status=200)

@login_required(login_url='login')
def deleteTransaksi(request):
	barang_id = request.GET.get('barang')
	print(barang_id)
	dtransaksi = Transaksi.objects.get(id=barang_id)

	if request.method == 'GET':
		dtransaksi.delete()
		messages.success(request, 'Berhasil Menghapus Barang')
		return JsonResponse({"success":True}, status=200)
		# if dtransaksi.status == 'Masuk':
		# 	return redirect('/transaksi/masuk')
		# else:
		# 	return redirect('/transaksi/keluar')

@login_required(login_url='login')
def selesaiTransaksi(request):
	dtrans = Transaksi.objects.all()

	if dtrans.count() == 0:
		messages.info(request, 'Tidak ada barang!')
		return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

	for i in dtrans:
		x = SupplierRelationship.objects.filter(barang_id = i.barang.id, supplier_id= i.supplier.id).get()
		# nama = request.user
		p1 = i.idtrx
		p2 = i.barang.nama
		p3 = i.status
		p4 = x.harga_jual
		p5 = i.qty
		p6 = i.total
		p7 = x.harga_beli
		p8 = i.harga
		p9 = i.supplier.nama
		p10 = i.barang.kategori.nama
		lb = LogBarang(barang=i.barang, supplier=i.supplier, status=i.status, qty=i.qty, stok=x.stok, kasir=request.user)
		rt = RekapTransaksi(idtrx=p1, barang=p2, kategori=p10, status=p3, harga_jual=p4, harga_beli=p7, qty=p5, total=p6, harga=p8, supplier=p9)
		lb.save()
		rt.save()


	forif = Transaksi.objects.all()[:1].get()

	signals.pre_delete.disconnect(undostok, sender=Transaksi)
	Transaksi.objects.all().delete()
	signals.pre_delete.connect(undostok, sender=Transaksi)

	messages.info(request, 'Transaksi Selesai')

	if forif.status == 'Masuk':
		return redirect('/transaksi/masuk')
	else:
		return redirect('/transaksi/keluar')

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
	status = getact.status

	listunt = []

	for i in drekap:
		if i.status == 'Keluar':
			jual = i.harga_jual * i.qty
			beli = i.harga_beli * i.qty
			untung = jual - beli
			listunt.append(untung)

	totaluntung = sum(listunt)

	context = {'drekap': drekap, 'act':act, 'totalg':totalg, 'totali':totali, 'totaluntung':totaluntung,'status':status}

	return render(request, 'admin/detailrekap.html', context)

def laporanPage(request):
	totaluntung = 0
	
	drekap = RekapTransaksi.objects.all()

	rekapFilter = FormRekap()

	itemkeluar = 0

	context = {'rekapFilter':rekapFilter, 'drekap':drekap, 'act':'Laporan Transaksi', 'itemkeluar':itemkeluar}

	return render(request, 'admin/laporan.html', context)

def filterRekap(request):
	rekapFilter = FormRekap()
	totaluntung = 0
	if request.method == 'GET':
		rekapFilter = FormRekap(request.GET)
		if rekapFilter.is_valid():
			bulan = rekapFilter.cleaned_data['bulan']
			tahun = rekapFilter.cleaned_data['tahun']
			status = rekapFilter.cleaned_data['status']

			drekap = RekapTransaksi.objects.filter(created_at__year=tahun, status=status, created_at__month=bulan)

			listunt = []
			if status == 'Keluar':
				for i in drekap:
					jual = i.harga_jual * i.qty
					beli = i.harga_beli * i.qty
					untung = jual - beli
					listunt.append(untung)

					totaluntung = sum(listunt)

			elif status == 'Semua':
				drekap = RekapTransaksi.objects.filter(created_at__year=tahun,created_at__month=bulan)
	
			itemkeluar = drekap.aggregate(Sum('qty'))
			tottrans = drekap.order_by('idtrx').annotate(Count('idtrx'))

	context = {'rekapFilter':rekapFilter, 'drekap':drekap, 'act':'Laporan Transaksi', 'itemkeluar':itemkeluar, 'tottrans':tottrans, 'totaluntung':totaluntung}
	return render(request, 'admin/laporan.html', context)

def load_barang(request):
	barang_id = request.GET.get('barang')
	dbarang = Barang.objects.get(id=barang_id)
	formup = FormEditBarang(instance=dbarang)
	context = {'formup': formup, 'barang_id':barang_id}

	return render(request, 'admin/partial/updatebarang.html', context)

def update_barang(request, pk):
	dbarang = Barang.objects.get(id=pk)
	formup = FormEditBarang(instance=dbarang)
	if request.method == 'POST':
		formup = FormEditBarang(request.POST, instance=dbarang)
		if formup.is_valid():
			formup.save()
			messages.success(request, 'Berhasil Melakukan Perubahan pada Barang')
			return redirect('/barang/')

def harstokPage(request):
	dhargastok = SupplierRelationship.objects.all()
	context = {'dhargastok':dhargastok, 'act':'Harga & Stok'}

	return render(request, 'admin/harstok.html', context)
