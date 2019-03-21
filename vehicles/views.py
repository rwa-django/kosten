from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.shortcuts import redirect
from .models import Vehicle_Fuel, Vehicle_Fuel_Pos, Vehicle_Type

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
        'vt_id': Q_Type[0],
    }


def set_vehicle_type(request, type_id):

    q = Vehicle_Type.objects.filter(login=request.user).update(aktiv=False)
    q = Vehicle_Type.objects.filter(login=request.user, id=type_id).update(aktiv=True)

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def _save_amount(login, type, km, chf, ltr):

    Q_V = Vehicle_Fuel.objects.filter(login=login, type=type)
    if not Q_V:
        Q = Vehicle_Fuel(login=login, type=type, info='init header')
        Q.save()

        Q_V = Vehicle_Fuel.objects.filter(login=login, type=type)

    ID_V = Q_V[0].pk
    Q_Pos = Vehicle_Fuel_Pos.objects.filter(fuel_id=ID_V)

    last_pos = 0
    last_km = 0
    average = 0
    for pos in Q_Pos.order_by('pos'):
        last_pos = pos.pos
        last_km = pos.km

    if last_km < km:
        average = ltr / ((km - last_km) / 100)

        ap = Vehicle_Fuel_Pos(fuel_id=Q_V[0], pos=last_pos + 1, amount=chf, km=km, liter=ltr, average=average, info='info text')
        ap.save()
    else:
        return {'ERROR': 'Fehler bei Eingabe!'}

    return {'SUCCESS': 'Daten gespeichert'}


###############################
# Vehicles
###############################
@login_required(login_url='/vehicles/login/')
def index(request):

    data = _getVehicleTypes(request.user)

    MSG = ''
    try:
        amount_km = int(request.POST['amount-km'])
        amount_chf = float(request.POST['amount-chf'])
        amount_ltr = float(request.POST['amount-ltr'])
    except:
        amount_km = 0
        amount_chf = 0
        amount_ltr = 0
    if amount_km != 0:
        MSG = _save_amount(request.user, data['vt_id'], amount_km, amount_chf, amount_ltr)

    Q_V_Pos = []
    last = {}
    Q_V = Vehicle_Fuel.objects.filter(login=request.user, type=data['vt_id'])
    if Q_V:
        Q_V_Pos = Vehicle_Fuel_Pos.objects.filter(fuel_id=Q_V[0])

        for pos in Q_V_Pos.order_by('pos'):
            last_av = pos.average
            last_km = pos.km
            last_date = pos.booked
            last = {
                'last_average': last_av,
                'last_km': last_km,
                'last_date': last_date,
            }

    template = loader.get_template('vehicles/index.html')
    context = {
        'last': last,
        'vt_list': data['vt_list'],
        'vt_type': data['vt_type'],
        'vt_label': data['vt_label'],
        'Q_V_Pos': Q_V_Pos,
        'MSG': MSG,
    }
    return HttpResponse(template.render(context, request))

def upd_vehicle_pos(request, pos):

    msg = ''
    login = request.user

    Q_Type = Vehicle_Type.objects.filter(login=login,
                                         aktiv=True)
    Q_V = Vehicle_Fuel.objects.filter(login=login, type=Q_Type[0])

    try:
        amount = int(request.POST['amount'])
        info = request.POST['info']
    except:
        amount = 0
        info = ''

    if amount != 0:
        val = amount
        ap = Vehicle_Fuel_Pos.objects.filter(fuel_id=Q_V[0], pos=pos).update(amount=val, booking_info=info)

        msg = 'Ihr Daten wurden gespeichert'

    Q_Pos = Vehicle_Fuel_Pos.objects.filter(fuel_id=Q_V[0], pos=pos)

    context = {'POS': Q_Pos,
               'MSG': msg,}

    template = loader.get_template('vehicles/vehicle-upd-pos.html')
    return HttpResponse(template.render(context, request))


def del_vehicle_pos(request, pos):

    Q_Type = Vehicle_Type.objects.filter(login=request.user,
                                         aktiv=True)

    Q_V = Vehicle_Fuel.objects.filter(login=request.user, type=Q_Type[0])

    Q_Pos = Vehicle_Fuel_Pos.objects.filter(fuel_id=Q_V[0], pos=pos)
    Q_Pos.delete()

    msg = 'Position gelöscht'

    print('--DEL POS:', Q_Pos)

    return redirect('/vehicles')
