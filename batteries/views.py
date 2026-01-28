from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.db.models import Sum
from .models import BatterySubmission, RecyclableType
from .forms import BatterySubmissionForm
import json


def home(request):
    """Главная страница с общей статистикой"""
    total_batteries = BatterySubmission.objects.aggregate(
        total=Sum('quantity')
    )['total'] or 0
    
    recent_submissions = BatterySubmission.objects.all()[:10]
    total_users = BatterySubmission.objects.values('user').distinct().count()
    
    # Статистика по типам материалов для диаграммы
    stats_by_type = BatterySubmission.objects.values(
        'recyclable_type__name',
        'recyclable_type__icon',
        'recyclable_type__unit'
    ).annotate(
        total=Sum('quantity')
    ).order_by('-total')
    
    # Подготовка данных для Chart.js
    chart_labels = [f"{item['recyclable_type__icon']} {item['recyclable_type__name']}" for item in stats_by_type]
    chart_data = [item['total'] for item in stats_by_type]
    
    context = {
        'total_batteries': total_batteries,
        'recent_submissions': recent_submissions,
        'total_users': total_users,
        'stats_by_type': stats_by_type,
        'chart_labels': json.dumps(chart_labels),
        'chart_data': json.dumps(chart_data),
    }
    return render(request, 'batteries/home.html', context)


@login_required
def submit_batteries(request):
    """Форма для сдачи вторсырья"""
    if request.method == 'POST':
        form = BatterySubmissionForm(request.POST)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.user = request.user
            submission.save()
            messages.success(request, f'Спасибо! Вы сдали {submission.recyclable_type.name}: {submission.quantity} {submission.recyclable_type.unit}')
            return redirect('home')
    else:
        form = BatterySubmissionForm()
    
    return render(request, 'batteries/submit.html', {'form': form})


@login_required
def my_submissions(request):
    """Личная статистика пользователя"""
    submissions = BatterySubmission.objects.filter(user=request.user)
    total = submissions.aggregate(total=Sum('quantity'))['total'] or 0
    
    context = {
        'submissions': submissions,
        'total': total,
    }
    return render(request, 'batteries/my_submissions.html', context)


def register(request):
    """Регистрация нового пользователя"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Регистрация прошла успешно!')
            return redirect('home')
    else:
        form = UserCreationForm()
    
    return render(request, 'registration/register.html', {'form': form})
