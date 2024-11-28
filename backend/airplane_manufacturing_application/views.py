# from django.shortcuts import render
from .models import Airplane, Part, Team, Employee, AirplaneType,PartType
from .serializers import AirplaneSerializer, PartSerializer, TeamSerializer, EmployeeSerializer, AirplaneTypeSerializer,PartTypeSerializer, DatatableParamsSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework import status,viewsets,generics
from django.http import HttpResponse
from django.utils.safestring import mark_safe
import markdown
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.db.models import Count
import os
from django.shortcuts import get_object_or_404
import jwt
from django.conf import settings
from rest_framework.exceptions import NotFound
# Create your views here.

#region token
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        # Kullanıcıya ait employee bilgileri
        try:
            employee = Employee.objects.get(user_id=self.user.id)
            team = Team.objects.get(id=employee.team_id)

            data['employee'] = {
                'id': employee.id,
                'name': employee.name,
                'team_id': employee.team_id,  
            }
            data['team'] = {
                'id': team.id,
                'name': team.name,
                'part_type_name': team.part_type.name if team.part_type else None,
                'part_type_id': team.part_type.id if team.part_type else None,
                'is_assembly_team':team.is_assembly_team  
            }

        except Team.DoesNotExist:
            data['team'] = None
            data['employee'] = {
                'id': employee.id,
                'name': employee.name,
                'team_id': employee.team_id,  
            }
            
        return data

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

def get_user_info_from_token(request):
    token = request.headers.get('Authorization')  # Header'dan token alır
    print(token[7:])
    if token:
        try:
            # Token'ı çözümler
            decoded_token = jwt.decode(token[7:],  settings.SECRET_KEY, algorithms=['HS256'])
            user_id = decoded_token.get('user_id', None)
            employee = Employee.objects.get(id=user_id)
            
            user_info = {
                "employee":employee,
                "team": employee.team,
                "is_admin": True if user_id == 1 else False
            } 
            return user_info
        except jwt.ExpiredSignatureError:
            print("jwt.ExpiredSignatureError")
            return None
        except jwt.DecodeError:
            print("jwt.DecodeError")
            return None
        except:
            print("hata")
            return None
    return None
#endregion

#region mainpage readme
def readme_view(request):
    app_dir = os.path.dirname(os.path.abspath(__file__))  
    readme_path = os.path.join(app_dir, "README.md")
    try:
        with open(readme_path, "r", encoding="utf-8") as file:
            content = file.read()
        # Markdown'u HTML'e dönüştür
        html_content = markdown.markdown(content)
        return HttpResponse(mark_safe(html_content))
    except FileNotFoundError:
        return HttpResponse("README.md dosyası bulunamadı.", status=404)
#endregion

#region Temel Viewlar
class AirplaneViewSet(viewsets.ModelViewSet):
    queryset = Airplane.objects.all()
    serializer_class = AirplaneSerializer

# class PartViewSet(viewsets.ModelViewSet):
#     queryset = Part.objects.all()
#     serializer_class = PartSerializer

# class TeamViewSet(viewsets.ModelViewSet):
#     queryset = Team.objects.all()
#     serializer_class = TeamSerializer

class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

class PartAPIView(APIView):
    @swagger_auto_schema(
        operation_description="Yeni bir parça oluştur",
        request_body=PartSerializer,  
        responses={201: PartSerializer}
    )
    def post(self, request):
        serializer = PartSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)  # 201 Created: başarıyla oluşturuldu
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # 400 Bad Request: Hatalı veri
    
    @swagger_auto_schema(operation_description="Parçayı güncelle") ## uygulamada kullanılmadığı için ek geliştirme yapılmadı
    def put(self, request, id):
        return Response("Ek Geliştirme Yapılmadı", status=status.HTTP_400_BAD_REQUEST)
        try:
            part = Part.objects.get(id=id)
        except Part.DoesNotExist:
            raise NotFound(detail="Part not found", code=404)
        
        serializer = PartSerializer(part, data=request.data, partial=False)  # False for full update, True for partial
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @swagger_auto_schema(
        manual_parameters=[openapi.Parameter('id', openapi.IN_PATH, description="Silinecek parçanın id'si", type=openapi.TYPE_INTEGER)],
        operation_description="Partayı sil",
        responses={204: "No Content", 404: "Not Found"}  # Başarılı silme için 204 döner, 404 silinmek istenen parça bulunamazsa döner
    )
    def delete(self, request, id, *args, **kwargs):
        print(id)
        try:
            part = Part.objects.get(pk=id)
            part.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)  # 204: Başarıyla silindi
        except Part.DoesNotExist:
            return Response({"detail": "Part not found."}, status=status.HTTP_404_NOT_FOUND)  # 404: Parça bulunamadı
