from .models import *
from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404
from django.template import RequestContext
from django.http import HttpResponse, Http404
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse
from django.views.generic.base import RedirectView

global items_per_page
items_per_page = 24

class ProjectDetailRedirectView(RedirectView):

    def get_redirect_url(self, project):
        return '/artworks/%s/' % project

class AuthorRedirectView(RedirectView):

    def get_redirect_url(self, username):
        return '/artworks/author/%s/' % username

def artwork_list(request, page=1):
    projects = Project.objects.all()
    artworks_list = Artwork.objects.all().order_by('-time')
    get_items_per_page = request.GET.get('items', items_per_page)
    paginator = Paginator(artworks_list, get_items_per_page)
    random_artwork = artworks_list.order_by('?')[0]

    try:
        artworks = paginator.page(page)
    except PageNotAnInteger:
        artworks = paginator.page(1)
    except EmptyPage:
        artworks = paginator.page(paginator.num_pages)

    context = {
        'projects' : projects,
        'artworks' : artworks,
        'categories' : Category.objects.all(),
        'random_artwork' : random_artwork,
        'artists' : Artist.objects.all()
    }
    return render_to_response(
        'artworks/artwork_list.html',
        context,
        context_instance = RequestContext(request),
    )

def artwork_detail(request, pk):
    get_object_or_404(Artwork.objects, pk=pk)
    artworks_list = Artwork.objects.all().order_by('-time')
    artwork = artworks_list.get(pk=pk)
    get_items_per_page = request.GET.get('items', items_per_page)
    paginator = Paginator(artworks_list, get_items_per_page)
    def artwork_page():
        for p in paginator.page_range:
            if (artwork in paginator.page(p)):
                page_number = p
                break
        return page_number
    
    context = {
        'artwork' : artwork,
        'artwork_page' : artwork_page,
    }

    return render_to_response(
        'artworks/artwork_detail.html',
        context,
        context_instance = RequestContext(request),
    )
    
def project_list(request):
    projects = Project.objects.all()
    random_artwork = Artwork.objects.all().order_by('?')[0]

    context = {
        'projects' : projects,
        'authors' : User.objects.all(),
        'random_artwork' : random_artwork,
    }
    return render_to_response(
        'artworks/project_list.html',
        context,
        context_instance = RequestContext(request),
    )

def project_detail(request, project, page=1):
    artworks_list = get_list_or_404(Artwork.objects.order_by('-time'), project__slug=project)
    get_items_per_page = request.GET.get('items', items_per_page)
    paginator = Paginator(artworks_list, get_items_per_page)
    random_artwork = Artwork.objects.filter(project__slug=project).order_by('?')[0]
    
    try:
        artworks = paginator.page(page)
    except PageNotAnInteger:
        artworks = paginator.page(1)
    except EmptyPage:
        artworks = paginator.page(paginator.num_pages)
    
    context = {
        'project' : Project.objects.get(slug=project),
        'artworks' : artworks,
        'random_artwork' : random_artwork,
    }
    return render_to_response(
        'artworks/project_detail.html',
        context,
        context_instance = RequestContext(request),
    )

def project_artwork_detail(request, project, pk):
    get_object_or_404(Artwork.objects, pk=pk, project__slug=project)
    artworks_list = Artwork.objects.filter(project__slug=project).order_by('-time')
    artwork = artworks_list.get(pk=pk)
    get_items_per_page = request.GET.get('items', items_per_page)
    paginator = Paginator(artworks_list, get_items_per_page)
    def artwork_page():
        for p in paginator.page_range:
            if (artwork in paginator.page(p)):
                page_number = p
                break
        return page_number

    try:
        next_artwork = artworks_list.order_by('time').filter(time__gt=artwork.time)[0]
    except:
        next_artwork = False

    try:
        prev_artwork = artworks_list.filter(time__lt=artwork.time)[0]
    except:
        prev_artwork = False
    
    context = {
        'project' : Project.objects.get(slug=project),
        'artwork' : artwork,
        'next_artwork' : next_artwork,
        'prev_artwork' : prev_artwork,
        'artwork_page' : artwork_page,
    }
    return render_to_response(
        'artworks/project_artwork_detail.html',
        context,
        context_instance = RequestContext(request),
    )

def author_detail(request, username, page=1):
    artworks_list = get_list_or_404(Artwork.objects.order_by('-time'), author__username=username)
    get_items_per_page = request.GET.get('items', items_per_page)
    paginator = Paginator(artworks_list, get_items_per_page)

    try:
        artworks = paginator.page(page)
    except PageNotAnInteger:
        artworks = paginator.page(1)
    except EmptyPage:
        artworks = paginator.page(paginator.num_pages)
    
    context = {
        'artworks' : artworks,
        'artist' : Artist.objects.get(user__username=username),
    }
    return render_to_response(
        'artworks/author_detail.html',
        context,
        context_instance = RequestContext(request),
    )
    
def author_artwork_detail(request, username, pk):
    get_object_or_404(Artwork.objects, pk=pk, author__username=username)
    artworks = get_list_or_404(Artwork.objects.order_by('-time'), author__username=username)
    artworks_list = Artwork.objects.filter(author__username=username).order_by('-time')
    artwork = artworks_list.get(pk=pk)
    get_items_per_page = request.GET.get('items', items_per_page)
    paginator = Paginator(artworks_list, get_items_per_page)
    def artwork_page():
        for p in paginator.page_range:
            if (artwork in paginator.page(p)):
                page_number = p
                break
        return page_number
    
    try:
        next_artwork = artworks_list.order_by('time').filter(time__gt=artwork.time)[0]
    except:
        next_artwork = False

    try:
        prev_artwork = artworks_list.filter(time__lt=artwork.time)[0]
    except:
        prev_artwork = False
    
    context = {
        'artist' : Artist.objects.get(user__username=username),
        'artwork' : artwork,
        'next_artwork' : next_artwork,
        'prev_artwork' : prev_artwork,
        'artwork_page' : artwork_page,
    }

    return render_to_response(
        'artworks/author_artwork_detail.html',
        context,
        context_instance = RequestContext(request),
    )

