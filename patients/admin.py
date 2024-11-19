from django.contrib import admin
from django.contrib.auth.models import Group, Permission
from guardian.admin import GuardedModelAdmin
from .models import Patient

# Mevcut GroupAdmin'i genişlet
class CustomGroupAdmin(admin.ModelAdmin):
    list_display = ('name',)  # Grup adı gösterimi
    search_fields = ('name',)  # Grup arama
    filter_horizontal = ('permissions',)  # İzinleri yatay düzenle

# Group modelini yeni admin ile yeniden kaydet
admin.site.unregister(Group)  # Önce kaydı kaldır
admin.site.register(Group, CustomGroupAdmin)  # Yeniden kaydet

class PatientAdmin(GuardedModelAdmin):
    pass

admin.site.register(Patient, PatientAdmin)