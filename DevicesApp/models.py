from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.functions import Lower


class Branch(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200,blank=True, null=True)
    phone_number = models.CharField(max_length=20,blank=True, null=True)
    email = models.EmailField( blank=True, null=True)
   
    class Meta:
        constraints = [
            models.UniqueConstraint(
                Lower('name'),
                name='unique_branch_name'
            )
        ]
        db_table = 'tb_branch'  # Especifica el nombre de la tabla en la base de datos

    def __str__(self):
        return self.name

class Department(models.Model):
    name = models.CharField(max_length=100)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='departments')
    
    
    class Meta:
        db_table = 'tb_department'  # Especifica el nombre de la tabla en la base de datos
        constraints = [
            models.UniqueConstraint(
                Lower('name'),
                'branch',
                name='unique_department_per_branch'
            )
        ]
        

    def __str__(self):
        return f"{self.name}"


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20,blank=True, null=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    pictures = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
   
   
   
    class Meta:
        db_table = 'tb_custom_user'
        constraints = [
            models.UniqueConstraint(
                Lower('email'),
                name='unique_email'
            )
        ]   
            
    def __str__(self):
        return self.username
    

class Pc_tablet_server(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='devices')
    name = models.CharField(max_length=100)   
    mac_address = models.CharField(max_length=17)   
    any_desk=models.CharField(max_length=100, blank=True, null=True)
    rust_desk=models.CharField(max_length=100, blank=True, null=True)
    remote_desktop=models.BooleanField(default=False)
    
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                Lower('name'),
                'department',
                name='unique_device_per_department'
            )
                ]
        db_table = 'tb_pc_tablet_server'  # Especifica el nombre de la tabla en la base de datos    
        
    def __str__(self):
        return self.name
    

class PcIpAddress(models.Model):
    pc = models.ForeignKey('Pc_tablet_server', on_delete=models.CASCADE, related_name='ip_addresses')
    ip_address = models.GenericIPAddressField()


    class Meta:
        db_table = 'tb_pc_ip_address'  # Especifica el nombre de la tabla en la base de datos   
        
    def __str__(self):
        return self.ip_address
    
    
    
class Switch_router(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='switch_routers')
    name = models.CharField(max_length=100)
    ip_address = models.GenericIPAddressField()
    username = models.CharField(max_length=100, blank=True, null=True)
    password = models.CharField(max_length=100, blank=True, null=True)
    mac_address = models.CharField(max_length=17)   
    file_settings=models.FileField(upload_to='settings_files/', null=True, blank=True)
    
    class Meta:
       
        db_table = 'tb_switch_router'  # Especifica el nombre de la tabla en la base de datos
        
    def __str__(self):
        return self.name
    
    
class Email(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='emails')
    email_address = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
     
    class Meta:
        db_table = 'tb_email'
       
        

    def __str__(self):
        return self.email_address   
 
    
class Printer(models.Model):
    department= models.ForeignKey(Department, on_delete=models.CASCADE, related_name='printers')
    name= models.CharField(max_length=100)
    ip_address = models.GenericIPAddressField()
    username = models.CharField(max_length=100, blank=True, null=True)
    password = models.CharField(max_length=100, blank=True, null=True)
    
    
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                Lower('name'),
                'department',
                name='unique_printer_per_department'
            )
        ]
        db_table = 'tb_printer'  # Especifica el nombre de la tabla en la base de datos
        
        
        
    def __str__(self):
        return self.name
