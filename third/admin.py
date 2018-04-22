from django.contrib import admin
from .models import Logacn,Logtxn
from .models import Post,Category,Tag

class PostAdmin(admin.ModelAdmin):
    list_display = ['title','category','created_time','modified_time','author']
# Register your models here.
admin.site.register(Logacn)
admin.site.register(Logtxn)
admin.site.register(Post,PostAdmin)
admin.site.register(Category)
admin.site.register(Tag)