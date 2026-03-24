from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import (Branch, Department, CustomUser, 
                     Pc_tablet_server, Switch_router,
                     Email, PcIpAddress,Printer,Department)

from .forms import (PcTabletServerForm,PcIpAddressFormSet,
                    DepartmentForm,BranchForm,SwitchRouterForm,
                    EmailForm,PrinterForm,CustomUserForm,CustomUserUpdateForm,
                    CustomPasswordChangeForm,GroupForm)


from django.contrib.auth.models import Group, Permission

from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import logout
from django.db.models import Count
from django.db.models.functions import Lower
from django.contrib.contenttypes.models import ContentType
from collections import defaultdict



# Create your views here.
#def home(request):
 #   if request.user.is_authenticated:
 #       return render(request, 'tabler/index.html')

 #   if request.method == "POST":
 #       username = request.POST.get("username")
 #       password = request.POST.get("password")
 #       remember_me = request.POST.get("remember_me")

 #       user = authenticate(request, username=username, password=password)

 #       if user is not None:
 #           login(request, user)
            
#            if not remember_me:
 #               request.session.set_expiry(0)  
                # 👉 sesión expira al cerrar navegador
#            else:
#                request.session.set_expiry(1209600)  
                # 👉 2 semanas (puedes cambiarlo)
 #           return redirect('home')
#        else:
#            messages.error(request, "Invalid username or password")
            
       

 #   return render(request, 'login.html')
 
 



def home(request):
    if request.user.is_authenticated:

        # ======================
        # KPIs PRINCIPALES
        # ======================
        total_branches = Branch.objects.count()
        total_departments = Department.objects.count()
        total_users = CustomUser.objects.count()
        total_devices = Pc_tablet_server.objects.count()
        total_printers = Printer.objects.count()
        total_switches = Switch_router.objects.count()
        total_emails = Email.objects.count()


        # ======================
        # DEVICES
        # ======================
        devices_remote = Pc_tablet_server.objects.filter(remote_desktop=True).count()

        devices_without_ip = Pc_tablet_server.objects.annotate(
            ip_count=Count('ip_addresses')
        ).filter(ip_count=0).count()

        # ======================
        # DEPARTMENTS ANALYSIS
        # ======================
        departments_without_devices = Department.objects.annotate(
            device_count=Count('devices')
        ).filter(device_count=0).count()

        departments_without_printers = Department.objects.annotate(
            printer_count=Count('printers')
        ).filter(printer_count=0).count()

        departments_without_emails = Department.objects.annotate(
            email_count=Count('emails')
        ).filter(email_count=0).count()

        # ======================
        # NETWORK
        # ======================
        total_ips = PcIpAddress.objects.count()

        switches_without_config = Switch_router.objects.filter(file_settings="").count()

        # ======================
        # TOP DEPARTMENTS
        # ======================
        top_departments = Department.objects.annotate(
            total_devices=Count('devices')
        ).order_by('-total_devices')[:5]

        # ======================
        # DEVICES PER BRANCH
        # ======================
        devices_per_branch = Branch.objects.annotate(
            total_devices=Count('departments__devices')
        )

        context = {
            # KPIs
            "total_branches": total_branches,
            "total_departments": total_departments,
            "total_users": total_users,
            "total_devices": total_devices,
            "total_printers": total_printers,
            "total_switches": total_switches,

            # Devices
            "devices_remote": devices_remote,
            "devices_without_ip": devices_without_ip,

            # Departments
            "departments_without_devices": departments_without_devices,
            "departments_without_printers": departments_without_printers,
            "departments_without_emails": departments_without_emails,

            # Network
            "total_ips": total_ips,
            "switches_without_config": switches_without_config,

            # Ranking
            "top_departments": top_departments,
            "devices_per_branch": devices_per_branch,
            "total_emails": total_emails,
            
        }

        return render(request, 'tabler/index.html', context)

    # ======================
    # LOGIN (NO TOCAR)
    # ======================
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        remember_me = request.POST.get("remember_me")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            if not remember_me:
                request.session.set_expiry(0)
            else:
                request.session.set_expiry(1209600)

            return redirect('home')
        else:
            messages.error(request, "Invalid username or password")

    return render(request, 'login.html')
    