#endregion

#region Datatables işlemlerini yapmak için temel sınıf 
class BaseListView(APIView):
    model = None
    serializer_class = None

    @swagger_auto_schema(
        request_body=DatatableParamsSerializer,
        responses={status.HTTP_200_OK: None}
    )
    def post(self, request, *args, **kwargs):
        # Datatables parametreleri
        datatable_params = DatatableParamsSerializer(data=request.data)
        if not datatable_params.is_valid():
            return Response(datatable_params.errors, status=status.HTTP_400_BAD_REQUEST)

        start = datatable_params.validated_data['start']
        length = datatable_params.validated_data['length']
        search_value = datatable_params.validated_data['search_value']
        order_column = datatable_params.validated_data['order_column']  # string değer
        order_dir = datatable_params.validated_data['order_dir']

        # valid_columns = ['id', 'name', 'create_date', 'related_model__title']  
        # if order_column not in valid_columns:
        #     return Response({"error": f"Invalid order column: {order_column}"}, status=status.HTTP_400_BAD_REQUEST)

        order_by = order_column
        if order_dir == 'desc':
            order_by = '-' + order_by

         # Dinamik arama işlemi (özelleştirilebilir)
        queryset = self.model.objects.all()
        if search_value:
            query_filter = Q()
            
            # Modelin tüm alanlarını al ve arama filtresini oluştur
            for field in self.model._meta.get_fields():
                field_name = field.name

                # Eğer ilişkilendirilmiş bir modelse (ForeignKey, OneToOneField vb.)
                if field.is_relation:
                    # İlişkili modelin adını almak için:
                    related_model = field.related_model
                    
                    # İlişkili modeldeki 'name' gibi bir alanda arama yap
                    print("related_model",related_model)
                    if hasattr(related_model, 'name'):  # İlişkili modelin 'name' alanı varsa
                        query_filter |= Q(**{f"{field_name}__name__icontains": search_value})

                else:
                    # İlişkili olmayan alanda (örneğin: 'create_date', 'id') arama yapılır
                    query_filter |= Q(**{f"{field_name}__icontains": search_value})
            
            queryset = queryset.filter(query_filter)

        # Sayfalama ve sıralama
        total_count = self.model.objects.count()
        filtered_count = queryset.count()
        queryset = queryset.order_by(order_by)[start:start + length]
        serializer = self.serializer_class(queryset, many=True)

        response_data = {
            "draw": request.data.get('draw', 0),
            "recordsTotal": total_count,
            "recordsFiltered": filtered_count,
            "data": serializer.data
        }

        return Response(response_data)
#endregion

#region datatables view'ları

# AirplaneListView
class AirplaneListView(BaseListView):
    model = Airplane
    serializer_class = AirplaneSerializer

