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

def ayuda(request):
    return render(request, 'ayuda.html')