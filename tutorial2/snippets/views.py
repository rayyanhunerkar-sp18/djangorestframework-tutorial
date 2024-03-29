from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from .models import Snippets
from .serializers import SnippetSerializer

@csrf_exempt
def snippet_list(request):

    if request.method == 'GET':
        snippets = Snippets.objects.all()
        serializer = SnippetSerializer(snippets, many=True)
        return JsonResponse(serializer.data, safe=False)
    
    if request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = SnippetSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

@csrf_exempt
def snippet_detail(request,pk):

    try:
        snippet = Snippets.objects.get(pk=pk)
    except Snippets.DoesNotExist:
        return HttpResponse(status=404)
    
    if request.method == 'GET':
        serializer = SnippetSerializer(snippet)
        return JsonResponse(serializer.data)
    
    if request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = SnippetSerializer(snippet, data = data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    if request.method == 'DELETE':
        snippet.delete()
        return HttpResponse(status=204)