class PartListViewByAirplaneId(BaseListView):
    def get(self, request, airplane_id, *args, **kwargs):
        parts = Part.objects.filter(airplane_id=airplane_id)
        
        if not parts.exists():
            return Response({"detail": "Parça mevcut değil."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = PartSerializer(parts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class PartListViewByUavTypeId(BaseListView):
    def get(self, request, airplane_type_id, *args, **kwargs):
        if airplane_type_id==0:
            parts = Part.objects.filter(airplane_id__isnull=True)
        else: 
            parts = Part.objects.filter(airplane_type_id=airplane_type_id,airplane_id__isnull=True)
        
        if not parts.exists():
            return Response({"detail": "Parça mevcut değil."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = PartSerializer(parts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class PartListViewByUavTypeIdPartTypeCounts(APIView):
    def get(self, request, airplane_type_id, *args, **kwargs):
        if airplane_type_id==0:
            parts_grouped = Part.objects.filter(airplane_id__isnull=True).values('part_type').annotate(part_count=Count('part_type'))
        else: 
            parts_grouped = Part.objects.filter(airplane_type_id=airplane_type_id,airplane_id__isnull=True).values('part_type').annotate(part_count=Count('part_type'))

        # Eğer grup yoksa
        if not parts_grouped:
            return Response({"detail": "Grup bulunamadı."}, status=status.HTTP_404_NOT_FOUND)

        # Gruplama sonucu her bir part_type ile birlikte dönen veri
        return Response(parts_grouped, status=status.HTTP_200_OK)

class PartListViewByTeamId(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                name='team_id',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_INTEGER,
                required=True
            )
        ],
        responses={
            200: AirplaneSerializer(many=True),
            400: "team_id parametresi gereklidir.",
            404: "Bulunamadı."
        }
    )
    def get(self, request):
        user_info = get_user_info_from_token(request)

        # team_id query parametresini alır
        team_id = request.query_params.get('team_id')

        # Eğer admin değilse ve takım ID'si eşleşmiyorsa yetkisiz hata döndür
        if user_info["is_admin"] is not True:
            if str(team_id) != str(user_info["team"].id):
                return HttpResponse('Unauthorized', status=401)

        
        # Team nesnesini getir, yoksa 404 döner
        team = get_object_or_404(Team, id=team_id)
        
        parts = Part.objects.filter(part_type=team.part_type,airplane__isnull=True)
        
        # Part'ları serialize ederek döndürür
        serializer = PartSerializer(parts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class TeamListView(APIView):
    def get(self, request, *args, **kwargs):
        teams = Team.objects.all()
        serializer = TeamSerializer(teams, many=True)        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class EmployeeListView(BaseListView):
    model = Employee
    serializer_class = EmployeeSerializer

class EmployeeListViewByTeamId(APIView):
    
    def get(self, request, team_id, *args, **kwargs):        
        employees = Employee.objects.filter(team_id=team_id)
        
        if not employees.exists():
            return Response({"detail": "Bu takımın personeli yoktur."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = EmployeeSerializer(employees, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class AirplaneTypeViewSet(generics.ListAPIView):
    queryset = AirplaneType.objects.all()
    serializer_class = AirplaneTypeSerializer


class PartTypeViewSet(generics.ListAPIView):
    queryset = PartType.objects.all()
    serializer_class = PartTypeSerializer
#endregion

#region montaj
class CreateAirplaneAndAssignParts(APIView):
    airplane_type_id_param = openapi.Parameter(
        'airplane_type_id',
        openapi.IN_QUERY,
        type=openapi.TYPE_INTEGER,
        required=True,
    )

    @swagger_auto_schema(
        manual_parameters=[airplane_type_id_param],
        responses={
            201: AirplaneSerializer,
            400: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'detail': openapi.Schema(type=openapi.TYPE_STRING),
                },
                description="Hata detayları",
            ),
        }
    )
    def post(self, request, *args, **kwargs):
        user_info = get_user_info_from_token(request)

        # Eğer admin değilse ve takım ID'si eşleşmiyorsa yetkisiz hata döndür
        if user_info["is_admin"] is not True:
            if not user_info["team"].is_assembly_team:
                return HttpResponse('Unauthorized', status=401)
        # Gelen airplane_type_id'yi alır
        airplane_type_id = request.query_params.get('airplane_type_id')

        # AirplaneType modelinden gelen id ile AirplaneType objesini alır
        try:
            airplane_type = AirplaneType.objects.get(id=airplane_type_id)
        except AirplaneType.DoesNotExist:
            return Response({"detail": "Uçak tipi bulunamadı "}, status=status.HTTP_404_NOT_FOUND)

        # Airplane tipine ait olması gereken tüm PartType'ları alıyoruz
        required_part_types = PartType.objects.all()

        # Her bir gerekli PartType'ın bu airplane_type_id için mevcut olup olmadığını kontrol ediyoruz
        for part_type in required_part_types:
            if not Part.objects.filter(airplane_type=airplane_type, part_type__id=part_type.id, airplane=None).exists():
                return Response(
                 {"detail": f"Parça Eksik: {part_type.name}"},
                 status=status.HTTP_400_BAD_REQUEST
                 )

        # Airplane modelini oluşturur
        airplane = Airplane.objects.create(airplane_type=airplane_type)

        # Seçili Airplane tipine bağlı olan tüm parçaları alır (part_type a göre gruplama ve distinct yapılarak tek parçaya montaj sağlanacak)
        parts = Part.objects.filter(airplane_type=airplane_type, airplane=None).distinct('part_type')

        # Her part_type için yalnızca bir parça assign işlemi yapılır
        for part in parts:
            part.airplane = airplane
            part.save()

        # Oluşturulan Airplane'i döner
        serializer = AirplaneSerializer(airplane)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
#endregion