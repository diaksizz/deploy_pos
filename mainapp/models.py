from django.db import models
from django.db import connection
from django.db.models.signals import pre_save, pre_delete

# Create your models here.
class Kategori(models.Model):
	nama = models.CharField(max_length=200)
	created_at = models.DateTimeField(auto_now_add=True, null=True)

	def __str__(self):
		return self.nama
	
class Barang(models.Model):
	nama = models.CharField(max_length=200)
	kategori = models.ForeignKey(Kategori, null=True, on_delete=models.CASCADE)
	stok = models.IntegerField()
	harga_jual = models.IntegerField(null=True)
	harga_beli = models.IntegerField(null=True)
	created_at = models.DateTimeField(auto_now_add=True, null=True)

	def __str__(self):
		return self.nama

class Transaksi(models.Model):
	STATUS = (('Keluar', 'Keluar'), ('Masuk', 'Masuk'))
	idtrx = models.CharField(max_length=12, null=True, blank=True)
	barang = models.ForeignKey(Barang, null=True, on_delete=models.SET_NULL)
	status = models.CharField(max_length=200, null=True, choices=STATUS)
	harga = models.IntegerField(null=True, blank=True)
	qty = models.IntegerField(null=True)
	total = models.IntegerField(null=True, blank=True)
	created_at = models.DateTimeField(auto_now_add=True, null=True)

	def __str__(self):
		return self.status

class RekapTransaksi(models.Model):
	idtrx = models.CharField(max_length=12, null=True, blank=True)
	barang = models.ForeignKey(Barang, null=True, on_delete=models.SET_NULL)
	status = models.CharField(max_length=200, null=True)
	harga_jual = models.IntegerField(null=True, blank=True)
	harga_beli = models.IntegerField(null=True, blank=True)
	qty = models.IntegerField(null=True)
	total = models.IntegerField(null=True, blank=True)
	created_at = models.DateTimeField(auto_now_add=True, null=True)

	def __str__(self):
		return self.idtrx

