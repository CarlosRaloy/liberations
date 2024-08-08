from django.shortcuts import render


def ping(request):
    pong = "Response 200 Ok"
    return render(request, 'panel.html', {'PING': pong})
