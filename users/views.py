from rest_framework import permissions, generics, views, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import User
from users.permissions import CreateEmployeePermission, CreateCompanyPermission
from users.serializers import UserSerializer, RegistrationCompanyOwnerSerializer, CreateEmployeeSerializer, \
    LoginUserSerializer, CreateCompanySerializer


# Create your views here.

class InfoView(generics.RetrieveUpdateAPIView):
    """Display user info view"""
    model = User
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def get_object(self):
        """Get user data"""
        user = User.objects.filter(id=self.request.user.id).prefetch_related("companies")
        return user[0]


class RegistrationCompanyOwnerView(generics.CreateAPIView):
    """Register company owner view provide only post method"""
    serializer_class = RegistrationCompanyOwnerSerializer
    permission_classes = (permissions.AllowAny, )


class CreateCompanyView(generics.CreateAPIView):
    """Create company view provide only post method"""
    serializer_class = CreateCompanySerializer
    permission_classes = (CreateCompanyPermission, )


class CreateEmployeeView(generics.CreateAPIView):
    """Create employee view provide only post method"""
    serializer_class = CreateEmployeeSerializer
    permission_classes = (CreateEmployeePermission, )


class LoginView(views.APIView):
    """Login user (conditionally) view, get access and refresh tokens"""
    def post(self, request):
        
        serializer = LoginUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            refresh = RefreshToken.for_user(user)
            access_token: str = str(refresh.access_token)
            return Response({"access": str(access_token),
                             "refresh": str(refresh)},
                            status=status.HTTP_200_OK)
        return Response({"error": "Unexpected error"})


class LogoutView(views.APIView):
    """
    Logout user (conditionally) view, after user logout token lifetime not ended,
    and still available retrieve data with token
    """
    def post(self, request):
        
        return Response({"message": "Logout successfully"},
                        status=status.HTTP_200_OK)
