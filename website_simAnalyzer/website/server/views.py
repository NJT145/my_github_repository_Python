from django.shortcuts import render
from django.template import Context, RequestContext
from django.shortcuts import render_to_response, get_object_or_404
import  json
from server.models import Books, UserGroup

def callback(request):
    return render(request, 'serverPage.html')

def userCallback(request):
    json_data = json.dumps(["string", 1, 2.5, None])
    a = request.method == 'POST'
    b = request.method == 'GET' #True
    if request.method == 'GET':
        mail = request.GET.get('mail')
        password = request.GET.get('password')
        action = request.GET.get('action')
        context = {
            'mail': mail,
            'password': password,
            'action': action,
        }
        UserGroup.objects.create(mail=mail,password=password)
        return render(request, 'user.html', context)

    elif request.method == 'POST':
        pass