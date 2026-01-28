from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from batteries.models import RecyclableType


class Command(BaseCommand):
    help = 'Инициализация начальных данных'

    def handle(self, *args, **options):
        # Создаем суперпользователя если его нет
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
            self.stdout.write(self.style.SUCCESS('✅ Суперпользователь admin создан (пароль: admin123)'))
        else:
            self.stdout.write(self.style.WARNING('⚠️ Суперпользователь admin уже существует'))

        # Создаем типы материалов если их нет
        recyclable_types = [
            {'name': 'Батарейки', 'unit': 'шт', 'icon': '🔋', 'description': 'Использованные батарейки и аккумуляторы'},
            {'name': 'Стекло', 'unit': 'кг', 'icon': '🍾', 'description': 'Стеклянные бутылки и банки'},
            {'name': 'Пластик', 'unit': 'кг', 'icon': '♻️', 'description': 'Пластиковые бутылки и упаковка'},
            {'name': 'Бумага', 'unit': 'кг', 'icon': '📄', 'description': 'Макулатура, картон, газеты'},
            {'name': 'Металл', 'unit': 'кг', 'icon': '🥫', 'description': 'Алюминиевые банки и металлолом'},
        ]

        created_count = 0
        for rt_data in recyclable_types:
            rt, created = RecyclableType.objects.get_or_create(
                name=rt_data['name'],
                defaults={
                    'unit': rt_data['unit'],
                    'icon': rt_data['icon'],
                    'description': rt_data['description'],
                    'is_active': True
                }
            )
            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f'✅ Создан тип: {rt.icon} {rt.name}'))

        if created_count == 0:
            self.stdout.write(self.style.WARNING('⚠️ Все типы материалов уже существуют'))
        else:
            self.stdout.write(self.style.SUCCESS(f'✅ Создано типов материалов: {created_count}'))
