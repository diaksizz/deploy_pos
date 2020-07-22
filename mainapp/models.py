from django.db import models
from django.db import connection
from django.db.models.signals import pre_save, pre_delete

# Create your models here.
class Kategori(models.Model):
	nama = models.CharField(max_length=200)
	created_at = models.DateTimeField(auto_now_add=True, auto_now=False, null=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.nama

class Supplier(models.Model):
	nama = models.CharField(max_length=200, null=True, blank=True)
	created_at = models.DateTimeField(auto_now_add=True, auto_now=False, null=False)
	updated_at = models.DateTimeField(auto_now=True)


	def __str__(self):
		return self.nama

class Barang(models.Model):
	nama = models.CharField(max_length=200)
	kategori = models.ForeignKey(Kategori, null=True, on_delete=models.SET_NULL)
	supplier = models.ManyToManyField(Supplier, through='SupplierRelationship')
	created_at = models.DateTimeField(auto_now_add=True, null=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.nama

class LogBarang(models.Model):
	barang = models.ForeignKey(Barang, null=True, on_delete=models.SET_NULL)
	kasir = models.CharField(max_length=200, null=True)
	supplier = models.ForeignKey(Supplier, null=True, on_delete=models.SET_NULL)
	status = models.CharField(max_length=200, null=True)
	qty = models.IntegerField(null=True, blank=True)
	stok = models.IntegerField(null=True, blank=True)
	created_at = models.DateTimeField(auto_now_add=True, null=True)
	updated_at = models.DateTimeField(auto_now=True)


class SupplierRelationship(models.Model):
	barang = models.ForeignKey(Barang, on_delete=models.CASCADE)
	supplier = models.ForeignKey(Supplier, null=True, on_delete=models.SET_NULL)
	stok = models.IntegerField(null=True, blank=True, default=0)
	harga_jual = models.IntegerField(null=True, blank=True, default=0)
	harga_beli = models.IntegerField(null=True, blank=True, default=0)
	created_at = models.DateTimeField(auto_now_add=True, null=True)
	updated_at = models.DateTimeField(auto_now=True)


	def __str__(self):
         return self.supplier.nama


class Transaksi(models.Model):
	STATUS = (('Keluar', 'Keluar'), ('Masuk', 'Masuk'))
	idtrx = models.CharField(max_length=12, null=True, blank=True)
	barang = models.ForeignKey(Barang, blank=True, null=True, on_delete=models.CASCADE)
	supplier = models.ForeignKey(Supplier, blank=True, null=True, on_delete=models.CASCADE)
	status = models.CharField(max_length=200, null=True, blank=True, choices=STATUS)
	harga_jual = models.IntegerField(null=True, blank=True, default=0)
	harga_beli = models.IntegerField(null=True, blank=True, default=0)
	harga = models.IntegerField(null=True, blank=True)
	qty = models.IntegerField(null=True)
	total = models.IntegerField(null=True, blank=True)
	created_at = models.DateTimeField(auto_now_add=True, null=True)

	def __str__(self):
		return self.status

class RekapTransaksi(models.Model):
	STATUS = (('Keluar', 'Keluar'), ('Masuk', 'Masuk'))

	idtrx = models.CharField(max_length=12, null=True, blank=True)
	barang = models.CharField(max_length=200, null=True)
	kategori = models.CharField(max_length=200, null=True)
	supplier = models.CharField(max_length=200, null=True)
	status = models.CharField(max_length=200, null=True, choices=STATUS)
	harga = models.IntegerField(null=True, blank=True)
	harga_jual = models.IntegerField(null=True, blank=True)
	harga_beli = models.IntegerField(null=True, blank=True)
	qty = models.IntegerField(null=True)
	total = models.IntegerField(null=True, blank=True)
	created_at = models.DateTimeField(auto_now_add=True, null=True)

	def __str__(self):
		return self.idtrx
