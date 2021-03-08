from django.db import models
from django.utils import timezone

from livefield import LiveField


class BaseModel(models.Model):
    created_at = models.DateTimeField('作成日', auto_now_add=True)
    updated_at = models.DateTimeField('更新日', auto_now=True)
    live = LiveField()

    class Meta:
        abstract = True
    
    def delete(self, using=None):
        self.live = False
        self.save(using=using)

    def hard_delete(self):
        self.delete()