from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics, mixins, status
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from accounts.models import User
from constants import ACCESS_DENIED, VENDOR_NOT_APPROVED, VENDOR_DELETED
from vendors.models import VendorCategories, VendorRegistration, VendorImages
from vendors.serializers import VendorCategoriesSerializer, VendorRegistrationSerializer, ApproveVendorSerializer, \
    VendorUpdateSerializer, VendorImageSerializer, GetVendorDetailsSerializer


class GetVendorCategoriesView(generics.GenericAPIView, mixins.ListModelMixin):
    """
    to get a list of vendor categories
    """
    serializer_class = VendorCategoriesSerializer
    queryset = VendorCategories.objects.all().order_by('id')

    def get(self, request):
        return self.list(request)


class VendorCategoriesViewSet(viewsets.ModelViewSet):
    """
    to insert, update and delete vendor categories
    """
    serializer_class = VendorCategoriesSerializer
    queryset = VendorCategories.objects.all().order_by('id')
    permission_classes = [IsAdminUser]


class VendorRegistrationView(generics.GenericAPIView, mixins.CreateModelMixin):
    """
    class for vendor registration
    """
    serializer_class = VendorRegistrationSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        request.data['user'] = request.user.id
        serializer = self.get_serializer(data=request.data, context={'user': request.user, 'data': request.data})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class ApproveVendorView(generics.GenericAPIView, mixins.UpdateModelMixin):
    """
    class to approve vendor
    """
    permission_classes = [IsAdminUser]
    serializer_class = ApproveVendorSerializer
    queryset = VendorRegistration.objects.all()
    lookup_field = 'id'

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        vendor = User.objects.filter(id=instance.user_id)
        email = vendor[0].email
        serializer = self.get_serializer(instance, data=request.data, context={'email': email})
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


class VendorDetails(generics.GenericAPIView, mixins.UpdateModelMixin, mixins.DestroyModelMixin):
    """
    class to update vendor details and delete vendor
    """
    serializer_class = VendorUpdateSerializer
    permission_classes = [IsAuthenticated]
    queryset = VendorRegistration.objects.all()
    lookup_field = 'id'

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.user == instance.user:
            if instance.is_approved:
                serializer = self.get_serializer(instance, data=request.data)
                serializer.is_valid(raise_exception=True)
                self.perform_update(serializer)
                return Response(serializer.data)
            else:
                return Response({'msg': VENDOR_NOT_APPROVED}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'msg': ACCESS_DENIED}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.user == instance.user:
            if instance.is_approved:
                self.perform_destroy(instance)
                return Response({'msg': VENDOR_DELETED}, status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({'msg': VENDOR_NOT_APPROVED}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'msg': ACCESS_DENIED}, status=status.HTTP_400_BAD_REQUEST)


class VendorImageView(generics.GenericAPIView, mixins.CreateModelMixin, mixins.UpdateModelMixin,
                      mixins.DestroyModelMixin):
    """
    class to add, update and delete vendor images
    """
    serializer_class = VendorImageSerializer
    queryset = VendorImages.objects.all()
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        vendor = instance.vendor_id
        user = VendorRegistration.objects.filter(id=vendor)

        if user[0].user_id == request.user.id:
            request.data._mutable = True
            request.data['vendor'] = vendor
            serializer = self.get_serializer(instance, data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data)
        else:
            return Response({'msg': ACCESS_DENIED}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        vendor = instance.vendor_id
        user = VendorRegistration.objects.filter(id=vendor)

        if user[0].user_id == request.user.id:
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'msg': ACCESS_DENIED}, status=status.HTTP_400_BAD_REQUEST)


class GetVendorInformationView(generics.GenericAPIView, mixins.RetrieveModelMixin):
    """
    class to get vendor's data
    """
    serializer_class = GetVendorDetailsSerializer
    queryset = VendorRegistration.objects.all()
    lookup_field = 'id'
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class GetAllVendors(generics.GenericAPIView, mixins.ListModelMixin):
    """
    class to show all vendors of a category
    """
    serializer_class = VendorRegistrationSerializer
    queryset = VendorRegistration.objects.filter(is_approved=True).order_by('id')
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['vendor_category']
    search_fields = ['vendor_details']

    def get(self, request):
        return self.list(request)
