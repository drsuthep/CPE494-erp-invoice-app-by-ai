from django.shortcuts import render

def landing_view(request):
    """Renders the landing page."""
    return render(request, "landing.html")