from rest_framework import serializers
from .models import Status, Type, Category, Subcategory, CashflowEntry

class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = '__all__'

class TypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Type
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class SubcategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Subcategory
        fields = '__all__'

class CashflowEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = CashflowEntry
        fields = '__all__'

    def validate(self, data):
        """
        Кастомная бизнес-валидация:
        - Подкатегория должна соответствовать выбранной категории
        - Категория должна соответствовать выбранному типу
        """
        category = data.get('category')
        subcategory = data.get('subcategory')
        type_ = data.get('type')

        if subcategory and subcategory.category != category:
            raise serializers.ValidationError("Выбранная подкатегория не принадлежит выбранной категории.")

        if category and category.type != type_:
            raise serializers.ValidationError("Выбранная категория не принадлежит выбранному типу.")

        return data