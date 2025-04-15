from django.urls import path, include
from rest_framework.routers import DefaultRouter
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
    path('', include(router.urls)),
    path('dynamic/categories/', get_categories_by_type, name='get_categories_by_type'),
    path('dynamic/subcategories/', get_subcategories_by_category, name='get_subcategories_by_category'),
    path('', include(router.urls)),
]