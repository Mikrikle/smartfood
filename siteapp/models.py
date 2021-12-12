from datetime import timezone
from django.db import models
from django.contrib.auth.models import User
from django.db.models.base import Model
from django.utils import timezone
from django.urls import reverse
from django.utils.text import slugify
from time import time
from PIL import Image
import pytils.translit
import os



def gen_slug(s):
    text = pytils.translit.translify(s)
    new_slug = slugify(text, allow_unicode=False)
    return 'n-' + new_slug + '-' + str(int(time()))


#------------------------------------------------------------------
class FoodCategory(models.Model):
    """Категории еды"""
    name = models.CharField("Категория", max_length=150)
    description = models.TextField("Описание")
    url = models.SlugField(max_length=160, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории еды"

    def save(self, *args, **kwargs):
        if not self.id:
            self.url = gen_slug(self.name)
        super().save(*args, **kwargs)



#------------------------------------------------------------------
class FoodItem(models.Model):
    """Еда"""
    name = models.CharField("Название", max_length=150)
    visionname = models.CharField("Обозначение в CustomVision", max_length=150, blank=True)
    isIngredient = models.BooleanField("Может использоваться в качестве ингредиента")
    isEatable = models.BooleanField("Готово к употреблению")
    ingredients = models.ManyToManyField('self', blank=True, verbose_name="Ингредиенты")
    img = models.ImageField("Изображение", upload_to = "img/food")
    url = models.SlugField(max_length=160, unique=True)
    category = models.ForeignKey(
        FoodCategory, verbose_name="Категория", on_delete=models.SET_NULL, null=True
    )
    calories = models.PositiveIntegerField("Калории", default=10)
    fats = models.FloatField("Жиры (г)", default=0)
    carbohydrates = models.FloatField("Углеводы (г)", default=0)
    proteins = models.FloatField("Белки (г)", default=0)

    def save(self, *args, **kwargs):
        if not self.id:
            self.url = gen_slug(self.name)
        super().save(*args, **kwargs)

        img = Image.open(self.img.path)

        if img.height > 512 or img.width > 512:
            new_img = (512, 512)
            img.thumbnail(new_img)
            img.save(self.img.path)

    class Meta:
        verbose_name = "Еда"
        verbose_name_plural = "Список еды"
        ordering = ["name"]

    def __str__(self):
        return str(self.name)
    
    def get_absolute_url(self):
        return reverse("dish_detail", kwargs={"slug": self.url})

    def as_json(self):
        return dict(
            name=self.name, 
            visionname=self.visionname,
        )


#------------------------------------------------------------------
class FoodInfo(models.Model):
    """персональная информация про еду"""
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    food = models.ForeignKey(FoodItem, on_delete=models.CASCADE, verbose_name="Еда")
    date = models.DateTimeField("Дата", default=timezone.now)
    weight = models.PositiveIntegerField("Вес (г)", default=100)

    class Meta:
        verbose_name = "Персональная информация о еде"
        verbose_name_plural = "Персональная информация о еде"

    def __str__(self):
        return str(self.owner.username + ": " + self.food.name)


