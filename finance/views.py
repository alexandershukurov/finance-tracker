from rest_framework import viewsets
from .models import Status, Type, Category, Subcategory, CashflowEntry
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import render, redirect
from .models import CashflowEntry, Status, Type, Category, Subcategory
from .forms import TypeForm, StatusForm, CategoryForm, SubcategoryForm
from .forms import CashflowEntryForm
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.apps import apps
from django.http import HttpResponseNotFound
from django.shortcuts import get_object_or_404, redirect, render
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
@require_GET
def manage_view(request):
    types = Type.objects.all()
    statuses = Status.objects.all()
    categories = Category.objects.select_related('type').all()
    subcategories = Subcategory.objects.select_related('category').all()

    type_form = TypeForm(request.POST or None, prefix='type')
    status_form = StatusForm(request.POST or None, prefix='status')
    category_form = CategoryForm(request.POST or None, prefix='category')
    subcategory_form = SubcategoryForm(request.POST or None, prefix='subcategory')

    if request.method == 'POST':
        if 'submit_type' in request.POST and type_form.is_valid():
            type_form.save()
            return redirect('manage')
        if 'submit_status' in request.POST and status_form.is_valid():
            status_form.save()
            return redirect('manage')
        if 'submit_category' in request.POST and category_form.is_valid():
            category_form.save()
            return redirect('manage')
        if 'submit_subcategory' in request.POST and subcategory_form.is_valid():
            subcategory_form.save()
            return redirect('manage')

    return render(request, 'finance/manage.html', {
        'types': types,
        'statuses': statuses,
        'categories': categories,
        'subcategories': subcategories,
        'type_form': type_form,
        'status_form': status_form,
        'category_form': category_form,
        'subcategory_form': subcategory_form,
    })
    
MODEL_MAP = {
    'type': Type,
    'status': Status,
    'category': Category,
    'subcategory': Subcategory
}
def edit_item(request, model, pk):
    if model not in MODEL_MAP:
        return HttpResponseNotFound("Unknown model.")

    ModelClass = MODEL_MAP[model]
    instance = get_object_or_404(ModelClass, pk=pk)

    # Формы соответствующие
    FormClass = {
        'type': TypeForm,
        'status': StatusForm,
        'category': CategoryForm,
        'subcategory': SubcategoryForm
    }[model]

    if request.method == 'POST':
        form = FormClass(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return redirect('manage')
    else:
        form = FormClass(instance=instance)

    return render(request, 'finance/edit_item.html', {
        'form': form,
        'model_name': model
    })

def delete_item(request, model, pk):
    if model not in MODEL_MAP:
        return HttpResponseNotFound("Unknown model.")

    ModelClass = MODEL_MAP[model]
    instance = get_object_or_404(ModelClass, pk=pk)

    if request.method == 'POST':
        instance.delete()
        return redirect('manage')

    return render(request, 'finance/delete_item.html', {
        'object': instance,
        'model_name': model
    })
def delete_entry(request, pk):
    entry = get_object_or_404(CashflowEntry, pk=pk)
    if request.method == 'POST':
        entry.delete()
        return redirect('index')
    return render(request, 'finance/delete_entry.html', {'entry': entry})