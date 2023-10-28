import requests
from django.http import JsonResponse, HttpResponse

from django.shortcuts import render


def mainpage_view(request):
    if request.method == 'POST':
        data = request.POST.get("data")
        file = request.FILES.get("file")
        url = request.POST.get("url")

        if not file:
            return JsonResponse({"message": "No se ha seleccionado un archivo."})
        
        try:
            files = {"file": (file.name, file.read())}
            response = requests.post(url, data={"data": data}, files=files)
            response.raise_for_status()

            response_data = response.json()
            return JsonResponse(response_data)
        except requests.exceptions.RequestException as e:
            return HttpResponse(str(e), status=500)
        
    return render(request, 'mainpage.html')

def menciones_view(request):
    menciones = {}

    if request.method == 'POST':
        data = request.POST.get("data")
        url = request.POST.get("url")
        fecha_in = request.POST.get("fecha_in")
        fecha_fin = request.POST.get("fecha_fin")

        try :
            response = requests.post("http://127.0.0.1:5000/devolverMenciones", data={"fecha_in": fecha_in, "fecha_fin": fecha_fin},)
            response.raise_for_status()
            # menciones = response.menciones
            # print(menciones)
            response_data = response.json()
            menciones = response_data["menciones"]

            return JsonResponse(response_data)
        except requests.exceptions.RequestException as e:
            return HttpResponse(str(e), status=500)

    return render(request, 'menciones.html', {"menciones": menciones})

def hashtags_view(request):
    hashtags = {}

    if request.method == 'POST':
        data = request.POST.get("data")
        url = request.POST.get("url")
        fecha_in = request.POST.get("fecha_in")
        fecha_fin = request.POST.get("fecha_fin")

        try :
            response = requests.post("http://127.0.0.1:5000/devolverHashtags", data={"fecha_in": fecha_in, "fecha_fin": fecha_fin},)
            response.raise_for_status()
            # menciones = response.menciones
            # print(menciones)
            response_data = response.json()
            hashtags = response_data["hashtags"]

            print("hashtags:",hashtags)
            return JsonResponse(response_data)
        except requests.exceptions.RequestException as e:
            return HttpResponse(str(e), status=500)

    return render(request, 'hashtags.html', {"hashtags": hashtags})

def sentimientos_view(request):
    sentimientos = {}

    if request.method == 'POST':
        data = request.POST.get("data")
        url = request.POST.get("url")
        fecha_in = request.POST.get("fecha_in")
        fecha_fin = request.POST.get("fecha_fin")

        try :
            response = requests.post("http://127.0.0.1:5000/devolverSentimientos", data={"fecha_in": fecha_in, "fecha_fin": fecha_fin},)
            response.raise_for_status()
            # menciones = response.menciones
            # print(menciones)
            response_data = response.json()
            sentimientos = response_data["respuesta"]

            print("sentimientos:",sentimientos)
            return JsonResponse(response_data)
        except requests.exceptions.RequestException as e:
            return HttpResponse(str(e), status=500)
        
    return render(request, 'sentimientos.html', {"sentimientos": sentimientos})

def ayuda(request):
    return render(request, 'ayuda.html')