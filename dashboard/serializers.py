from rest_framework.serializers import ModelSerializer
from . models import artikelz

class ArtikelSerializer(ModelSerializer):
    class Meta:
        model = artikelz
        fields = ['id', 'nama', 'judul', 'body', 'kategory', 'date']