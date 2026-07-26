from rest_framework import serializers

from .models import Service


class ServiceSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(
        source="category.name",
        read_only=True,
    )

    class Meta:
        model = Service

        fields = [
            "id",
            "name",
            "description",
            "category",
            "category_name",
            "duration_minutes",
            "price",
            "is_active",
            "clinic",
        ]

        read_only_fields = [
            "id",
            "clinic",
            "category_name",
        ]