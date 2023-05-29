from django.urls import path
from .views import (
    ClassifyListView,
    ClassifyDetailView,
    ClassifyCreateView,
    ClassifyUpdateView,
    ClassifyDeleteView
)
from . import views

urlpatterns = [
    path('', views.beranda, name='classify-beranda'),
    path('tutorial/', views.tutorial, name='classify-tutorial'),
    path('riwayat/', ClassifyListView.as_view(), name='classify-riwayat'),
    path('skrining/<int:pk>/hasil/', ClassifyDetailView.as_view(), name='classify-hasil'),
    path('skrining/', ClassifyCreateView.as_view(), name='classify-skrining'),
    path('skrining/<int:pk>/sunting/', ClassifyUpdateView.as_view(), name='classify-sunting'),
    path('skrining/<int:pk>/hapus/', ClassifyDeleteView.as_view(), name='classify-hapus'),
]
