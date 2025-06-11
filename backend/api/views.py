from django.http import JsonResponse


# Create your views here.
def health_check(request):
    """Health check endpoint. Returns status confirmation."""
    response = {"status": "ok"}
    return JsonResponse(response)
