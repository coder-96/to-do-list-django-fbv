# from django.http import JsonResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response
from firstapp.models import Todo
from .serializers import TodoSerializer

@api_view(["GET"])
def getRoutes(request):
    routes = [
        "GET /api",
        "GET /api/todo",
        "GET /api/todo/:id"
    ]
    # return JsonResponse(routes, safe=False)
    return Response(routes)

@api_view(["GET"])
def getTodos(request):
    todos = Todo.objects.all()
    serializer = TodoSerializer(todos, many=True)
    return Response(serializer.data)

@api_view(["GET"])
def getTodo(request, pk):
    todo = Todo.objects.get(id=pk)
    serializer = TodoSerializer(todo, many=False)
    return Response(serializer.data)
