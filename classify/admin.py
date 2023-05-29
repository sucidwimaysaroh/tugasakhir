from django.contrib import admin
from .models import Classify

@admin.register(Classify)
class ClassifyAdmin(admin.ModelAdmin):
    list_display = ("nama_Dokter", "nama_Pasien", "hasil")
