from django.contrib import admin

from admin_app.models import ExternalUser


@admin.register(ExternalUser)
class ExternalUserAdmin(admin.ModelAdmin):
    list_display = ("username", "empresa", "activo", "updated_hint")
    list_display_links = ("username",)
    list_filter = ("activo", "empresa")
    search_fields = ("username", "empresa")
    list_editable = ("activo",)
    ordering = ("username",)
    list_per_page = 50
    save_on_top = True
    fieldsets = (
        (None, {"fields": ("username", "password_plain", "empresa", "activo")}),
    )

    @admin.display(description="Contraseña")
    def updated_hint(self, obj):
        if not obj.password_plain:
            return "—"
        p = obj.password_plain
        return "•" * min(len(p), 12) + ("…" if len(p) > 12 else "")


admin.site.site_header = "ReMASA ID — Administración"
admin.site.site_title = "ReMASA ID"
admin.site.index_title = "Gestión de usuarios externos"
