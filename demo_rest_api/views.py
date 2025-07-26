from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

import uuid

data_list = []

# Añadiendo algunos datos de ejemplo para probar el GET
data_list.append({'id': str(uuid.uuid4()), 'name': 'User01', 'email': 'user01@example.com', 'is_active': True})
data_list.append({'id': str(uuid.uuid4()), 'name': 'User02', 'email': 'user02@example.com', 'is_active': True})
data_list.append({'id': str(uuid.uuid4()), 'name': 'User03', 'email': 'user03@example.com', 'is_active': False}) # Ejemplo de item inactivo

class DemoRestApi(APIView):
    name = 'Demo REST API'
    
    def get(self, request):
        """
        Maneja el método GET para retornar la lista de datos
        """
        return Response(data_list, status=status.HTTP_200_OK)
    
    def post(self, request):
        """
        Maneja el método POST para crear nuevos datos
        """
        data = request.data
        
        # Validar que los campos name y email estén presentes
        if 'name' not in data or 'email' not in data:
            return Response(
                {'error': 'Los campos name y email son requeridos'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Si los campos son válidos
        data['id'] = str(uuid.uuid4())
        data['is_active'] = True
        
        # Agregar a la lista
        data_list.append(data)
        
        # Retornar respuesta exitosa
        return Response(
            {
                'message': 'Datos guardados exitosamente',
                'data': data
            },
            status=status.HTTP_201_CREATED
        )


class DemoRestApiItem(APIView):
    name = 'Demo REST API Item'
    
    def put(self, request, item_id):
        """
        Maneja el método PUT para reemplazar completamente un elemento
        """
        data = request.data.copy()
        data['id'] = item_id  # Usar el id de la URL
        
        # Buscar el elemento en la lista
        for i, item in enumerate(data_list):
            if item['id'] == item_id:
                # Reemplazar completamente excepto el id
                new_item = data.copy()
                new_item['id'] = item_id  # Mantener el id original
                data_list[i] = new_item
                
                return Response(
                    {
                        'message': 'Elemento reemplazado exitosamente',
                        'data': new_item
                    },
                    status=status.HTTP_200_OK
                )
        
        return Response(
            {'error': 'Elemento no encontrado'}, 
            status=status.HTTP_404_NOT_FOUND
        )
    
    def patch(self, request, item_id):
        """
        Maneja el método PATCH para actualizar parcialmente un elemento
        """
        data = request.data
        
        # Buscar el elemento en la lista
        for item in data_list:
            if item['id'] == item_id:
                # Actualizar solo los campos proporcionados
                for key, value in data.items():
                    if key != 'id':  # No actualizar el id
                        item[key] = value
                
                return Response(
                    {
                        'message': 'Elemento actualizado exitosamente',
                        'data': item
                    },
                    status=status.HTTP_200_OK
                )
        
        return Response(
            {'error': 'Elemento no encontrado'}, 
            status=status.HTTP_404_NOT_FOUND
        )
    
    def delete(self, request, item_id):
        """
        Maneja el método DELETE para eliminar lógicamente un elemento
        """
        # Buscar el elemento en la lista
        for item in data_list:
            if item['id'] == item_id:
                # Eliminación lógica: marcar como inactivo
                item['is_active'] = False
                
                return Response(
                    {
                        'message': 'Elemento eliminado lógicamente',
                        'data': item
                    },
                    status=status.HTTP_200_OK
                )
        
        return Response(
            {'error': 'Elemento no encontrado'}, 
            status=status.HTTP_404_NOT_FOUND
        )
