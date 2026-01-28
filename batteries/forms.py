from django import forms
from .models import BatterySubmission, RecyclableType


class BatterySubmissionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Показываем только активные типы материалов
        self.fields['recyclable_type'].queryset = RecyclableType.objects.filter(is_active=True)
        self.fields['recyclable_type'].label_from_instance = lambda obj: f"{obj.icon} {obj.name}"
    
    class Meta:
        model = BatterySubmission
        fields = ['recyclable_type', 'quantity', 'city', 'comment']
        widgets = {
            'recyclable_type': forms.Select(attrs={
                'class': 'form-control',
            }),
            'quantity': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите количество',
                'min': '1'
            }),
            'city': forms.Select(attrs={
                'class': 'form-control',
            }),
            'comment': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Комментарий (необязательно)',
                'rows': 3
            }),
        }
        labels = {
            'recyclable_type': 'Что сдаете?',
            'quantity': 'Количество',
            'city': 'Город',
            'comment': 'Комментарий',
        }
