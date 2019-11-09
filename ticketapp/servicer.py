from ticketapp.models import Service, Ticket


def service(p):
    l = ['food', 'enter', 'pixel']
    for i in l:
        Service.objects.create(name=i, profile=p)


t = Ticket.objects.all()
for i in t:
    p = i.profile
    s = p.service.all()
    for j in s:
        j.delete()

for i in t:
    p = i.profile
    service(p)
