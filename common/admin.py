from django.contrib import admin

# Register your models here.
from common.models import Province, City, Category, Skill


@admin.register(Province)
class ProvinceAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]
    list_display_links = ["id", "name"]
    search_fields = ["id", "name"]


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "province"]
    list_display_links = ["id", "name"]
    search_fields = ["id", "name", "province"]

    def province(self, obj: City):
        try:
            return obj.province.id
        except AttributeError:
            return None


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]
    list_display_links = ["id", "name"]
    search_fields = ["id", "name"]


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]
    list_display_links = ["id", "name"]
    search_fields = ["id", "name"]
