# Инструкция по развертыванию на Google Cloud Run через GitHub

## Предварительные требования

1. Аккаунт Google Cloud Platform
2. Установленный Firebase CLI (необязательно)
3. Репозиторий на GitHub

## Шаг 1: Настройка Google Cloud Project

1. Перейдите на https://console.cloud.google.com/
2. Создайте новый проект или выберите существующий
3. Запомните Project ID (например: `my-project-123`)

## Шаг 2: Включение необходимых API

Включите следующие API в консоли:
- Cloud Run API
- Container Registry API
- Cloud Build API

Или через командную строку:
```bash
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com
gcloud services enable cloudbuild.googleapis.com
```

## Шаг 3: Создание Service Account

1. В консоли GCP перейдите в IAM & Admin > Service Accounts
2. Создайте новый Service Account
3. Добавьте роли:
   - Cloud Run Admin
   - Storage Admin
   - Service Account User
4. Создайте JSON ключ и скачайте его

## Шаг 4: Настройка GitHub Secrets

Добавьте следующие секреты в Settings > Secrets > Actions вашего репозитория:

- `GCP_PROJECT_ID` - ID вашего проекта GCP
- `GCP_SA_KEY` - содержимое скачанного JSON ключа
- `DJANGO_SECRET_KEY` - секретный ключ Django (сгенерируйте новый!)

Для генерации Django secret key:
```python
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

## Шаг 5: Push в GitHub

```bash
git add .
git commit -m "Add Cloud Run deployment configuration"
git push origin main
```

GitHub Action автоматически:
1. Соберет Docker образ
2. Загрузит его в Google Container Registry
3. Развернет на Cloud Run

## Шаг 6: После деплоя

1. Перейдите в Cloud Console > Cloud Run
2. Найдите ваш сервис
3. Скопируйте URL (например: https://battery-recycling-xxx-uc.a.run.app)

## Шаг 7: Выполнение миграций

После первого деплоя нужно выполнить миграции:

```bash
gcloud run services update battery-recycling \
  --region us-central1 \
  --command="python,manage.py,migrate"
```

Или через Cloud Shell:
```bash
gcloud run jobs execute migrate-db --region us-central1
```

## Локальное тестирование Docker

Перед деплоем можно протестировать локально:

```bash
docker build -t battery-app .
docker run -p 8080:8080 -e PORT=8080 -e DEBUG=True battery-app
```

Откройте http://localhost:8080

## Настройка домена

1. В Cloud Run выберите ваш сервис
2. Перейдите во вкладку "Manage Custom Domains"
3. Добавьте свой домен
4. Настройте DNS записи согласно инструкциям

## Мониторинг и логи

Логи доступны в:
- Cloud Console > Cloud Run > Logs
- Или через командную строку:
```bash
gcloud run services logs tail battery-recycling --region us-central1
```

## Обновление приложения

Просто сделайте push в main ветку - GitHub Action автоматически развернет обновление:

```bash
git add .
git commit -m "Update application"
git push origin main
```

## Масштабирование

Cloud Run автоматически масштабируется от 0 до N экземпляров в зависимости от трафика.

Настроить можно в консоли или через gcloud:
```bash
gcloud run services update battery-recycling \
  --region us-central1 \
  --min-instances=0 \
  --max-instances=10
```

## Стоимость

Cloud Run взимает плату только за время работы. Есть бесплатный лимит:
- 2 миллиона запросов в месяц
- 360,000 GB-секунд памяти
- 180,000 vCPU-секунд

Для малого проекта это практически бесплатно!
