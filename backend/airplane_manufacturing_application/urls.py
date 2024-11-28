from django.urls import include, path
from rest_framework.routers import DefaultRouter
from airplane_manufacturing_application import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = DefaultRouter()
router.register(r'airplane', views.AirplaneViewSet)
# router.register(r'parts', views.PartViewSet)
# router.register(r'teams', views.TeamViewSet)
router.register(r'employee', views.EmployeeViewSet)

urlpatterns = [
    # genel api lar
    path('', include(router.urls)),
    path('parts/', views.PartAPIView.as_view(), name='part-create'),
    path('parts-by-id/<int:id>/', views.PartAPIView.as_view(), name='part-delete'),
    # tipler
    path('part-types/', views.PartTypeViewSet.as_view(), name='part-type-list'), 
    path('airplane-types/', views.AirplaneTypeViewSet.as_view(), name='airplane-types-list'),
    # datatables api ları
    path('airplane-list/', views.AirplaneListView.as_view(), name='airplane-list'), 
    path('teams-list/', views.TeamListView.as_view(), name='teams-list'), 
    path('employee-list/', views.EmployeeListView.as_view(), name='employee-list'), 
    # by-id list
    path('employees/<int:team_id>/', views.EmployeeListViewByTeamId.as_view(), name='employee-list-by-team-id'),
    path('parts-by-team-id/', views.PartListViewByTeamId.as_view(), name='airplanes-by-team'),
    path('parts-list-by-airplane-id/<int:airplane_id>/', views.PartListViewByAirplaneId.as_view(), name='part-list-by-airplane-id'),
    path('parts-list-by-airplane-type-id/<int:airplane_type_id>/', views.PartListViewByUavTypeId.as_view(), name='part-list-by-airplane-type-id'),
    path('parts-list-by-airplane-type-id-count/<int:airplane_type_id>/', views.PartListViewByUavTypeIdPartTypeCounts.as_view(), name='part-list-by-airplane-type-id'),

    # montaj
    path('create-airplane/', views.CreateAirplaneAndAssignParts.as_view(), name='create_airplane'),

    #token
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('custom-token/', views.CustomTokenObtainPairView.as_view(), name='custom_token_obtain_pair'),
]
