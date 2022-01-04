from django import forms
from django.forms import fields, widgets
from .models import artikelz

class ArtikelForms(forms.ModelForm):
    class Meta:
        model = artikelz
        fields = ('judul', 'body', 'kategory')
        widgets = {
            "judul" : forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'type': 'text',
                    'placeholder':"Judul Artikel",
                    'required': True,
                }
            ),
            # cols="30" rows="10" class="form-control" placeholder="Isi Berita"
            "body" : forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'cols': "30",
                    'rows': "10",
                    'placeholder':"Isi Berita",
                    'required': True,
                }
            ),
            "kategory" : forms.Select(
                attrs={
                    'class': 'selectpicker',
                    'required': True,
                    'data-style' : 'btn  btn-block',
                    'title' : "Kategory",
                    'data-size' : '7',
                }
            )
        }