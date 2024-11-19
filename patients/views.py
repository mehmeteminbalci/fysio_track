from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Patient, Appointment
from .forms import PatientForm, AppointmentForm
from .permissions import get_user_patients
from django.http import JsonResponse
from datetime import datetime, timedelta
from django.core.paginator import Paginator
from django.db.models import Count
from django.utils.timezone import now, timedelta
from django.utils.safestring import mark_safe
import json
from django.db.models.functions import TruncDay


# Kullanıcının fizyoterapist olup olmadığını kontrol eden test
def is_physiotherapist(user):
    return user.groups.filter(name='Fizyoterapist').exists()

# Ana sayfa görünümü
def home(request):
    return render(request, 'patients/home.html')

# Hasta Yönetimi

@login_required
@user_passes_test(is_physiotherapist)
def physiotherapist_patients(request):
    patients = Patient.objects.filter(therapist=request.user)
    return render(request, 'patients/physiotherapist_patients.html', {'patients': patients})

@login_required
def patient_list(request):
    patients = get_user_patients(request.user)  # Kullanıcının erişebileceği hastalar
    return render(request, 'patients/patient_list.html', {'patients': patients})

@login_required
def patient_detail(request, pk):
    patient = get_object_or_404(Patient, pk=pk, therapist=request.user)
    return render(request, 'patients/patient_detail.html', {'patient': patient})

@login_required
def patient_create(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            patient = form.save(commit=False)
            patient.therapist = request.user
            patient.save()
            return redirect('patient_list')
    else:
        form = PatientForm()
    return render(request, 'patients/patient_form.html', {'form': form})

@login_required
def patient_update(request, pk):
    patient = get_object_or_404(Patient, pk=pk, therapist=request.user)
    if request.method == 'POST':
        form = PatientForm(request.POST, instance=patient)
        if form.is_valid():
            form.save()
            return redirect('patient_list')
    else:
        form = PatientForm(instance=patient)
    return render(request, 'patients/patient_form.html', {'form': form})

@login_required
def patient_delete(request, pk):
    patient = get_object_or_404(Patient, pk=pk, therapist=request.user)
    if request.method == 'POST':
        patient.delete()
        return redirect('patient_list')
    return render(request, 'patients/patient_confirm_delete.html', {'patient': patient})

# Randevu Yönetimi

@login_required
def appointment_list(request):
    # Tüm randevuları getir
    appointments = Appointment.objects.filter(therapist=request.user).order_by('-date_time')
    
    # Sayfalama işlemi için Paginator sınıfını kullan
    paginator = Paginator(appointments, 5)  # Her sayfada 5 randevu göster
    
    # Kullanıcının o anki sayfa numarasını al
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'patients/appointment_list.html', {'page_obj': page_obj})

@login_required
def appointment_create(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.therapist = request.user
            appointment.save()
            return redirect('appointment_list')
    else:
        form = AppointmentForm()
    return render(request, 'patients/appointment_form.html', {'form': form})

@login_required
def appointment_update(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk, therapist=request.user)
    if request.method == 'POST':
        form = AppointmentForm(request.POST, instance=appointment)
        if form.is_valid():
            form.save()
            return redirect('appointment_list')
    else:
        form = AppointmentForm(instance=appointment)
    return render(request, 'patients/appointment_form.html', {'form': form})

@login_required
def appointment_delete(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk, therapist=request.user)
    if request.method == 'POST':
        appointment.delete()
        return redirect('appointment_list')
    return render(request, 'patients/appointment_confirm_delete.html', {'appointment': appointment})

@login_required
def appointment_api(request):
    appointments = Appointment.objects.filter(therapist=request.user)
    events = [
        {
            'title': f"{appointment.patient.first_name} {appointment.patient.last_name}",
            'start': appointment.date_time.isoformat(),
            'end': (appointment.date_time + timedelta(hours=1)).isoformat(),  # Randevu süresi 1 saat
        }
        for appointment in appointments
    ]
    return JsonResponse(events, safe=False)

@login_required
def calendar_view(request):
    return render(request, 'patients/calendar.html')

@login_required
def report_view(request):
    # Son bir hafta içindeki randevular
    one_week_ago = now() - timedelta(days=7)
    appointments_last_week = Appointment.objects.filter(date_time__gte=one_week_ago)

    # Terapist başına randevu sayısı
    appointments_by_therapist = appointments_last_week.values('therapist__username').annotate(total=Count('id')).order_by('-total')

    return render(request, 'patients/reports.html', {
    'appointments_by_therapist': appointments_by_therapist,
    'appointments_last_week': appointments_last_week
})

@login_required
def report_view(request):
    # Son 7 günü hesaplayın
    seven_days_ago = now() - timedelta(days=7)

    # Terapist başına randevu sayısını alın
    appointments_by_therapist = (
        Appointment.objects.filter(date_time__gte=seven_days_ago)  # Hata düzeltildi
        .values('therapist__username')
        .annotate(total=Count('id'))
    )

    # İsim ve toplam sayıları ayrı listelere ayırın
    labels = [item['therapist__username'] for item in appointments_by_therapist]
    data = [item['total'] for item in appointments_by_therapist]

    context = {
        'appointments_by_therapist': appointments_by_therapist,
        'labels': mark_safe(json.dumps(labels)),
        'data': mark_safe(json.dumps(data)),  # JSON formatı
    }
    return render(request, 'patients/reports.html', context)

@login_required
def advanced_report_view(request):
    # Son 30 günü hesaplayın
    thirty_days_ago = now() - timedelta(days=30)

    # Günlük randevu sayısını hesaplayın
    daily_appointments = (
        Appointment.objects.filter(date_time__gte=thirty_days_ago)
        .annotate(day=TruncDay('date_time'))
        .values('day')
        .annotate(total=Count('id'))
        .order_by('day')
    )

    # Gün ve toplam sayıları ayırın
    labels = [item['day'].strftime('%Y-%m-%d') for item in daily_appointments]
    data = [item['total'] for item in daily_appointments]

    context = {
        'labels': mark_safe(json.dumps(labels)),
        'data': mark_safe(json.dumps(data)),
    }
    return render(request, 'patients/advanced_reports.html', context)

@login_required
def therapist_performance_view(request):
    performance_data = (
        Appointment.objects.values('therapist__username', 'status')
        .annotate(total=Count('id'))
        .order_by('therapist__username', 'status')
    )

    # Kullanıcıya sunulacak veri
    labels = list(set([item['therapist__username'] for item in performance_data]))
    status_data = {
        'scheduled': [],
        'completed': [],
        'cancelled': []
    }

    for label in labels:
        for status in status_data.keys():
            status_data[status].append(
                next(
                    (item['total'] for item in performance_data
                     if item['therapist__username'] == label and item['status'] == status),
                    0
                )
            )

    context = {
        'labels': labels,
        'status_data': status_data,
    }
    return render(request, 'patients/therapist_performance.html', context)