from django.shortcuts import render


def view_startpage(request):
    return render(request, "startpage/startpage.html", {})
