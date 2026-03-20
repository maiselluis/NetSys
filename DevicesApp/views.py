from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import (Branch, Department, CustomUser, 
                     Pc_tablet_server, Switch_router,
                     Email, PcIpAddress,Printer,Department)

from .forms import (PcTabletServerForm,PcIpAddressFormSet,
                    DepartmentForm,BranchForm,SwitchRouterForm,
                    EmailForm,PrinterForm,CustomUserForm,CustomUserUpdateForm,
                    CustomPasswordChangeForm)


from django.contrib.auth.models import Group, Permission

from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import logout



# Create your views here.

def home(request):
    if request.user.is_authenticated:
        return render(request, 'tabler/index.html')

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        remember_me = request.POST.get("remember_me")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            
            if not remember_me:
                request.session.set_expiry(0)  
                # 👉 sesión expira al cerrar navegador
            else:
                request.session.set_expiry(1209600)  
                # 👉 2 semanas (puedes cambiarlo)
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password")
            
       

    return render(request, 'login.html')
    

#Brnach views
def branch_list(request):
    branches = Branch.objects.all()
    context = {'branches': branches}    
    return render(request, 'tabler/branch/branch_list.html', context)
    

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



#[Create department in PC_TABLET_SERVER form]


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
           

def logout_view(request):
    logout(request)
    return redirect('home')  # te manda al login