#Brnach views
@login_required
def branch_list(request):
    branches = Branch.objects.all()
    context = {'branches': branches}    
    return render(request, 'tabler/branch/branch_list.html', context)
    
@login_required
#Department views
def department_list(request):
    departments = Department.objects.select_related('branch').all()
    branches = Branch.objects.all()

    if request.method == "POST":

        # ======================
        # DELETE
        # ======================
        if "delete_department" in request.POST:
            department_id = request.POST.get("department_id")
            department = get_object_or_404(Department, id=department_id)
            department.delete()
            return redirect("department_list")

        # ======================
        # CREATE / EDIT
        # ======================
        department_id = request.POST.get("department_id")

        if department_id:
            department = get_object_or_404(Department, id=department_id)
            form = DepartmentForm(request.POST, instance=department)
        else:
            form = DepartmentForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("department_list")
        else:
            print(form.errors)  # 🔥 debug útil

    else:
        form = DepartmentForm()

    return render(request, 'tabler/department/department_list.html', {
        'departments': departments,
        'form': form,
        'branches': branches,
    })


@login_required
def create_department_in_pc_tablet_server(request):
    #branch_list = Branch.objects.all()

 
    if request.method == 'POST':
        form = DepartmentForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('pc_tablet_server_list')

    else:
        form = DepartmentForm()

    context = {
        'form': form,
    }

    return render(
        request,
        'tabler/pc_tablet_server/pc_tablet_server_list.html',
        context
    )


#[Cretae, Edit] views for Pc_tablet_server
#Pc_tablet_server views
@login_required
def pc_tablet_server_list(request):
   # devices = Pc_tablet_server.objects.select_related("department")
    devices = Pc_tablet_server.objects.select_related("department").prefetch_related("ip_addresses")

    departments = Department.objects.all()
    
    department_form = DepartmentForm()

    if request.method == "POST":

        # ----------------------
        # DELETE
        # ----------------------
        if "delete_device" in request.POST:
            device_id = request.POST.get("device_id")
            device = get_object_or_404(Pc_tablet_server, id=device_id)
            device.delete()
            return redirect("pc_tablet_server_list")

        # ----------------------
        # CREATE / EDIT
        # ----------------------
        device_id = request.POST.get("device_id")
        if device_id:
            # Edit
            device = get_object_or_404(Pc_tablet_server, id=device_id)
            form = PcTabletServerForm(request.POST, instance=device)
            ip_formset = PcIpAddressFormSet(request.POST, instance=device)
        else:
            # Create
            form = PcTabletServerForm(request.POST)
            ip_formset = PcIpAddressFormSet(request.POST)

        if form.is_valid() and ip_formset.is_valid():
            device = form.save()
            ip_formset.instance = device
            ip_formset.save()
            return redirect("pc_tablet_server_list")

    else:
        # GET
        form = PcTabletServerForm()
        ip_formset = PcIpAddressFormSet()

    context = {
        "devices": devices,
        "departments": departments,
        "form": form,
        "ip_formset": ip_formset,
        'department_form': department_form,
    }

    return render(request, 'tabler/pc_tablet_server/pc_tablet_server_list.html', context)


