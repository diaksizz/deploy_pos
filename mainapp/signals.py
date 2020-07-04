from django.db.models.signals import pre_save
from .models import *
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
import datetime

def subtotaldanharga(sender, instance, *args, **kwargs):

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


	barang = Barang.objects.get(id=instance.barang.id)

	if instance.status == 'Masuk':
		instance.harga = instance.barang.harga_beli

		barang.stok = barang.stok + instance.qty
		barang.save()
	else:
		instance.harga = instance.barang.harga_jual

		barang.stok = barang.stok - instance.qty
		barang.save()

	instance.total = instance.qty * instance.harga

def undostok(sender, instance, *args, **kwargs):
	barang = Barang.objects.get(id=instance.barang.id)

	if instance.status == 'Masuk':
		barang.stok = barang.stok - instance.qty
		barang.save()
	else:
		barang.stok = barang.stok + instance.qty
		barang.save()



pre_save.connect(subtotaldanharga, sender=Transaksi)
pre_delete.connect(undostok, sender=Transaksi)