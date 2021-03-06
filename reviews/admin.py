from django.contrib import admin

from reviews.models import Review, Strain, Comment
# Register your models here.


class ReviewModelAdmin(admin.ModelAdmin):
    list_display = ["title", "user", "strain", "rating", "timestamp", "photo"]
    list_display_links = ["title"]
    list_filter = ["strain", "user", "rating"]

    class Meta:
        model = Review


class StrainModelAdmin(admin.ModelAdmin):
    list_display = ["name", "genetics", "lineage", "photo_url"]
    list_display_links = ["name"]
    search_fields = ["name"]

    class Meta:
        model = Strain


class CommentModelAdmin(admin.ModelAdmin):
    list_display = ["user", "review", "created", "active"]
    list_filter = ["active", "created", "updated"]
    search_fields = ["user", "body"]

    class Meta:
        model = Comment


admin.site.register(Review, ReviewModelAdmin)
admin.site.register(Strain, StrainModelAdmin)
admin.site.register(Comment, CommentModelAdmin)