#Switch_router views
@login_required
def switch_routers_list(request):
   # devices = Pc_tablet_server.objects.select_related("department")
    switch_routers = Switch_router.objects.all() 
    
    branch= Branch.objects.all()
    
    if request.method == "POST":
        
        # ----------------------
        # DELETE
        # ----------------------
        if "delete_device" in request.POST:
            device_id = request.POST.get("device_id")
            device = get_object_or_404(Switch_router, id=device_id)
            device.delete()
            return redirect("switch_router_list")   
        # ----------------------
        # CREATE / EDIT     
        device_id = request.POST.get("device_id")
        if device_id:
            # Edit
            device = get_object_or_404(Switch_router, id=device_id)
            form = SwitchRouterForm(request.POST,request.FILES, instance=device)
        else:
            # Create    
            form = SwitchRouterForm(request.POST,request.FILES)
            
        if form.is_valid():
            device = form.save()
            return redirect("switch_router_list")
    else:
        # GET
        form = SwitchRouterForm()        
    

    context = {
            'switch_routers': switch_routers,
            'form': form,
            'branch': branch,
        }   
   

    return render(request, 'tabler/switch_routers/switch_routers_list.html', context)

@login_required
def email_list(request):
    departments= Department.objects.all()
    emails = Email.objects.all()
    
    if request.method == "POST":        
        # ----------------------
        # DELETE
        # ----------------------
        if "delete_email" in request.POST:
            email_id = request.POST.get("email_id")
            email = get_object_or_404(Email, id=email_id)
            email.delete()
            return redirect("email_list")   
        # ----------------------
        # CREATE / EDIT     
        email_id = request.POST.get("email_id")
        if email_id:
            # Edit
            email = get_object_or_404(Email, id=email_id)
            form = EmailForm(request.POST, instance=email)
        else:
            # Create    
            form = EmailForm(request.POST)
            
        if form.is_valid():
            email = form.save()
            return redirect("email_list")
    else:
        # GET
        form = EmailForm()        
    
    
    
    context = {
               'emails': emails,
               'departments': departments,
                'form': form,
               }    
    return render(request, 'tabler/email/email_list.html', context) 


@login_required
def printer_list(request):
    departments = Department.objects.all()
    printers = Printer.objects.all()

    if request.method == "POST":

        # ----------------------
        # DELETE
        # ----------------------
        if "delete_printer" in request.POST:
            printer_id = request.POST.get("printer_id")
            printer = get_object_or_404(Printer, id=printer_id)
            printer.delete()
            return redirect("printer_list")

        # ----------------------
        # CREATE / EDIT
        # ----------------------
        printer_id = request.POST.get("printer_id")

        if printer_id:
            printer = get_object_or_404(Printer, id=printer_id)
            form = PrinterForm(request.POST, instance=printer)
        else:
            form = PrinterForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("printer_list")

    else:
        form = PrinterForm()

    return render(request, 'tabler/printer/printer_list.html', {
        'printers': printers,
        'departments': departments,
        'form': form,
    })

@login_required
def user_list(request):
    departments = Department.objects.all()
    users = CustomUser.objects.all()
    form = CustomUserForm()
    groups_all = Group.objects.all()
    perms_all = Permission.objects.all()

    if request.method == "POST":
        action = request.POST.get("action")

        # ======================
        # CREATE
        # ======================
        if action == "create":
            form = CustomUserForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return redirect('user_list')

        # ======================
        # EDIT
        # ======================
    

        elif action == "edit":
            try:
                user = CustomUser.objects.get(id=request.POST.get("user_id"))

                user.username = request.POST.get("username")
                user.first_name = request.POST.get("first_name")
                user.last_name = request.POST.get("last_name")
                user.email = request.POST.get("email")

                user.phone_number = request.POST.get("phone_number") or ""

                dept_id = request.POST.get("department")
                user.department = Department.objects.get(id=dept_id) if dept_id else None

                if request.FILES.get("pictures"):
                    user.pictures = request.FILES.get("pictures")

                # 🔥 Password
                password = request.POST.get("password")

                user.is_active = 'is_active' in request.POST
                user.is_staff = 'is_staff' in request.POST
                user.is_superuser = 'is_superuser' in request.POST

                user.save()

                # 🔥 IMPORTANTE: después del save
                if password:
                    user.set_password(password)
                    user.save()
                    update_session_auth_hash(request, user)

                # Groups & Permissions
                group_ids = request.POST.getlist("groups")
                perm_ids = request.POST.getlist("user_permissions")

                user.groups.set(group_ids)
                user.user_permissions.set(perm_ids)

                return redirect('user_list')

            except Exception as e:
                print("ERROR EDIT USER:", e)

        # ======================
        # DELETE
        # ======================
        elif "delete_id" in request.POST:
            CustomUser.objects.get(id=request.POST.get("delete_id")).delete()
            return redirect('user_list')

    # 🔥 DATA PARA MODAL
    for u in users:
        u.groups_ids = list(u.groups.values_list('id', flat=True))
        u.permissions_ids = list(u.user_permissions.values_list('id', flat=True))
        u.department_id = u.department.id if u.department else None

    return render(request, "tabler/user/user_list.html", {
        "users": users,
        "form": form,
        "departments": departments,
        "groups": groups_all,
        "permissions": perms_all,
    })

    
    
