from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

import uuid

# Simulación de base de datos local en memoria
data_list = []

# Añadiendo algunos datos de ejemplo para probar el GET
data_list.append({'id': str(uuid.uuid4()), 'name': 'User01', 'email': 'user01@example.com', 'is_active': True})
data_list.append({'id': str(uuid.uuid4()), 'name': 'User02', 'email': 'user02@example.com', 'is_active': True})
data_list.append({'id': str(uuid.uuid4()), 'name': 'User03', 'email': 'user03@example.com', 'is_active': False}) # Ejemplo de item inactivo

class DemoRestApi(APIView):
    name = "Demo REST API"
    def get(self, request):

      # Filtra la lista para incluir solo los elementos donde 'is_active' es True
      active_items = [item for item in data_list if item.get('is_active', False)]
      return Response(active_items, status=status.HTTP_200_OK)
    
    def post(self, request):
      data = request.data

      # Validación mínima
      if 'name' not in data or 'email' not in data:
         return Response({'error': 'Faltan campos requeridos.'}, status=status.HTTP_400_BAD_REQUEST)

      data['id'] = str(uuid.uuid4())
      data['is_active'] = True
      data_list.append(data)

      return Response({'message': 'Dato guardado exitosamente.', 'data': data}, status=status.HTTP_201_CREATED)


class DemoRestApiItem(APIView):
    name = "Demo REST API Item"
    
    def _find_item_by_id(self, item_id):
        """Método helper para encontrar un elemento por ID"""
        for item in data_list:
            if item['id'] == item_id:
                return item
        return None
    
    def put(self, request, item_id):
        """PUT - Reemplaza completamente los datos de un elemento"""
        data = request.data
        
        # Validar que el ID esté presente en el cuerpo de la solicitud
        if 'id' not in data:
            return Response({
                'error': 'El campo id es obligatorio en el cuerpo de la solicitud.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Validar que el ID del cuerpo coincida con el ID de la URL
        if data['id'] != item_id:
            return Response({
                'error': 'El ID en el cuerpo de la solicitud debe coincidir con el ID de la URL.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Buscar el elemento existente
        existing_item = self._find_item_by_id(item_id)
        if not existing_item:
            return Response({
                'error': f'No se encontró el elemento con ID: {item_id}'
            }, status=status.HTTP_404_NOT_FOUND)
        
        # Validación mínima de campos requeridos
        if 'name' not in data or 'email' not in data:
            return Response({
                'error': 'Los campos name y email son requeridos.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Reemplazar completamente los datos (manteniendo el ID)
        new_data = {
            'id': item_id,
            'name': data['name'],
            'email': data['email'],
            'is_active': data.get('is_active', True)  # Valor por defecto si no se proporciona
        }
        
        # Encontrar el índice y reemplazar
        for i, item in enumerate(data_list):
            if item['id'] == item_id:
                data_list[i] = new_data
                break
        
        return Response({
            'message': 'Elemento actualizado completamente.',
            'data': new_data
        }, status=status.HTTP_200_OK)
    
    def patch(self, request, item_id):
        """PATCH - Actualiza parcialmente los campos del elemento"""
        data = request.data
        
        # Buscar el elemento existente
        existing_item = self._find_item_by_id(item_id)
        if not existing_item:
            return Response({
                'error': f'No se encontró el elemento con ID: {item_id}'
            }, status=status.HTTP_404_NOT_FOUND)
        
        # Si no hay datos para actualizar
        if not data:
            return Response({
                'error': 'No se proporcionaron datos para actualizar.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Actualizar solo los campos proporcionados
        updated_fields = []
        for key, value in data.items():
            if key != 'id':  # No permitir cambio de ID
                if key in existing_item:
                    existing_item[key] = value
                    updated_fields.append(key)
                else:
                    # Agregar nuevos campos si es necesario
                    existing_item[key] = value
                    updated_fields.append(key)
        
        if not updated_fields:
            return Response({
                'message': 'No se realizaron cambios.',
                'data': existing_item
            }, status=status.HTTP_200_OK)
        
        return Response({
            'message': f'Elemento actualizado parcialmente. Campos modificados: {", ".join(updated_fields)}',
            'data': existing_item
        }, status=status.HTTP_200_OK)
    
    def delete(self, request, item_id):
        """DELETE - Elimina lógicamente un elemento (marca como inactivo)"""
        # Buscar el elemento existente
        existing_item = self._find_item_by_id(item_id)
        if not existing_item:
            return Response({
                'error': f'No se encontró el elemento con ID: {item_id}'
            }, status=status.HTTP_404_NOT_FOUND)
        
        # Verificar si ya está eliminado lógicamente
        if not existing_item.get('is_active', True):
            return Response({
                'error': 'El elemento ya está eliminado.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Eliminación lógica (marcar como inactivo)
        existing_item['is_active'] = False
        
        return Response({
            'message': f'Elemento con ID {item_id} eliminado exitosamente.'
        }, status=status.HTTP_200_OK)