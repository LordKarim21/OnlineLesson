from django.db import models
from django.contrib.auth.models import User


class Product(models.Model):
    title = models.CharField(max_length=128)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owner')
    users = models.ManyToManyField(User, related_name='permitted_users')
    lessons = models.ManyToManyField('Lesson')

    def get_permitted_count(self):
        return self.users.count()

    def __str__(self):
        return f"Product <{self.title}>"


class Viewer(models.Model):
    VIEWED = 0
    NOT_VIEWED = 1
    STATUS_CHOICES = ((VIEWED, "Просмотрено"), (NOT_VIEWED, "Не просмотрено"))

    status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES, default=NOT_VIEWED)
    viewing_seconds = models.PositiveIntegerField()

    lesson = models.ForeignKey('Lesson', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

    viewed_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["viewed_at"]

    def set_status(self):
        duration_seconds = self.lesson.duration_seconds
        if self.viewing_seconds >= duration_seconds:
            raise Exception("More duration_seconds")
        if self.viewing_seconds / duration_seconds * 100 < 80:
            self.status = self.VIEWED
            self.save()


class Lesson(models.Model):
    viewers = models.ManyToManyField(Viewer, related_name='user_view')
    title = models.CharField(max_length=255)
    video_link = models.URLField()
    duration_seconds = models.PositiveIntegerField()

    def __str__(self):
        return f"Lesson <{self.title}>"
