from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Supplier
from .serializers import SupplierSerializer


# class SupplierViewSet(viewsets.ModelViewSet):
#     queryset = Supplier.objects.all()
#     serializer_class = SupplierSerializer

class SupplierListApiView(APIView):
    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated]

    # 1. List all
    def get(self, request, *args, **kwargs):
        '''
        List all the todo items for given requested user
        '''
        # Supplier = Supplier.objects.filter(user = request.user.id)
        id = self.request.query_params.get('id')
        if id:
            Supplier = Supplier.objects.get(id=id)
            serializer = SupplierSerializer(Supplier)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        Supplier = Supplier.objects.all()
        serializer = SupplierSerializer(Supplier, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 2. Create
    def post(self, request, *args, **kwargs):
        '''
        Create the Todo with given todo data
        '''
        serializer = SupplierSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 3. Update
    def put(self, request, *args, **kwargs):
        '''
        Update the Todo with given todo data
        '''

        id = self.request.query_params.get('id')
        if id:
            try:
                Supplier = Supplier.objects.get(id=id)
                Supplier.skid = request.data.get("skid")
                Supplier.code = request.data.get("code")
                Supplier.name = request.data.get("name")
                Supplier.description = request.data.get("description")
                Supplier.save()
                return Response(status=status.HTTP_200_OK)
            
            except:
                pass
        

            return Response(status=status.HTTP_404_NOT_FOUND)
        
        return Response(status=status.HTTP_400_BAD_REQUEST)

    # 4. Delete
    def delete(self, request, *args, **kwargs):
        '''
        Delete the Todo with given id
        '''
        id = self.request.query_params.get('id')
        if id:
            Supplier = Supplier.objects.get(id=id)
            Supplier.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(status=status.HTTP_404_NOT_FOUND)