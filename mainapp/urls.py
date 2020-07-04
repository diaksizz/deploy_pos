from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('barang/', views.PageBarang, name="barang"),
    path('barang/<str:pk>/delete', views.deleteBarang, name="delBarang"),
    path('barang/update', views.updateBarang, name="upBarang"),
    #################################################################################
    path('kategori/', views.PageKategori, name="kategori"),
    path('kategori/<str:pk>/delete', views.deleteKategori, name="delKategori"),
    path('kategori/update', views.updateKategori, name="upKategori"),
    #################################################################################
    path('transaksi/', views.PageTransaksi, name="transaksi"),
    path('transaksi/<str:pk>/delete', views.deleteTransaksi, name="deltrans"),
    path('transaksi/selesai', views.selesaiTransaksi, name="transdone"),
    path('rekaptransaksi/', views.rekapTransaksi, name="rekaptrans"),
    path('detailtransaksi/<str:idtrx>', views.detailRekap, name="detailrekap"),
    #################################################################################
    path('login/', views.loginPage, name="login"),
    path('register/', views.registerPage, name="register"),
    path('logout/', views.logoutUser, name="logout"),
]
