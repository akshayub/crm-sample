from django.db import models
from django.core.validators import RegexValidator


# Create your models here.
class Owner(models.Model):
    user = models.ForeignKey('auth.User')
    bdate = models.DateField()

    def __str__(self):
        return str(self.id) + " - " + self.user.first_name + " " + self.user.last_name


class Lead(models.Model):
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    address = models.CharField(max_length=250)
    company = models.CharField(max_length=250)
    email = models.EmailField()
    status = models.CharField(max_length=250)
    added_on = models.DateField()

    def __str__(self):
        return str(self.id) + " - " + self.name


class Account(models.Model):
    name = models.CharField(max_length=250)
    website = models.CharField(max_length=250)
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )

    # validators should be a list
    phone_number = models.CharField(
        validators=[phone_regex],
        max_length=15,
        blank=True
    )
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE)
    added_on = models.DateField()

    # Recursive relationship
    # https://stackoverflow.com/questions/18271001/django-recursive-relationship

    subsidiary_of = models.OneToOneField('self', null=True, blank=True)

    def save(self, check=True, *args, **kwargs):
        super(Account, self).save()
        if self.subsidiary_of and check:
            self.subsidiary_of.subsidiary_of = self
            self.subsidiary_of.save(check=False)

    def __str__(self):
        return str(self.id) + " - " + self.name


class AccountLocation(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    place = models.CharField(max_length=250)


class Note(models.Model):
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=200)

    def __str__(self):
        return str(self.id) + " - " + self.title


class Attachment(models.Model):
    note = models.ForeignKey(Note, on_delete=models.CASCADE)
    attached_to_acc = models.ForeignKey(Account, on_delete=models.CASCADE)


class Contact(models.Model):
    name = models.CharField(max_length=250)
    address = models.CharField(max_length=250)
    email = models.EmailField()
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )

    # validators should be a list
    phone_number = models.CharField(
        validators=[phone_regex],
        max_length=15,
        blank=True
    )

    bdate = models.DateField()
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE)
    added_on = models.DateField()
    works_for = models.ForeignKey(Account, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id) + " - " + self.name


class Opportunity(models.Model):
    name = models.CharField(max_length=200)
    stage = models.CharField(max_length=200)
    close_date = models.DateField()
    probability = models.IntegerField()
    description = models.CharField(max_length=1000)
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id) + " - " + self.name


class Product(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return str(self.id) + " - " + self.name


class Case(models.Model):
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=1000)
    resolve_date = models.DateField()
    resolved = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id) + " - " + self.title


class Problem(models.Model):
    case = models.ForeignKey(Case, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE)
    issue_date = models.DateField()

    def __str__(self):
        return str(self.case) + "Issued on " + str(self.issue_date)


class Component(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('id', 'product')

    def __str__(self):
        return str(self.id) + " - " + str(self.product) + " - " + str(self.name)
