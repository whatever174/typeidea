from django.contrib import admin
from .models import Post,Category,Tag
from .adminforms import PostAdminForm
from typeidea.custom_site import custom_site
from typeidea.base_admin import BaseOwnerAdmin
from django.contrib.admin.models import LogEntry,CHANGE
from django.contrib.admin.options import get_content_type_for_model
# from django.contrib.auth import get_permission_codename

from django.urls import reverse
import requests
from django.utils.html import format_html
# Register your models here.

# sso示例
# PERMISSION_API='http://permission.sso.com/has_perm?user={}&perm_code={}'



class PostInline(admin.TabularInline):
    fields = ('title','desc')
    extra = 1
    model = Post


@admin.register(Category,site=custom_site)
class CategoryAdmin(BaseOwnerAdmin):
    list_display = ('name','status','is_nav','created_time','post_count',)
    fields = ('name','status','is_nav')
    inlines = [PostInline,]
    # 出现在显示界面，只是一个返回值
    def post_count(self,obj):
        return obj.post_set.count()
    post_count.short_description = '文章数量'




@admin.register(Tag,site=custom_site)
class TagAdmin(BaseOwnerAdmin):
    list_display = ('name','status','created_time')
    fields = ('name','status')



class CategoryOwnerFilter(admin.SimpleListFilter):
    title = '分类过滤器'

    parameter_name = 'owner_category'
    # 返回查询的id
    def lookups(self, request, model_admin):
        return Category.objects.filter(owner=request.user).values_list('id','name')
    def queryset(self, request, queryset):
        category_id=self.value()
        if category_id:
            return queryset.filter(category_id=self.value())
        return queryset


@admin.register(Post,site=custom_site)
class PostAdmin(BaseOwnerAdmin):
    form = PostAdminForm
    list_display = [
        'title','category','status',
        'created_time','operator','owner'
    ]
    list_display_links = []
    list_filter = [CategoryOwnerFilter]
    search_fields = ['title','category__name',]
    exclude = ('owner',)
    actions_on_top = True
    actions_on_bottom = True
    save_on_top = True
    # 左右
    # filter_horizontal = ('tag',)
    # 上下
    filter_vertical = ('tag',)
    # 普通界面
    # fields = (
    #     ('category','title'),
    #     'desc',
    #     'status',
    #     'content',
    #     'tag',
    # )
    fieldsets = (
        ('基础配置',{
            'description':'基础配置描述',
            'fields':(
                ('category', 'title'),
                 'status',
            ),
        }),
        ('内容',{
            'fields':(
                'desc',
                'content',
            ),
        }),
        ('额外信息',{
            'classes':('collapse',),
            'fields':('tag',),
        }),
    )
    def operator(self,obj):
        return format_html(
            "<a href='{}'>编辑</a>",
            reverse('cus_admin:blog_post_change',args=(obj.id,))
        )
    operator.short_description = '操作'
    # sso示例
    # def has_add_permission(self, request):
    #     opts=self.opts
    #     codename=get_permission_codename('add',opts)
    #     perm_code="%s.%s" % (opts.app_label,codename)
    #     resp=requests.get(PERMISSION_API.format(request.user.username,perm_code))
    #     if resp.status_code==200:
    #         return True
    #     else:
    #         return False

@admin.register(LogEntry,site=custom_site)
class LogEntryAdmin(admin.ModelAdmin):
    list_display = ['object_repr','object_id','action_flag','user','change_message']