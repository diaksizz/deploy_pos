from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('barang/', views.PageBarang, name="barang"),
    path('barang/<str:pk>/delete', views.deleteBarang, name="delBarang"),
    path('barang/update', views.updateBarang, name="upBarang"),
    path('barang/hargastok/', views.harstokPage, name="hargastok"),
    ################################################################################
    path('supplier',views.PageSupplier, name="Supplier"),
    path('supplier/<str:pk>/delete', views.deleteSupplier, name="delSupplier"),
    path('supplier/update/<str:pk>', views.updateSupplier, name="upSupplier"),
    #################################################################################
    path('kategori/', views.PageKategori, name="kategori"),
    path('kategori/<str:pk>/delete', views.deleteKategori, name="delKategori"),
    path('kategori/update/<str:pk>', views.updateKategori, name="upKategori"),
    #################################################################################
    path('transaksi/keluar', views.PageTransaksiKeluar, name="transaksikeluar"),
    path('transaksi/keluar/add', views.PageTransaksiKeluarAdd, name="transaksikeluaradd"),
    path('transaksi/masuk', views.PageTransaksiMasuk, name="transaksimasuk"),
    # path('transaksi/<str:pk>/delete', views.deleteTransaksi, name="deltrans"),
    path('transaksi/selesai', views.selesaiTransaksi, name="transdone"),
    path('rekaptransaksi/', views.rekapTransaksi, name="rekaptrans"),
    path('detailtransaksi/<str:idtrx>', views.detailRekap, name="detailrekap"),
    #################################################################################
    path('updateuser/',views.updateUserPage, name="updateuser"),
    path('login/', views.loginPage, name="login"),
    path('register/', views.registerPage, name="register"),
    path('logout/', views.logoutUser, name="logout"),
    #################################################################################
    path('laporan/', views.laporanPage, name="laporan"),
    path('laporan/filter/', views.filterRekap, name="filter"),

    path('ajax/loadsupplier/', views.load_supplier, name="loadsupplier"),
    path('ajax/loadsupplier/edit', views.load_supplier_edit, name="loadsupplieredit"),
    path('ajax/getbarang/', views.load_barang, name="loadbarang"),
    path('ajax/getkategori/', views.load_kategori, name="loadkategori"),
    path('ajax/getsupplier/', views.load_supplier, name="loadsupplier"),
    path('ajax/table/', views.load_table, name="tabletransaksi_ajax"),
    path('ajax/getstok/', views.load_stok, name="loadstok"),
    path('ajax/getlog/', views.load_log, name="loadlog"),
    path('ajax/updatebarang/<str:pk>', views.update_barang, name="updateeeee"),
    path('ajax/gettotal', views.gettotal, name="gettotal"),
    path('ajax/transaksi/delete/', views.deleteTransaksi, name="deletetrajax"),

    #####################################################################################
    path('pdf-view-keluar/', views.ViewPDF.as_view(), name="pdfviewkeluar"),
    path('pdf-view-masuk/', views.ViewPDFMasuk.as_view(), name="pdfviewmasuk"),
]
