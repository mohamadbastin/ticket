from django.contrib.auth.models import User
from django.db import models


# Create your models here.

class Service(models.Model):
    name = models.CharField(max_length=256)
    profile = models.ForeignKey('Profile', on_delete=models.CASCADE, related_name='service')
    is_used = models.BooleanField(default=False)

    def __str__(self):
        return self.name + ' ' + str(self.profile.name) + ' ' + str(self.is_used)


class Major(models.Model):
    name = models.CharField(max_length=127)

    def __str__(self):
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    picture = models.ImageField(null=True, blank=True, default='profile.png')
    student_id = models.CharField(max_length=10)
    national_id = models.CharField(max_length=25)
    gender = models.CharField(max_length=2, choices=[('m', 'male'), ('f', 'female'), ('t', 'trans')])
    major = models.ForeignKey(Major, on_delete=models.SET_NULL, null=True, blank=True)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    name = models.CharField(max_length=200)
    qr = models.CharField(null=True, blank=True, max_length=10000)

    # chair = models.ManyToManyField('Seat', through='Ticket')

    @property
    def bought(self):
        a = Ticket.objects.filter(profile=self)
        if a:
            return True
        return False

    def __str__(self):
        return self.name
    # service = m


# class Ticket(models.Model):
#     name = models.CharField(max_length=1000)
#     price = models.IntegerField()
#     description = models.CharField(max_length=2048, null=True, blank=True)
#     ad = models.CharField(max_length=1024, null=True, blank=True)
#     ad_pic = models.ImageField(null=True, blank=True)


class UserService(models.Model):
    # class Meta:
    #     unique_together = ()
    service = models.ForeignKey(Service, on_delete=models.PROTECT)
    user = models.ForeignKey(Profile, on_delete=models.PROTECT)
    status = models.BooleanField(default=False)

    def __str__(self):
        return str(self.service) + ' --> ' + str(self.user)


class Price(models.Model):
    name = models.CharField(max_length=127)
    price = models.IntegerField()

    def __str__(self):
        return self.name


class Ad(models.Model):
    title = models.CharField(max_length=255)
    text = models.CharField(max_length=10000)
    pic = models.ImageField()

    def __str__(self):
        return self.title


class Seat(models.Model):
    class Meta:
        unique_together = ['number', 'row']
        ordering = ['row', 'number', ]

    status_choices = [('A', 'Available'), ('S', 'Sold'), ('M', 'Mine'), ('N', 'Not_Visible')]
    # block = models.CharField(max_length=128)
    # gender = models.CharField(max_length=2, choices=[('f', 'female'), ('m', 'male')])
    # row = models.IntegerField()
    number = models.IntegerField()
    title = models.CharField(max_length=128)
    price = models.ForeignKey(Price, on_delete=models.PROTECT, related_name='seat')
    description = models.CharField(max_length=2048, null=True, blank=True)
    ad = models.ForeignKey(Ad, on_delete=models.PROTECT, null=True, blank=True, related_name='seat')
    row = models.ForeignKey('Row', on_delete=models.PROTECT, related_name='seat')
    owner = models.ManyToManyField(Profile, through='Ticket', through_fields=('seat', 'profile'))
    status = models.CharField(default='A', choices=status_choices, max_length=2)

    # owner = models.OneToOneField(Profile, on_delete=models.PROTECT, null=True, blank=True)

    def __str__(self):
        return str(self.title) + ' : ' + str(self.number) + ' -> ' + str(self.row)


class Ticket(models.Model):
    class Meta:
        unique_together = ['seat', 'profile']

    seat = models.OneToOneField(Seat, on_delete=models.CASCADE)
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, related_name='ticket_owned')
    date = models.DateTimeField(auto_now_add=True)
    # buyer = models.ForeignKey(Profile, on_delete=models.SET_NULL, related_name='ticket_bought')
    pdf = models.FileField(null=True, blank=True)

    def __str__(self):
        return str(self.seat) + ' -------> ' + str(self.profile)


class Row(models.Model):
    class Meta:
        ordering = ['block', 'number', ]
        unique_together = ['number', 'block']

    number = models.IntegerField()
    # seat = models.ForeignKey(Seat, on_delete=models.PROTECT)
    block = models.ForeignKey('Block', on_delete=models.PROTECT, related_name='row')

    def __str__(self):
        return str(self.number) + ' -> ' + str(self.block)


class Block(models.Model):
    class Meta:
        # ordering = ['row__number']
        unique_together = ['name', 'gender', 'hall']

    name = models.CharField(max_length=127)
    gender = models.CharField(max_length=2, choices=[('f', 'female'), ('m', 'male'), ('t', 'trans')])
    # row = models.ForeignKey(Row, on_delete=models.PROTECT)
    hall = models.ForeignKey('Hall', on_delete=models.PROTECT, related_name='block')

    def __str__(self):
        return str(self.name) + ' : ' + str(self.gender) + ' : ' + str(self.hall)


class Hall(models.Model):
    name = models.CharField(max_length=128)

    # block = models.ForeignKey(Block, on_delete=models.PROTECT)

    def __str__(self):
        return self.name


class Event(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name


class HallEvent(models.Model):
    event = models.ForeignKey(Event, on_delete=models.PROTECT)
    hall = models.ForeignKey(Hall, on_delete=models.PROTECT)


class Terminal(models.Model):
    name = models.CharField(max_length=50)
    api_key = models.CharField(max_length=1000)
    token = models.CharField(max_length=100000, null=True, blank=True)

    # boz = models.IntegerField()

    def __str__(self):
        return self.name


class PaymentLinks(models.Model):
    name = models.CharField(max_length=100)
    link = models.CharField(max_length=1000)
    terminal = models.ForeignKey(Terminal, on_delete=models.PROTECT)

    def __str__(self):
        return self.name


class Invoice(models.Model):
    # class Meta:
    # unique_together = ['key', ]

    date = models.DateTimeField(auto_now_add=True)
    terminal = models.ForeignKey(Terminal, on_delete=models.PROTECT)
    amount = models.PositiveIntegerField()
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    key = models.CharField(max_length=1000, blank=True, null=True)
    status = models.CharField(max_length=100, choices=[('f', 'false'), ('w', 'waiting'), ('t', 'true')], blank=True,
                              null=True)
    payment_id = models.CharField(max_length=1000, null=True, blank=True)
    error = models.CharField(max_length=100, null=True, blank=True)
    reservation = models.ForeignKey('Reservation', on_delete=models.SET_NULL, null=True, blank=True,
                                    related_name='invoice')
    ticket = models.ForeignKey(Ticket, on_delete=models.SET_NULL, null=True, blank=True, related_name='invoice')
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return str(self.key)


class Reservation(models.Model):
    # class Meta:
    # unique_together = ['seat', 'profile', ]

    seat = models.ForeignKey(Seat, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='reservation_owned')
    date = models.DateTimeField(auto_now_add=True)
    # buyer = models.ForeignKey(Profile, on_delete=models.SET_NULL, related_name='reservation_bought')
    res_date_time = models.DateTimeField(auto_now_add=True)
    # pay_date_time = models.DateTimeField(null=True, blank=True)
    is_deleted = models.BooleanField(default=False)
    ticket = models.ForeignKey(Ticket, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return str(self.seat) + ' -------> ' + str(self.profile)
