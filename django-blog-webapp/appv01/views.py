from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def welcome(request):
    return HttpResponse("Helli from the appv01 !!")

def feed_func(request):
    # Dummy data to simulate database records

    # here a long pera to check my Expand button XD 😌

    pera="Sydney Sweeney has emerged as a definitive symbol " \
    "of 21st-century beauty, celebrated for a look that blends " \
    "classic Hollywood glamour with a refreshing, unfiltered authenticity. " \
    "Often hailed as a classical beauty her features—including bright, expressive " \
    "eyes, a defined jawline, and high cheekbones—have even been noted for their alignment " \
    "with the golden ratio of aesthetic proportions. Beyond these formal measures, her appeal " \
    "lies in her versatility and unapologetic self-love, whether she is gracing the red carpet " \
    "in high-fashion couture or sharing makeup-free photos " \
    "that challenge traditional industry standards. This magnetic charm, " \
    "which she describes as a form of self-expression, combines a powerful " \
    "screen presence with a grounded, natural glow that resonates with fans worldwide."




    posts = [
        {
            'author': 'dev_shabbir',
            'title': 'The Radiant Authenticity of Sydney Sweeney',
            'content': pera,
            'date_posted': '2 hours ago',
            'likes': 12,
            'comments': 5,
            'tags': ['Backend', 'Security'],
            'attach_png':'/static/appv01/images/sweeny.jpg'
        },
        {
            'author': 'python_wizard',
            'title': 'Why Python 3.14 is a Game Changer',
            'content': 'Exploring the new performance improvements and how the GIL changes affect your backend scaling...',
            'date_posted': '5 hours ago',
            'likes': 45,
            'comments': 10,
            'tags': ['Python', 'Updates'],
            'attach_png': None
        },
        {
            'author': 'dev_shabbir',
            'title': 'The Radiant Authenticity of Sydney Sweeney',
            'content': pera,
            'date_posted': '2 hours ago',
            'likes': 12,
            'comments': 5,
            'tags': ['Backend', 'Security'],
            'attach_png':'/static/appv01/images/sweeny.jpg'
        }
    ]
    
    context = {
        'posts': posts
    }
    return render(request, 'appv01/feed.html', context)


def create_post_view(request):
    return render(request,'appv01/createpost.html')

def login_view(request):
    return render(request,'appv01/login.html')

def registration_view(request):
    return render(request,'appv01/registration.html')