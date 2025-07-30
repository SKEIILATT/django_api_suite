from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from firebase_admin import db
from datetime import datetime

class LandingAPI(APIView):
    # Atributos de la clase
    name = "Landing API"
    collection_name = "data"  # Nombre de la colección en Firebase Realtime Database

        
    def get(self, request):

      # Referencia a la colección
      ref = db.reference(f'{self.collection_name}')

      # get: Obtiene todos los elementos de la col ección
      data = ref.get()

      # Devuelve un arreglo JSON
      return Response(data, status=status.HTTP_200_OK)
    
    
    def post(self, request):
        # Obtener los datos del cuerpo de la solicitud
        obj = request.data.copy()

        # Obtener la fecha y hora actual en el servidor y formatearla
        now = datetime.now()
        am_pm = 'a. m.' if now.strftime('%p').lower() == 'am' else 'p. m.'
        timestamp = now.strftime(f'%d/%m/%Y, %I:%M:%S {am_pm}')
        obj['timestamp'] = timestamp

        # Referencia a la colección en Firebase
        ref = db.reference(self.collection_name)
        new_ref = ref.push(obj)
        obj_id = new_ref.key 
        return Response({'id': obj_id}, status=status.HTTP_201_CREATED)
