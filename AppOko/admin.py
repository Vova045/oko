from django.contrib import admin
from AppOko.models import Chapters, SubCategories, GuestList

class ViewsAdmin(admin.ModelAdmin):
    list_display = ('id','ip', 'time')

class ViewersAdmin(admin.ModelAdmin):
    list_display = ('ip','time', 'count')


admin.site.register(GuestList, ViewsAdmin)

admin.site.register(Chapters)
admin.site.register(SubCategories)