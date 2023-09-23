from rest_framework import serializers
from django.utils import timezone

from .models import (Lesson, Product, Viewer,)


class ViewerDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Viewer
        fields = ('status', 'viewing_seconds', 'viewed_at')

    # def _get_distance(self, obj):
    #     return obj.get_distance(user=self.context['request'].user)


class LessonDetailSerializer(serializers.ModelSerializer):
    viewers = ViewerDetailSerializer(read_only=True, many=True)

    class Meta:
        model = Lesson
        fields = ('title', 'video_link', 'duration_seconds', 'viewers')


class ViewerListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Viewer
        fields = ('status', 'viewing_seconds')

    # def _get_distance(self, obj):
    #     return obj.get_distance(user=self.context['request'].user)


class LessonListSerializer(serializers.ModelSerializer):
    viewers = ViewerListSerializer(read_only=True, many=True)

    class Meta:
        model = Lesson
        fields = ('title', 'video_link', 'duration_seconds', 'viewers')


class ProductDetailSerializer(serializers.ModelSerializer):
    lessons = LessonDetailSerializer(read_only=True, many=True)

    class Meta:
        model = Product
        fields = ('title', 'lessons')


class ProductListSerializer(serializers.ModelSerializer):
    lessons = LessonListSerializer(read_only=True, many=True)

    class Meta:
        model = Product
        fields = ('title', 'lessons')


class ProductStatsSerializer(serializers.ModelSerializer):
    total_lessons_viewed = serializers.IntegerField()
    total_viewing_time_seconds = serializers.IntegerField()
    total_students = serializers.IntegerField()
    purchase_percentage = serializers.FloatField()

    class Meta:
        model = Product
        fields = ('id', 'title', 'total_lessons_viewed', 'total_viewing_time_seconds', 'total_students', 'purchase_percentage')
