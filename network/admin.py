from django.contrib import admin
from network.models import User, Post

class PostAdmin(admin.ModelAdmin):
    readonly_fields = ('timestamp', "edited_at",)
    list_display = ('owner', 'timestamp', 'text', "edited_at",)

# Register your models here.
admin.site.register(User)
admin.site.register(Post, PostAdmin)
