from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from .models import Vehicle_Setting

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from vehicles.views import _getVehicleTypes


###############################
# Settings
###############################
@login_required(login_url='/vehicles/login/')
def settings(request):

    MSG = ''

    data = _getVehicleTypes(request.user)

    Q_S = Vehicle_Setting.objects.filter(login=request.user, type=data['vt_id'])

    print(Q_S)

    template = loader.get_template('settings/setting.html')
    context = {
        'vt_list': data['vt_list'],
        'vt_type': data['vt_type'],
        'vt_label': data['vt_label'],
        'Q_S': Q_S,
        'MSG': MSG,
    }
    return HttpResponse(template.render(context, request))

    # return HttpResponse('TEst')
