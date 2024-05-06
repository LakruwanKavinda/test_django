from rest_framework.decorators import api_view
from rest_framework.response import Response
import json  # Add import for json module

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from .models import PDFFile


@api_view(['GET'])
def getRoutes(request):
    routes = [
        {
            'Endpoint': '/notes/',
            'method': 'GET',
            'body': None,
            'description': 'Returns an array of notes'
        },
        {
            'Endpoint': '/notes/',
            'method': 'GET',
            'body': None,
            'description': 'Returns a single note object'
        },
        {
            'Endpoint': '/notes/create/',
            'method': 'POST',
            'body': {'body': ""},
            'description': 'Creates new note with data sent in post request'
        },
        {
            'Endpoint': '/notes/id/update/',
            'method': 'PUT',
            'body': {'body': ""},
            'description': 'Creates an existing note with data sent in'
        },
        {
            'Endpoint': '/notes/id/delete/',
            'method': 'DELETE',
            'body': None,
            'description': 'Delete and existing note'
        },
    ]
    return Response(routes)

# Rest of the views...


def signup(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        if username and password:
            # Check if the username is already taken
            if User.objects.filter(username=username).exists():
                return JsonResponse({'error': 'Username already exists'}, status=400)
            # Create the user
            user = User.objects.create_user(
                username=username, password=password)
            # Authenticate the user
            user = authenticate(request, username=username, password=password)
            if user is not None:
                return JsonResponse({'token': 'your_auth_token'}, status=201)
            else:
                return JsonResponse({'error': 'Authentication failed'}, status=400)
        else:
            return JsonResponse({'error': 'Invalid request'}, status=400)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)


def user_login(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        if username and password:
            # Authenticate the user
            user = authenticate(request, username=username, password=password)
            if user is not None:
                return JsonResponse({'token': 'your_auth_token'}, status=200)
            else:
                return JsonResponse({'error': 'Invalid username or password'}, status=400)
        else:
            return JsonResponse({'error': 'Invalid request'}, status=400)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)


def upload_pdf_view(request):
    if request.method == 'POST':
        form = UploadPDFForm(request.POST, request.FILES)
        if form.is_valid():

            pdf_file = form.cleaned_data['pdf_file']

    else:
        form = UploadPDFForm()
    return render(request, 'upload_pdf.html', {'form': form})


def search_pdf(request):
    if request.method == 'GET':
        query = request.GET.get('query')
        if query:
            # Perform search based on the query
            pdf_files = PDFFile.objects.filter(title__icontains=query)
        else:
            # If no query provided, return all PDF files
            pdf_files = PDFFile.objects.all()

        return render(request, 'search_results.html', {'pdf_files': pdf_files, 'query': query})


def view_pdf(request, pdf_id):
    pdf = get_object_or_404(PDFFile, pk=pdf_id)
    with open(pdf.pdf_file.path, 'rb') as pdf_file:
        response = HttpResponse(
            pdf_file.read(), content_type='application/pdf')
        response['Content-Disposition'] = f'inline; filename="{pdf.title}.pdf"'
        return response
