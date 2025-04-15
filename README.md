# Финансовый трекер (Тестовое задание)

Тестовое задание на позицию backend-разработчика. Реализовано на Django + DRF.

## Функциональность

- Учёт движения денежных средств
- CRUD для записей
- Фильтрация по дате, типу, статусу, категориям
- Управление справочниками
- Django Admin
- REST API + Swagger документация
- Форма добавления с зависимыми выпадающими списками

---

## Стек

- Python 3.12
- Django 5.2
- Django REST Framework
- Bootstrap 5
- drf-spectacular (Swagger)

---

## Установка

```bash
git clone <репозиторий>
cd finance_tracker
pip install -r requirements.txt
python manage.py migrate
python manage.py loaddata fixtures.json
python manage.py runserver