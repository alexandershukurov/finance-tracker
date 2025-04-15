from rest_framework import viewsets
from .models import Status, Type, Category, Subcategory, CashflowEntry
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import render, redirect
from .models import CashflowEntry, Status, Type
from .forms import CashflowEntryForm
from django.http import JsonResponse
from .models import Category, Subcategory
from .serializers import (
    StatusSerializer,
    TypeSerializer,
    CategorySerializer,
    SubcategorySerializer,
    CashflowEntrySerializer,
)

class StatusViewSet(viewsets.ModelViewSet):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer

class TypeViewSet(viewsets.ModelViewSet):
    queryset = Type.objects.all()
    serializer_class = TypeSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class SubcategoryViewSet(viewsets.ModelViewSet):
    queryset = Subcategory.objects.all()
    serializer_class = SubcategorySerializer

class CashflowEntryViewSet(viewsets.ModelViewSet):
    queryset = CashflowEntry.objects.all()
    serializer_class = CashflowEntrySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status', 'type', 'category', 'subcategory', 'date']

def index(request):
    entries = CashflowEntry.objects.all()

    date_from = request.GET.get("date_from")
    date_to = request.GET.get("date_to")
    status = request.GET.get("status")
    type_ = request.GET.get("type")

    if date_from:
        entries = entries.filter(date__gte=date_from)
    if date_to:
        entries = entries.filter(date__lte=date_to)
    if status:
        entries = entries.filter(status_id=status)
    if type_:
        entries = entries.filter(type_id=type_)

    statuses = Status.objects.all()
    types = Type.objects.all()

    return render(request, "finance/index.html", {
        "entries": entries,
        "statuses": statuses,
        "types": types,
    })
def add_entry(request):
    if request.method == 'POST':
        form = CashflowEntryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = CashflowEntryForm()

    return render(request, 'finance/add_entry.html', {'form': form})
def get_categories_by_type(request):
    type_id = request.GET.get('type_id')
    categories = Category.objects.filter(type_id=type_id).values('id', 'name')
    return JsonResponse(list(categories), safe=False)

def get_subcategories_by_category(request):
    category_id = request.GET.get('category_id')
    subcategories = Subcategory.objects.filter(category_id=category_id).values('id', 'name')
    return JsonResponse(list(subcategories), safe=False)