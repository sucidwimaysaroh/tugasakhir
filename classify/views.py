from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Classify
from django.views.generic import (
    ListView,
    DetailView,
    UpdateView,
    CreateView,
    DeleteView
)

def beranda (request):
    return render(request, 'classify/beranda.html')

def tutorial (request):
    return render(request, 'classify/tutorial.html')

class ClassifyListView(LoginRequiredMixin, ListView):
    model = Classify

    def get_queryset(self):
        return Classify.objects.filter(nama_Dokter = self.request.user).all().order_by('-tanggal_Skrining')

class ClassifyDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Classify

    def test_func(self):
        classify = self.get_object()
        if self.request.user == classify.nama_Dokter:
            return True
        return False

class ClassifyCreateView(LoginRequiredMixin, CreateView):
    model = Classify
    fields = ['nama_Pasien', 'tanggal_Lahir', 'nomer_Rekam_Medis', 'gambar_Mammogram']

    def form_valid(self, form):
        form.instance.nama_Dokter = self.request.user
        return super().form_valid(form)

class ClassifyUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Classify
    fields = ['nama_Pasien', 'tanggal_Lahir', 'nomer_Rekam_Medis', 'gambar_Mammogram', 'hasil']

    def form_valid(self, form):
        form.instance.nama_Dokter = self.request.user
        messages.success(self.request, f'Data skrining berhasil diperbarui!')
        return super().form_valid(form)

    def test_func(self):
        classify = self.get_object()
        if self.request.user == classify.nama_Dokter:
            return True
        return False

class ClassifyDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Classify
    success_url = reverse_lazy('classify-riwayat')

    def form_valid(self, form):
        messages.success(self.request, f'Data skrining berhasil dihapus!')
        return super().form_valid(form)

    def test_func(self):
        classify = self.get_object()
        if self.request.user == classify.nama_Dokter:
            return True
        return False
