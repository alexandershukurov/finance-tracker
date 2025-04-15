from django.urls import path, include
from django.contrib import admin
from rest_framework.routers import DefaultRouter
from finance.views import index, add_entry, manage_view, edit_item, delete_item, delete_entry
from .views import (
    StatusViewSet,
    TypeViewSet,
    CategoryViewSet,
    SubcategoryViewSet,
    CashflowEntryViewSet,
    StatusViewSet, TypeViewSet, CategoryViewSet, SubcategoryViewSet, CashflowEntryViewSet,
    get_categories_by_type, get_subcategories_by_category,
)

router = DefaultRouter()
router.register(r'statuses', StatusViewSet)
router.register(r'types', TypeViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'subcategories', SubcategoryViewSet)
router.register(r'entries', CashflowEntryViewSet)

urlpatterns = [
    path('dynamic/categories/', get_categories_by_type, name='get_categories_by_type'),
    path('dynamic/subcategories/', get_subcategories_by_category, name='get_subcategories_by_category'),
    path('', include(router.urls)),
]
urlpatterns += [
    path('manage/edit/<str:model>/<int:pk>/', edit_item, name='edit_item'),
    path('manage/delete/<str:model>/<int:pk>/', delete_item, name='delete_item'),
    path('delete-entry/<int:pk>/', delete_entry, name='delete_entry'),
]