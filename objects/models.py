from django.db import models
from django.core.validators import RegexValidator
# Create your models here.

class Owner(models.Model):
    Owner_Name = models.CharField(max_length=250)
    Owner_Email = models.EmailField()
    Owner_BDate = models.DateField()
    id = models.AutoField(primary_key=True)

    def __str__(self):
        return str(self.id)+ " - " + self.Owner_Name


class Lead(models.Model):
    Owned_By = models.ForeignKey(Owner , on_delete=models.CASCADE)
    Name =  models.CharField(max_length=250)
    Address =  models.CharField(max_length=250)
    Company = models.CharField(max_length=250)
    Email =  models.EmailField()
    Status = models.CharField(max_length=250)
    Added_On = models.DateField()

    def __str__(self):
        return str(self.id)+ " - " + self.Name


class Account(models.Model):
    Name =  models.CharField(max_length=250)
    Website = models.CharField(max_length=250)

    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    Phone_Number = models.CharField(validators=[phone_regex], max_length=15,
                                    blank=True )  # validators should be a list
    Owned_By = models.ForeignKey(Owner , on_delete=models.CASCADE)
    Added_On = models.DateField()

    #Recursive relationship
    #https://stackoverflow.com/questions/18271001/django-recursive-relationship

    Subsidiary_Of = models.OneToOneField('self' , null=True , blank=True)

    def save(self, check = True, *args, **kwargs):
        super(Account, self).save()
        if self.Subsidiary_Of and check:
            self.Subsidiary_Of.Subsidiary_Of = self
            self.Subsidiary_Of.save(check= False)

    def __str__(self):
        return str(self.id)+ " - " + self.Name


class Account_Location(models.Model):
    Acc_id = models.ForeignKey(Account , on_delete = models.CASCADE)
    Place = models.CharField(max_length = 250)




class Note(models.Model):
    Title = models.CharField(max_length = 200)
    Description = models.CharField(max_length = 200)

    def __str__(self):
        return str(self.id)+ " - " + self.Title

class Attachment(models.Model):
    Note_Id = models.ForeignKey(Note , on_delete=models.CASCADE)
    Attached_To_Acc = models.ForeignKey(Account , on_delete=models.CASCADE)

class Contact(models.Model):
    Name = models.CharField(max_length=250)
    Address = models.CharField(max_length=250)
    Email = models.EmailField()
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    Phone_Number = models.CharField(validators=[phone_regex], max_length=15,
                                    blank=True)  # validators should be a list

    Birth_Date = models.DateField()

    Added_By = models.ForeignKey(Owner , on_delete=models.CASCADE)

    Added_On = models.DateField()

    def __str__(self):
        return str(self.id)+ " - " + self.Name


class WorksIn(models.Model):
    Contact_Id = models.ForeignKey(Contact , on_delete=models.CASCADE)
    Account_Id = models.ForeignKey( Account, on_delete=models.CASCADE)

class Opportunity(models.Model):
    Name = models.CharField(max_length=200)
    Stage = models.CharField(max_length=200)
    Close_Date = models.DateField()
    probability = models.IntegerField();
    Description = models.CharField(max_length=1000)
    Owned_By = models.ForeignKey(Owner , on_delete=models.CASCADE)
    Account_Number = models.ForeignKey(Account , on_delete=models.CASCADE)


    def __str__(self):
        return str(self.id)+ " - " + self.Name



class Product(models.Model):
    Name =  models.CharField(max_length=200)


    def __str__(self):
        return str(self.id)+ " - " + self.Name



class Case(models.Model):
    Title = models.CharField(max_length = 200)
    Description = models.CharField(max_length=1000)
    Resolve_Date = models.DateField()

    def __str__(self):
        return str(self.id)+ " - " + self.Title


class Problem(models.Model):
    Case_Id = models.ForeignKey(Case , on_delete=models.CASCADE)
    Product_Id = models.ForeignKey(Product , on_delete=models.CASCADE)
    Account_Id = models.ForeignKey(Account , on_delete=models.CASCADE)
    Owner_Id = models.ForeignKey(Owner, on_delete=models.CASCADE)
    Issue_Date = models.DateField()

    def __str__(self):
        return str(self.id)+ " Issued on " + str(self.Issue_Date)

class Component(models.Model):
    Name = models.CharField(max_length=200)
    Product_Id = models.ForeignKey(Product, on_delete=models.CASCADE)
    id = models.AutoField(primary_key=True)

    class Meta:
        unique_together = ('id', 'Product_Id')

    def __str__(self):
        return str(self.id)+ " - " + str(self.Product_Id) + " - " + str(self.Name)