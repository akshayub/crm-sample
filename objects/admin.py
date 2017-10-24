from django.contrib import admin

from .models import Owner , Lead , Account , Account_Location ,Note , Attachment , Contact , Opportunity , Product , Case , Problem , Component, WorksIn
# Register your models here.

admin.site.register(Owner)
admin.site.register(Lead)
admin.site.register(Account)
admin.site.register(Account_Location)
admin.site.register(Note)
admin.site.register(Attachment)
admin.site.register(Contact)
admin.site.register(Opportunity)
admin.site.register(Case)
admin.site.register(Problem)
admin.site.register(Product)
admin.site.register(Component)
admin.site.register(WorksIn)




