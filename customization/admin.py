from django.contrib import admin

from .models import RepairWork, ModeOfPayment, Warranty, ItemCondition


display_items = ('description', 'created_at', 'updated_at')
search_items = ('description',)
filter_items = ('created_at', 'updated_at')


@admin.register(RepairWork)
class RepairWorkAdmin(admin.ModelAdmin):
    list_display = display_items
    search_fields = search_items
    list_filter = filter_items


@admin.register(ModeOfPayment)
class ModeOfPaymentAdmin(admin.ModelAdmin):
    list_display = display_items
    search_fields = search_items
    list_filter = filter_items


@admin.register(Warranty)
class WarrantyAdmin(admin.ModelAdmin):
    list_display = display_items
    search_fields = search_items
    list_filter = filter_items


@admin.register(ItemCondition)
class ItemConditionAdmin(admin.ModelAdmin):
    list_display = display_items
    search_fields = search_items
    list_filter = filter_items
