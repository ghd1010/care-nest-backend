from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import (
    SignUpView,
    ChildListCreateView, 
    ChildDetailView,
    ChildAchievementsListCreateView,
    ChildAchievementsByChildView,
    ChildAchievementsDetailView,
    AttendanceListView,
    AttendanceCreateView,
    SectionListView,
    AttendanceBySectionView,
    ChildrenBySectionView,
    AttendanceDetailView,
    AchievementsBySectionView,
    this_user_details,
    all_parents
    )

urlpatterns = [
    path('children/', ChildListCreateView.as_view(), name='child-list-create'),
    path('children/<int:pk>/', ChildDetailView.as_view(), name='child-detail'),
    path('children/<int:pk>/achievements/', ChildAchievementsByChildView.as_view(), name='get-achivements-by-child-id-delete-edit'),
    path('achievements/', ChildAchievementsListCreateView.as_view(), name='achievements-list-create'),
    path('achievements/<int:pk>/', ChildAchievementsDetailView.as_view(), name='achivements-detail'),
    path('attendance/<int:pk>/edit/', AttendanceDetailView.as_view(), name='attendance-edit'),
    path('attendance/', AttendanceListView.as_view(), name='attendance-list'),
    path('sections/', SectionListView.as_view(), name='sections-list'),
    path('sections/<int:section_id>/attendance/', AttendanceBySectionView.as_view(), name='attendance-by-section'),
    path('sections/<int:section_id>/attendance/add/', AttendanceCreateView.as_view(), name='attendance-create'),
    path('sections/<int:section_id>/children/', ChildrenBySectionView.as_view(), name='children-by-section'),
    path('sections/<int:section_id>/achievements/', AchievementsBySectionView.as_view(), name='achievement-by-section'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('user_details/', this_user_details, name='user-details'),
    path('all_parents/', all_parents, name='all-parents'),
]