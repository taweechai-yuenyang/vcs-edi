from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Book, Department, Position, ProductGroup, Section, Supplier, OrderType, Product, ProductType, Unit
from .serializers import BookSerializer, DepartmentSerializer, PositionSerializer, ProductGroupSerializer, SectionSerializer, SupplierSerializer,OrderTypeSerializer,ProductTypeSerializer,UnitSerializer,ProductSerializer


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
            obj = Supplier.objects.get(id=id)
            serializer = SupplierSerializer(obj)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        obj = Supplier.objects.all()
        serializer = SupplierSerializer(obj, many=True)
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

        print(serializer.error_messages)
        print(serializer.is_valid())
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


class OrderTypeListApiView(APIView):
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
            obj = OrderType.objects.get(id=id)
            serializer = OrderTypeSerializer(obj)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        obj = OrderType.objects.all()
        serializer = SupplierSerializer(obj, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 2. Create
    def post(self, request, *args, **kwargs):
        '''
        Create the Todo with given todo data
        '''
        serializer = OrderTypeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class ProductTypeListApiView(APIView):
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
            obj = ProductType.objects.get(id=id)
            serializer = ProductTypeSerializer(obj)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        obj = ProductType.objects.all()
        serializer = ProductTypeSerializer(obj, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 2. Create
    def post(self, request, *args, **kwargs):
        '''
        Create the Todo with given todo data
        '''
        serializer = ProductTypeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ProductGroupListApiView(APIView):
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
            obj = ProductGroup.objects.get(id=id)
            serializer = ProductGroupSerializer(obj)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        obj = ProductGroup.objects.all()
        serializer = ProductGroupSerializer(obj, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 2. Create
    def post(self, request, *args, **kwargs):
        '''
        Create the Todo with given todo data
        '''
        serializer = ProductGroupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UnitListApiView(APIView):
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
            obj = Unit.objects.get(id=id)
            serializer = UnitSerializer(obj)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        obj = Unit.objects.all()
        serializer = UnitSerializer(obj, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 2. Create
    def post(self, request, *args, **kwargs):
        '''
        Create the Todo with given todo data
        '''
        serializer = UnitSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class SectionListApiView(APIView):
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
            obj = Section.objects.get(id=id)
            serializer = SectionSerializer(obj)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        obj = Section.objects.all()
        serializer = SectionSerializer(obj, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 2. Create
    def post(self, request, *args, **kwargs):
        '''
        Create the Todo with given todo data
        '''
        serializer = SectionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PositionListApiView(APIView):
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
            obj = Position.objects.get(id=id)
            serializer = PositionSerializer(obj)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        obj = Position.objects.all()
        serializer = PositionSerializer(obj, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 2. Create
    def post(self, request, *args, **kwargs):
        '''
        Create the Todo with given todo data
        '''
        serializer = PositionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class DepartmentListApiView(APIView):
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
            obj = Department.objects.get(id=id)
            serializer = DepartmentSerializer(obj)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        obj = Department.objects.all()
        serializer = DepartmentSerializer(obj, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 2. Create
    def post(self, request, *args, **kwargs):
        '''
        Create the Todo with given todo data
        '''
        serializer = DepartmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class BookListApiView(APIView):
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
            obj = Book.objects.get(id=id)
            serializer = BookSerializer(obj)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        obj = Book.objects.all()
        serializer = BookSerializer(obj, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 2. Create
    def post(self, request, *args, **kwargs):
        '''
        Create the Todo with given todo data
        '''
        ordType = OrderType.objects.get(code=request.data.get('order_type_id'))
        obj = request.POST.copy()
        obj['order_type_id'] = ordType.id
        serializer = BookSerializer(data=obj)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProductListApiView(APIView):
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
            obj = Product.objects.get(id=id)
            serializer = ProductSerializer(obj)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        obj = Product.objects.all()
        serializer = ProductSerializer(obj, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 2. Create
    def post(self, request, *args, **kwargs):
        '''
        Create the Todo with given todo data
        '''
        pGrp = ProductGroup.objects.get(code=request.data.get('prod_group_id'))
        pType = ProductType.objects.get(code=request.data.get('prod_type_id'))
        pUnit = Unit.objects.get(code=request.data.get('unit_id'))
        obj = request.POST.copy()
        obj['prod_type_id'] = pType.id
        obj['prod_group_id'] = pGrp.id
        obj['unit_id'] = pUnit.id
        
        serializer = ProductSerializer(data=obj)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        print(f"Error ==>")
        print(obj)
        print(serializer.error_messages)
        print(f"<==")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)