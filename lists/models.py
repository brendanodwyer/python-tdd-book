from django.conf import settings
from django.db import models
from django.urls import reverse


class List(models.Model):

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.CASCADE
    )

    def get_absolute_url(self):
        return reverse("view_list", args=[self.id])

    @staticmethod
    def create_new(first_item_text, owner=None):
        new_list = List.objects.create(owner=owner)
        Item.objects.create(text=first_item_text, list=new_list)
        return new_list

    @property
    def name(self):
        return self.item_set.first().text


class Item(models.Model):
    text = models.TextField(default="")
    list = models.ForeignKey(List, on_delete=models.CASCADE, default=None)

    class Meta:
        ordering = ("id",)
        unique_together = ("list", "text")

    def __str__(self) -> str:
        return self.text
