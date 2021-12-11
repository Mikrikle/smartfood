from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import IngredientItem, IngredientInfo, DishItem, DishInfo, DishCategory, IngredientCategory

admin.site.site_title = "Smart food"
admin.site.site_header = "Smart food"

@admin.register(DishCategory)
class DishCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "description")
    exclude = ('url', )


@admin.register(IngredientCategory)
class IngredientCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "description")
    exclude = ('url', )

#-------------------------------------------------------------
@admin.register(IngredientItem)
class IngredientItemAdmin(admin.ModelAdmin):
    list_display = ("name", "visionname", "category", "get_image",
     "calories", "fats", "carbohydrates", "proteins" )
    exclude = ('url', )
    readonly_fields = ("get_image",)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.img.url} width="64" height="64"')

    get_image.short_description = "Изображение"


@admin.register(DishItem)
class DishItemAdmin(admin.ModelAdmin):
    list_display = ("name", "visionname", "category", "get_image",
     "calories", "fats", "carbohydrates", "proteins" )
    exclude = ('url', )
    readonly_fields = ("get_image",)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.img.url} width="64" height="64"')

    get_image.short_description = "Изображение"

#-------------------------------------------------------------
@admin.register(IngredientInfo)
class IngredientInfoAdmin(admin.ModelAdmin):
    list_display = ("owner", "date", "food", "weight")


@admin.register(DishInfo)
class DishInfoAdmin(admin.ModelAdmin):
    list_display = ("owner", "date", "food", "weight")