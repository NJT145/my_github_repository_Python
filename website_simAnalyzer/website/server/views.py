from django.http import HttpResponse, StreamingHttpResponse
from django.shortcuts import render
from django.template import Context, RequestContext
from django.shortcuts import render_to_response, get_object_or_404
import  json
from server.models import Books, UserGroup

def callback(request):
    return render(request, 'serverPage.html')

def userCallback(request):
    #json_data = json.dumps(["string", 1, 2.5, None])
    if request.method == 'GET':
        mail = request.GET.get('mail')
        password = request.GET.get('password')
        actionRequest = request.GET.get('action')
        action = "error"
        info = "noInfo111"
        if actionRequest=='register':
            try:
                json_dict = {}
                json_dict.setdefault('prefered_books', [])
                json_dict.setdefault('similar_books', [])
                UserGroup.objects.create(mail=mail,password=password,info=json_dict)
                action = 'register'
                info = json_dict
            except:
                pass
        elif actionRequest=='login':
            try:
                user1 = UserGroup.objects.get(mail=mail,password=password)
                action = 'login'
                info = user1.info
            except:
                pass
        elif actionRequest=='update':
            try:
                user1 = UserGroup.objects.get(mail=mail,password=password)
                action = 'update'
                prefered_book = request.GET.get('prefered_book')
                similar_book = request.GET.get('similar_book')
                json_dict = user1.info
                if prefered_book not in json_dict['prefered_books']:
                    json_dict['prefered_books'].append(prefered_book)
                if similar_book not in json_dict['similar_books']:
                    json_dict['similar_books'].append(similar_book)
                user1.info = json_dict
                user1.save()
                info = json.dumps(json_dict)
            except:
                pass
        context = {
            'mail': mail,
            'password': password,
            'action': action,
            'info': info
        }
        json_data = json.dumps(context)
        return HttpResponse(json_data, content_type="text/html")

    elif request.method == 'POST':
        pass
        #received_json_data = json.loads(request.body.decode("utf-8"))
        #return StreamingHttpResponse('it was post request: ' + str(received_json_data))