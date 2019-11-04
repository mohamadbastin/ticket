from ticketapp.models import *

for i in Seat.objects.all():
    i.delete()
for i in Row.objects.all():
    i.delete()

hall = Hall.objects.first()
price = Price.objects.first()

master1 = Block.objects.get(name='master-1')
for i in range(1, 2):
    tmp = Row.objects.create(number=i, block=master1)
    for j in range(1, 6):
        Seat.objects.create(number=j, title='master', price=price, row=tmp, status='A')

master2 = Block.objects.get(name='master-2')
for i in range(1, 2):
    tmp = Row.objects.create(number=i, block=master2)
    for j in range(1, 7):
        Seat.objects.create(number=j, title='master', price=price, row=tmp, status='A')

master3 = Block.objects.get(name='master-3')
for i in range(1, 2):
    tmp = Row.objects.create(number=i, block=master3)
    for j in range(1, 6):
        Seat.objects.create(number=j, title='master', price=price, row=tmp, status='A')

s981 = Block.objects.get(name='s98-1')
for i in range(1, 9):
    tmp = Row.objects.create(number=i, block=s981)
    for j in range(1, 6):
        Seat.objects.create(number=j, title='s98', price=price, row=tmp, status='A')

s982 = Block.objects.get(name='s98-2')
for i in range(1, 9):
    tmp = Row.objects.create(number=i, block=s982)
    for j in range(1, 9):
        Seat.objects.create(number=j, title='s98', price=price, row=tmp, status='A')

s983 = Block.objects.get(name='s98-3')
for i in range(1, 9):
    tmp = Row.objects.create(number=i, block=s983)
    for j in range(1, 6):
        Seat.objects.create(number=j, title='s98', price=price, row=tmp, status='A')

kadr971 = Block.objects.get(name='kadr97-1')
for i in range(1, 6):
    tmp = Row.objects.create(number=i, block=kadr971)
    for j in range(1, 5):
        Seat.objects.create(number=j, title='kadr', price=price, row=tmp, status='A')

kadr972 = Block.objects.get(name='kadr97-2')
for i in range(1, 6):
    tmp = Row.objects.create(number=i, block=kadr972)
    for j in range(1, 5):
        Seat.objects.create(number=j, title='kadr', price=price, row=tmp, status='A')

azad1 = Block.objects.get(name='azad-1')
for i in range(1, 4):
    tmp = Row.objects.create(number=i, block=azad1)
    for j in range(1, 10):
        Seat.objects.create(number=j, title='azad', price=price, row=tmp, status='A')

azad2 = Block.objects.get(name='azad-2')
for i in range(1, 2):
    tmp = Row.objects.create(number=i, block=azad2)
    for j in range(1, 8):
        Seat.objects.create(number=j, title='azad', price=price, row=tmp, status='A')

azad3 = Block.objects.get(name='azad-3')
for i in range(1, 5):
    tmp = Row.objects.create(number=i, block=azad3)
    for j in range(1, 12):
        Seat.objects.create(number=j, title='azad', price=price, row=tmp, status='A')

azad4 = Block.objects.get(name='azad-4')
for i in range(1, 5):
    tmp = Row.objects.create(number=i, block=azad4)
    for j in range(1, 11):
        Seat.objects.create(number=j, title='azad', price=price, row=tmp, status='A')

sponser = Block.objects.get(name='sponser')
for i in range(1, 3):
    tmp = Row.objects.create(number=i, block=sponser)
    for j in range(1, 8):
        Seat.objects.create(number=j, title='sponser', price=price, row=tmp, status='A')

ent1 = Block.objects.get(name='ent-1')
for i in range(1, 3):
    tmp = Row.objects.create(number=i, block=ent1)
    for j in range(1, 4):
        Seat.objects.create(number=j, title='ent', price=price, row=tmp, status='A')

ent2 = Block.objects.get(name='ent-2')
for i in range(1, 3):
    tmp = Row.objects.create(number=i, block=ent2)
    for j in range(1, 4):
        Seat.objects.create(number=j, title='ent', price=price, row=tmp, status='A')

###### DELETE


master3 = Block.objects.get(name='master-3')
row = Row.objects.get(block=master3, number=1)
seats = Seat.objects.filter(row=row)
seats[4].delete()

ent1 = Block.objects.get(name='ent-1')
row = Row.objects.get(number=2, block=ent1)
seats = Seat.objects.filter(row=row)
seats[2].delete()

ent2 = Block.objects.get(name='ent-2')
row = Row.objects.get(number=2, block=ent2)
seats = Seat.objects.filter(row=row)
seats[2].delete()

azad3 = Block.objects.get(name='azad-3')
row = Row.objects.get(number=2, block=azad3)
seats = Seat.objects.filter(row=row)
seats[10].delete()

azad3 = Block.objects.get(name='azad-3')
row = Row.objects.get(number=3, block=azad3)
seats = Seat.objects.filter(row=row)
for i in range(3):
    seats.last().delete()

azad3 = Block.objects.get(name='azad-3')
row = Row.objects.get(number=4, block=azad3)
seats = Seat.objects.filter(row=row)
for i in range(6):
    seats.last().delete()

azad4 = Block.objects.get(name='azad-4')
row = Row.objects.get(number=2, block=azad4)
seats = Seat.objects.filter(row=row)
seats[9].delete()

azad4 = Block.objects.get(name='azad-4')
row = Row.objects.get(number=3, block=azad4)
seats = Seat.objects.filter(row=row)
for i in range(2):
    seats.last().delete()

azad4 = Block.objects.get(name='azad-4')
row = Row.objects.get(number=4, block=azad4)
seats = Seat.objects.filter(row=row)
for i in range(3):
    seats.last().delete()

###### SELL

a = Block.objects.filter(name__contains='master')
for i in a:
    b = Row.objects.filter(block=i)
    for j in b:
        c = Seat.objects.filter(row=j)
        for k in c:
            k.status = 'S'
            k.save()

a = Block.objects.filter(name__contains='kadr')
for i in a:
    b = Row.objects.filter(block=i)
    for j in b:
        c = Seat.objects.filter(row=j)
        for k in c:
            k.status = 'S'
            k.save()

a = Block.objects.filter(name__contains='ent')
for i in a:
    b = Row.objects.filter(block=i)
    for j in b:
        c = Seat.objects.filter(row=j)
        for k in c:
            k.status = 'S'
            k.save()

a = Block.objects.get(name='sponser')
b = Row.objects.filter(block=a)
for j in b:
    c = Seat.objects.filter(row=j)
    for k in c:
        k.status = 'S'
        k.save()

a = Block.objects.get(name='azad-3')
b = Row.objects.get(block=a, number=1)
c = Seat.objects.get(row=b, number=1)
c.status = 'S'
c.save()

a = Block.objects.get(name='azad-4')
b = Row.objects.get(block=a, number=1)
c = Seat.objects.get(row=b, number=1)
c.status = 'S'
c.save()
