from django.http import JsonResponse

def home(request):

    return JsonResponse({
        'mensagem': 'Marketplace Artesanal API'
    })