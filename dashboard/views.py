from django.http import request, response
import requests
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User

from dashboard.serializers import ArtikelSerializer

from . models import artikelz, kategori
from . foms import ArtikelForms

from rest_framework import serializers, status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import ArtikelSerializer

# Create your views here.


def is_operator(user):
    if user.groups.filter(name='Operator').exists():
        return True
    else:
        return False

@login_required
def dashboard(request):
    if request.user.groups.filter(name='Operator').exists():
        request.session['is_operator'] = 'Operator'
        print(request.session['is_operator'])
    template_name="back/dashboard.html"
    context ={
        'title' : 'dashboard'
    }
    return render(request, template_name, context)


@login_required
def artikel(request):
    templates_name ="back/tabelArtikel.html"
    Artikel = artikelz.objects.filter(nama = request.user)
    #url = 'http://localhost:8000/dashboard/api/artikel/list/682562fa6e59d7f017e536dde51c9a2d3a1af4a33fdab956b4769ae2ee3594dd'
    #user_login ="revie"
    #user_password ="raden210801"
    #x = requests.get(url, auth=(user_login, user_password))
    #if x.status_code == 200:
    # print('request berhasil')
    # data = x.json()['rows']
    # for d in data:
    #     print(d['judul'])
    context = {
        'title':'tabel artikel',
        'artikel' : Artikel,
    }
    return render(request, templates_name, context)

@login_required
def tambah_artikel(request):
    template_name ="back/tambahArtikel.html"
    kategoriz = kategori.objects.all()


    if request.method == "POST":
        forms_artikel = ArtikelForms(request.POST)
        if forms_artikel.is_valid():
            art = forms_artikel.save(commit=False)
            art.nama = request.user
            art.save()
        return redirect(artikel)

    else:
        forms_artikel = ArtikelForms()
    context={
        'title' : 'tambah artikel',
        'kategori' : kategoriz,
        'forms_artikel' : forms_artikel
    }
    return render(request, template_name, context)

@login_required
def lihat_artikel(request, id):
    template_name = "back/lihatArtikel.html"
    artikel = artikelz.objects.get(id=id)
    context ={
        'title' : 'lihat artikel',
        'artikel' : artikel,
    }
    return render(request, template_name, context)

@login_required
def edit_artikel(request, id):
    template_name = "back/tambahArtikel.html"
    a = artikelz.objects.get(id=id)
    if request.method == "POST":
        forms_artikel = ArtikelForms(request.POST, instance=a)
        if forms_artikel.is_valid():
            art = forms_artikel.save(commit=False)
            art.nama = request.user
            art.save()
            return redirect(artikel)
    else:
        form_artikel = ArtikelForms(instance=a)

    context ={
        'title' : 'edit artikel',
        'artikel' : a,
        'forms_artikel' : form_artikel,
    }
    return render(request, template_name, context)

@login_required
def delete_artikel(request, id):
    artikelz.objects.get(id=id).delete()
    return redirect(artikel)
    
@login_required
@user_passes_test(is_operator)
def users(request):
    templates_name ="back/tabelUser.html"
    list_user = User.objects.all()
    context = {
        'title':'tabel users',
        'list_user' : list_user,
    }
    return render(request, templates_name, context)

def _cek_auth(request, x_api_key):
    try:
        key = request.user.api.api_key
    except:
         content = {
            'status' : False,
            'messages' : 'anda belum login'
        }
         return content
     
    if key != x_api_key:
        content = {
            'status' : False,
            'messages' : 'x api key tidak sama'
        }
        return content
    
    return True


@api_view(['GET'])
def artikel_list(request, x_api_key):
    #untuk auth
    cek = _cek_auth(request, x_api_key)
    if cek !=True:
        return Response(cek)    
    
    list = artikelz.objects.all()
    jumlah_artikel = list.count()
    serializer = ArtikelSerializer(list, many=True)
    content = {
        'status' : True,
        'records' : jumlah_artikel,
        'rows' : serializer.data,
    }
    return Response(content)

@api_view(['POST',])    
def artikel_post(request, x_api_key):
    #untuk auth
    cek = _cek_auth(request, x_api_key)
    if cek !=True:
        return Response(cek)   
    
    if request.method == 'POST':
        serializer = ArtikelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            content = {
                'status' : status.HTTP_201_CREATED,
                'messages' : 'berhasil membuat data'
            }
            return Response(content, status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        content ={
            'status' : status.HTTP_405_METHOD_NOT_ALLOWED,
            'message' : 'method tidak ditemukan'
        }
        return Response(content, status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['GET', 'PUT', 'DELETE'])
def artikel_detail(request, pk, x_api_key):
    #untuk auth
    cek = _cek_auth(request, x_api_key)
    if cek !=True:
        return Response(cek)   
    
    try:
        artikel = artikelz.objects.get(pk=pk)
    except artikelz.DoesNotExist:
        content = {
            'status' : status.HTTP_404_NOT_FOUND,
            'messages' : 'artikel tidak ada'
        }
        return Response(content, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ArtikelSerializer(artikel)
        return Response(serializer.data)
    
    

    elif request.method == 'PUT':
        serializer = ArtikelSerializer(artikel, data=request.data)
        if serializer.is_valid():
            serializer.save()
            content ={
                'status' : status.HTTP_202_ACCEPTED,
                'messages' : 'berhasil update',
                'rows' : serializer.data
            }
            return Response(content, status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        artikel.delete()
        content = {
            'status' : status.HTTP_204_NO_CONTENT,
            'messages' : 'berhasil di delete'
        }
        return Response(content, status.HTTP_204_NO_CONTENT)
    
