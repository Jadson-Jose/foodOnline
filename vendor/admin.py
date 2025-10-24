from django.contrib import admin

from vendor import models

# Register your models here.


class VendorAdmin(admin.ModelAdmin):
    list_display = ("user", "vendor_name", "is_approved", "created_at")
    list_display_links = ("user", "vendor_name")


admin.site.register(models.Vendor, VendorAdmin)
