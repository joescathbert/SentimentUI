from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from urllib.parse import urlencode
from . import twtex

def home(request):
    if request.GET.get('q'):
        search = request.GET['q']
        base_url = reverse('senti-tweets')  # 1 /products/
        query_string =  urlencode({'q': search})  # 2 category=42
        url = '{}?{}'.format(base_url, query_string)  # 3 /products/?category=42
        return redirect(url)
    else:
        search = 'Ver.1'
    search_api = twtex.TwitterClient()
    context = {
        'happy': search_api.get_tweets("happy",2),
        'sad': search_api.get_tweets("sad",2)
    }
    return render(request, 'senti/home.html', context)

def search(request):
    search = request.GET['q']
    search_api = twtex.TwitterClient()
    tweets = search_api.get_tweets(search,10)
    context = {
        'search': search,
        'tweets': tweets
    }
    return render(request, 'senti/tweets.html', context)
