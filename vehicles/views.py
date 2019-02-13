from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from .models import Vehicle_Type

from django.contrib.auth.decorators import login_required


def _creatAccountType(login, name, type):

    last = Vehicle_Type.objects.all().filter(login=login).last()
    if last:
        aktiv = False
        pos = last.pos + 1
    else:
        aktiv = True
        pos = 1
    Q = Vehicle_Type.objects.filter(login=login, label=name)

    status = ''
    if Q:
        status = 'Error:bereits vorhanden'
    elif len(name) < 2:
        status = 'Error:Name zu kurz'
    else:
        AT = Vehicle_Type(login=login,label=name,type=type,pos=pos,aktiv=aktiv)
        AT.save()

    return status


def _initAccountType(login):

    global MSG
    budgetName = 'Mein Auto'

    Q_Type = Vehicle_Type.objects.filter(login=login)
    if Q_Type:
        Vehicle_Type.objects.filter(login=login).update(aktiv=True)
    else:
        MSG = _creatAccountType(login, budgetName, 'CAR')
        Q_Type = Vehicle_Type.objects.filter(login=login)

    return Q_Type


def _getVehicleTypes(login):

    Q_Type = Vehicle_Type.objects.filter(login=login,
                                         aktiv=True)
    if not Q_Type:
        Q_Type = _initAccountType(login=login)

    label = Q_Type[0].label
    type =  Q_Type[0].type
    vt_list = Vehicle_Type.objects.values_list('id', 'label', 'aktiv', 'type', named=True).filter(login=login)

    return {
        'vt_list': vt_list,
        'vt_label': label,
        'vt_type': type,
    }


def set_vehicle_type(request, type_id):

    q = Vehicle_Type.objects.filter(login=request.user).update(aktiv=False)
    q = Vehicle_Type.objects.filter(login=request.user, id=type_id).update(aktiv=True)

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='/vehicles/login/')
def index(request):


    data = _getVehicleTypes(request.user)

    print('user:', request.user)

    print('list:', data['vt_list'], data['vt_label'])

    template = loader.get_template('vehicles/index.html')
    context = {
        'vt_list': data['vt_list'],
        'vt_type': data['vt_type'],
        'vt_label': data['vt_label'],
    }
    return HttpResponse(template.render(context, request))

    # return HttpResponse("Hello, world. You're at the CARS index.")