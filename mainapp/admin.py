from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Kategori)
admin.site.register(Barang)
admin.site.register(Transaksi)
admin.site.register(RekapTransaksi)
admin.site.register(LogBarang)
admin.site.register(Supplier)
admin.site.register(SupplierRelationship)
