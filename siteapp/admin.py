from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import FoodItem, FoodCategory, FoodInfo

admin.site.site_title = "Smart food"
admin.site.site_header = "Smart food"


@admin.register(FoodCategory)
class IngredientCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "description")
    exclude = ('url', )

#-------------------------------------------------------------
@admin.register(FoodItem)
class IngredientItemAdmin(admin.ModelAdmin):
    list_display = ("name", "visionname",  "isIngredient", "category",
     "get_image", "calories", "fats", "carbohydrates", "proteins" )
    exclude = ('url', )
    readonly_fields = ("get_image",)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.img.url} width="64" height="64"')

    get_image.short_description = "Текущее изображение"

#-------------------------------------------------------------
@admin.register(FoodInfo)
class IngredientInfoAdmin(admin.ModelAdmin):
    list_display = ("owner", "date", "food", "weight")
