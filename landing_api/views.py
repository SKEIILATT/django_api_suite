from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from firebase_admin import db
from datetime import datetime

class LandingAPI(APIView):
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
    
    def get(self, request):
        ref = db.reference(self.collection_name)
        data = ref.get()
        print("DATA FROM FIREBASE:", data)  # Esto aparecerá en la consola del servidor
        items = list(data.values()) if data else []
        return Response(items, status=status.HTTP_200_OK)
    name = "Landing API"
    collection_name = "data"  # Cambia este nombre según tu colección en Firebase

    # Aquí puedes agregar los métodos CRUD (get, post, put, patch, delete)
