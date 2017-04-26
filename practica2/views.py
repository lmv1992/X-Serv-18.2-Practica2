from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from models import URLS

# Create your views here.

@csrf_exempt
def show_cms(request):
	lista = URLS.objects.all();
	if request.method == "GET":
		answer = "<html><h3>ENVIE SU URL:</h3>"
		answer += "<h2>Solo envie la URL de la forma: www.maquina.com  o  maquina.com</h2>"
		answer += "<form action='http://localhost:1234' method='POST'>Escribe tu URL:<input type='text' name='nombre' value='' />"
		answer += "<br/>"
		answer += "<input type='submit' value='Enviar' />"
		answer += "</form></html>"
		answer += "<ul>LISTA:"
		for i in range(0,len(lista)):
			answer += "<li>"+lista[i].url+" --> "+ str(i)+"</li>"
		answer += "</ul>"
	elif request.method == "POST":
		pagina = str(request.body)
		pagina = pagina.split('=')[1]
		if not pagina.startswith('www'):
			pagina = "www."+pagina
		if not pagina.startswith('http://'):
			pagina = 'http://' + pagina
		i=0;
		while i<len(lista):
			if pagina !=lista[i].url and i==(len(lista)-1):
				guardar = URLS(url = pagina);
				guardar.save();
				i = len(lista);
				answer = "se ha guardado la pagina: "+pagina+" con el acortador : "+str(len(lista))
			elif pagina !=lista[i].url and i!=(len(lista)-1):
				i = i+1;
			else:
				answer = "La URL ya estaba guardada con el id:"
				answer += "<a href="+lista[i].url+">"+str(i)+"</a>"
				i = len(lista);
	return HttpResponse(answer)

def search_cms(request,recurso):
	lista = URLS.objects.all();
	try:
		if int(recurso) >= 0 and int(recurso) < len(lista):
			url = lista[int(recurso)].url
			answer = "<meta http-equiv='Refresh' content='0;url="+url+"'>"
		else:
			answer = "Not Found"
	except ValueError:
		answer = "Not Found"	
	return HttpResponse(answer)
