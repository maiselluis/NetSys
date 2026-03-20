# Register your models here.
from django.contrib import admin
from .models import (Branch, Department, CustomUser,
                     Pc_tablet_server, Switch_router,
                     Email, Printer,PcIpAddress,CustomUser)


admin.site.register(Branch)
admin.site.register(Department)
admin.site.register(CustomUser)
admin.site.register(Pc_tablet_server)
admin.site.register(Switch_router)  
admin.site.register(Email)
admin.site.register(Printer)
admin.register(PcIpAddress)

# Register your models here.