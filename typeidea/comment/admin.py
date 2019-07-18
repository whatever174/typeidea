from django.contrib import admin
from .models import Comment
from typeidea.base_admin import BaseOwnerAdmin
from typeidea.custom_site import custom_site


# Register your models here.
@admin.register(Comment, site=custom_site)
class CommentAdmin(BaseOwnerAdmin):
    list_display = (
        'target', 'nickname', 'content', 'website', 'created_time'
    )

    def save_model(self, request, obj, form, change):
        obj.nickname = request.user
        return super(BaseOwnerAdmin, self).save_model(request, obj, form, change)

    def get_queryset(self, request):
        qs = super(BaseOwnerAdmin, self).get_queryset(request)
        return qs.filter(nickname=request.user)
