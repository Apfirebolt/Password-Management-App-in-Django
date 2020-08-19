from django.shortcuts import render

# HTTP Error 400


def bad_request(request, exception):
    render(request, '400.html', status=400)

# HTTP Error 403


def no_permissions(request, exception):
    render(request, '403.html', status=403)

# HTTP Error 500, Server Error


def server_error(request):
    render(request, '500.html', status=500)

# HTTP Error 404


def not_found(request, exception):
    render(request, '404.html', status=404)