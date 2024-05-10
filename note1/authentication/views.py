from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q


def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        # Create the user
        user = User.objects.create_user(
            username=username, password=password, email=email)
        return JsonResponse({'message': 'User created successfully'})
    else:
        return JsonResponse({'message': 'Method not allowed'}, status=405)


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({'message': 'Login successful'})
        else:
            return JsonResponse({'message': 'Invalid credentials'}, status=400)
    else:
        return JsonResponse({'message': 'Method not allowed'}, status=405)


@csrf_exempt
def upload_pdf(request):
    if request.method == 'POST' and request.FILES.get('pdf'):
        pdf_file = request.FILES['pdf']
        new_pdf = PDFFile(file=pdf_file, name=pdf_file.name)
        new_pdf.save()
        return JsonResponse({'message': 'PDF file uploaded successfully'})
    else:
        return JsonResponse({'message': 'Invalid request'}, status=400)


def search_pdf(request):
    if request.method == 'GET':
        query = request.GET.get('query')
        if query:
            results = PDFFile.objects.filter(Q(name__icontains=query))
            # You can add additional search criteria here
            # For example, search by author, genre, etc.
            return JsonResponse({'results': [{'name': pdf.name, 'url': pdf.file.url} for pdf in results]})
        else:
            return JsonResponse({'message': 'Please provide a search query'}, status=400)
    else:
        return JsonResponse({'message': 'Invalid request'}, status=400)
