
from django.urls import path, include
from django.urls import reverse_lazy
from django.contrib.auth import views as auth_views

from    .views import (home,pc_tablet_server_list,
                       create_department_in_pc_tablet_server,
                       switch_routers_list,email_list,printer_list,
                       user_list,profile_view,password_change_view,
                       logout_view,department_list,branch_list
                       )

urlpatterns = [
    path ('',home, name='home'),
    path('password-change/', password_change_view,name='password_change'),
    path('password-change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='registration/password_change_done.html'), name='password_change_done'),
    path('pc_tablet_server_list/',pc_tablet_server_list, name='pc_tablet_server_list'),   
    path('create_department_in_pc_tablet_server/', create_department_in_pc_tablet_server, name='create_department_in_pc_tablet_server'), 
    path('switch_routers_list/', switch_routers_list, name='switch_router_list'),   
    path('email_list/', email_list, name='email_list'),
    path('printer_list/', printer_list, name='printer_list'),
    path('user_list/', user_list, name='user_list'),
    path('profile/', profile_view, name='profile'),
    path('logout/', logout_view, name='logout'),
    path('department_list/',department_list, name='department_list'),
    path('branch_list/',branch_list, name='branch_list'),

  
]