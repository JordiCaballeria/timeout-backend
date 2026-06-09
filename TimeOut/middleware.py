from django.http import JsonResponse

# Endpoints de sola lectura que necessiten POST per funcionar (autenticació)
WRITE_ALLOWED_PATHS = {
    '/api/auth/login/',
    '/api/auth/token/refresh/',
}


class ReadOnlyMiddleware:
    """
    Bloqueja totes les peticions que modifiquen dades (POST, PUT, PATCH, DELETE)
    excepte els endpoints d'autenticació, que necessiten POST per funcionar.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method in ('POST', 'PUT', 'PATCH', 'DELETE'):
            if request.path not in WRITE_ALLOWED_PATHS:
                return JsonResponse(
                    {'detail': 'Aquesta aplicació és de només lectura. No es permeten modificacions.'},
                    status=405,
                )
        return self.get_response(request)
