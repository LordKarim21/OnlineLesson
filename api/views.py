from . import serializers
from .models import (Lesson, Product, Viewer)
from .permissions import IsProductOwner, HasAccessToProductORIsProductOwner

from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.mixins import UpdateModelMixin
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from django.db.models import Sum, Count
from django.db.models.functions import Coalesce


class LessonViewSet(viewsets.ReadOnlyModelViewSet, UpdateModelMixin):
    serializer_class = serializers.LessonDetailSerializer
    queryset = Lesson.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.LessonListSerializer
        else:
            return serializers.LessonDetailSerializer

    def update(self, request, *args, **kwargs):
        lesson = self.get_object()
        viewing_seconds = request.data.get('viewing_seconds')
        user = request.user
        queryset = Viewer.objects.filter(user=user)
        if queryset.exists():
            viewer = queryset.first()
            viewer.viewing_seconds = viewing_seconds
        else:
            lesson = self.get_object()
            viewer = Viewer.objects.create(
                viewing_seconds=viewing_seconds,
                lesson=lesson,
                user=user
            )
        viewer.set_status()
        viewer.save()
        lesson.viewers.add(viewer)
        lesson.save()
        return super().retrieve(request, *args, **kwargs)


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = (HasAccessToProductORIsProductOwner, )
    queryset = Product.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.ProductListSerializer
        else:
            return serializers.ProductDetailSerializer


class ProductStatsModelViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = serializers.ProductStatsSerializer
    permission_classes = (IsAdminUser, IsProductOwner, )

    def list(self, request, *args, **kwargs):
        all_users = User.objects.count()
        products = self.get_queryset()

        product_stats = []
        for product in products:
            total_lessons_viewed = Viewer.objects.filter(lesson__in=product.lessons.all()).count()
            total_viewing_time_seconds = Viewer.objects.filter(lesson__in=product.lessons.all()).aggregate(
                total_viewing_time_seconds=Coalesce(Sum('viewing_seconds'), 0))['total_viewing_time_seconds']
            total_students = product.users.count()

            purchase_percentage = (product.get_permitted_count() / all_users) * 100 if all_users != 0 else 0

            product_stat = {
                'id': product.id,
                'title': product.title,
                'total_lessons_viewed': total_lessons_viewed,
                'total_viewing_time_seconds': total_viewing_time_seconds,
                'total_students': total_students,
                'purchase_percentage': round(purchase_percentage, 2),
            }
            product_stats.append(product_stat)

        return Response(product_stats)