@login_required
def profile_view(request):
    user = request.user

    if request.method == "POST":
        form = CustomUserUpdateForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile')

    else:
        form = CustomUserUpdateForm(instance=user)
        
    
    # PASAR LISTA DE IDS AL TEMPLATE
    user_groups_ids = list(user.groups.values_list('id', flat=True))
    user_permissions_ids = list(user.user_permissions.values_list('id', flat=True))

    return render(request, "tabler/profile/profile.html", {
        "form": form,
        "user_obj": user,
        "user_groups_ids": user_groups_ids,
        "user_permissions_ids": user_permissions_ids,
    })
    
    
@login_required
def password_change_view(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = CustomPasswordChangeForm(user=request.user)

    return render(request, 'registration/password_change.html', {'form': form})
           
@login_required
def logout_view(request):
    logout(request)
    return redirect('home')  # te manda al login

@login_required 
def branch_list(request):
    branch= Branch.objects.all()
    
    if request.method == "POST":
        if "delete_branch" in request.POST:
            branch_id = request.POST.get("branch_id")
            branch = get_object_or_404(Branch, id=branch_id)
            branch.delete()
            return redirect("branch_list")   
        
        branch_id = request.POST.get("branch_id")
        if branch_id:
            branch = get_object_or_404(Branch, id=branch_id)
            form = BranchForm(request.POST, instance=branch)
        else:
            form = BranchForm(request.POST)
            
            
        if form.is_valid():
            form.save()
            return redirect("branch_list")
   


    else:
        form = BranchForm()


    
    return render(request, 'tabler/branch/branch_list.html', {'branch': branch})


def group_list(request):
    groups = Group.objects.prefetch_related('permissions').all()

    # 🔥 Agrupar permisos por app para mostrar en UI
    permissions = Permission.objects.select_related('content_type')
    grouped_permissions = defaultdict(list)
    for perm in permissions:
        app_label = perm.content_type.app_label
        grouped_permissions[app_label].append(perm)

    # Si es POST, crear/editar
    if request.method == "POST":
        group_id = request.POST.get("group_id")
        if group_id:
            instance = Group.objects.get(id=group_id)
        else:
            instance = None

        form = GroupForm(request.POST, instance=instance)

        if form.is_valid():
            group = form.save()
            # Asignar permisos seleccionados
            group.permissions.set(form.cleaned_data['permissions'])
            return redirect("group_list")
        
        # Si borras
        if "delete_group" in request.POST:
            group_id = request.POST.get("group_id")
            Group.objects.get(id=group_id).delete()
            return redirect("group_list")

    else:
        form = GroupForm()

    return render(request, "tabler/groups/group_list.html", {
        "groups": groups,
        "grouped_permissions": dict(grouped_permissions),
        "form": form,  # 🔥 ahora el template recibe form
    })