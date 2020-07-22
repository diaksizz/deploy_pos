from django.db.models.signals import pre_save, post_save
from .models import *
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
import datetime

def subtotaldanharga(sender, instance, *args, **kwargs):

	print(instance.barang.id)
	print(instance.supplier.id)
	print(instance.status)

	if Transaksi.objects.count() == 0:
		x = datetime.datetime.now()
		tgl = x.strftime("%d")
		bln = x.strftime("%m")
		thn = x.strftime("%y")
		hr = x.strftime("%H")
		mn = x.strftime("%M")
		dt = x.strftime("%S")
		hasil = tgl+bln+thn+hr+mn+dt

		instance.idtrx = hasil
	else:
		idTrx = Transaksi.objects.all()[:1]

		for i in idTrx:
			existed = i.idtrx

		instance.idtrx = existed


	supbar = SupplierRelationship.objects.get(barang_id=instance.barang.id, supplier_id=instance.supplier.id)

	if instance.status == 'Masuk':
		instance.harga = instance.harga_beli
		supbar.harga_jual = instance.harga_jual
		supbar.harga_beli = instance.harga_beli
		supbar.stok = supbar.stok + instance.qty
		supbar.save()
	else:
		instance.harga = supbar.harga_jual
		instance.harga_jual = supbar.harga_jual
		instance.harga_beli = supbar.harga_beli

		supbar.stok = supbar.stok - instance.qty
		supbar.save()

	instance.total = instance.qty * instance.harga

def undostok(sender, instance, *args, **kwargs):
	barang = SupplierRelationship.objects.get(barang_id=instance.barang.id, supplier_id=instance.supplier.id)
	print(barang.harga_beli)
	print(instance.harga_beli)
	if instance.status == 'Masuk':
		barang.harga_beli = instance.harga_beli
		barang.harga_jual = instance.harga_jual
		barang.stok = barang.stok - instance.qty
		barang.save()
	else:
		barang.stok = barang.stok + instance.qty
		barang.save()

pre_save.connect(subtotaldanharga, sender=Transaksi)
pre_delete.connect(undostok, sender=Transaksi)