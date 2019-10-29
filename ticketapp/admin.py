from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Service)
admin.site.register(Price)
admin.site.register(Profile)
admin.site.register(UserService)
admin.site.register(Ad)
admin.site.register(Seat)
admin.site.register(Row)
admin.site.register(Block)
admin.site.register(Hall)
admin.site.register(Event)
admin.site.register(HallEvent)
admin.site.register(Ticket)
admin.site.register(Terminal)
admin.site.register(PaymentLinks)
admin.site.register(Invoice)

