from django.contrib import admin
from django.utils.html import format_html
from .models import Plat, ProduitMarche, Cuisinier, Commande, ReservationCuisinier, Vin, Publicite

# Admin pour Plat avec image miniature
@admin.register(Plat)
class PlatAdmin(admin.ModelAdmin):
    list_display = ('nom', 'prix', 'vin_recommande', 'image_tag')
    search_fields = ('nom',)
    list_filter = ('vin_recommande',)

    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 50px;" />', obj.image.url)
        return "-"
    image_tag.short_description = 'Image'

# Admin pour ProduitMarche avec image miniature
@admin.register(ProduitMarche)
class ProduitMarcheAdmin(admin.ModelAdmin):
    list_display = ('nom', 'prix', 'image_tag')
    search_fields = ('nom',)

    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 50px;" />', obj.image.url)
        return "-"
    image_tag.short_description = 'Image'

# Admin pour Cuisinier avec image miniature et filtre disponibilité
@admin.register(Cuisinier)
class CuisinierAdmin(admin.ModelAdmin):
    list_display = ('nom', 'prix', 'disponible', 'image_tag')
    list_filter = ('disponible',)
    search_fields = ('nom',)

    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 50px;" />', obj.image.url)
        return "-"
    image_tag.short_description = 'Image'

# Admin pour Vin avec image miniature
@admin.register(Vin)
class VinAdmin(admin.ModelAdmin):
    list_display = ('nom', 'prix', 'image_tag')
    search_fields = ('nom',)

    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 50px;" />', obj.image.url)
        return "-"
    image_tag.short_description = 'Image'

# Admin pour Commande avec liste et filtres
 
@admin.register(Commande)
class CommandeAdmin(admin.ModelAdmin):
    list_display = ('id', 'nom_client', 'telephone', 'statut', 'date_commande')
    list_filter = ('statut', 'date_commande')
    search_fields = ('nom_client', 'telephone', 'email')
    list_editable = ('statut',)
# Admin pour ReservationCuisinier
@admin.register(ReservationCuisinier)
class ReservationCuisinierAdmin(admin.ModelAdmin):
    list_display = ('client', 'cuisinier', 'date', 'heure', 'lieu')
    list_filter = ('date',)
    search_fields = ('client__username', 'cuisinier__nom')

# Actions pour Publicite
@admin.action(description='Activer les publicités sélectionnées')
def activer_publicites(modeladmin, request, queryset):
    queryset.update(actif=True)

@admin.action(description='Désactiver les publicités sélectionnées')
def desactiver_publicites(modeladmin, request, queryset):
    queryset.update(actif=False)

# Admin pour Publicite avec image miniature et actions
@admin.register(Publicite)
class PubliciteAdmin(admin.ModelAdmin):
    list_display = ('titre', 'actif', 'image_tag')
    list_filter = ('actif',)
    actions = [activer_publicites, desactiver_publicites]

    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 50px;" />', obj.image.url)
        return "-"
    image_tag.short_description = 'Image'
