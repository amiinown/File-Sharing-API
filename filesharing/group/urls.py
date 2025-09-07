from django.urls import path
from drf_spectacular.utils import extend_schema
from .views import (
    GroupDeleteView, GroupListMembersView, GroupAddMembersView,
    GroupDeleteMembersView, GroupListAddView, GroupChangeMembersPermissionView
    )

app_name = 'groups'
urlpatterns = [
    path('', GroupListAddView.as_view(), name='list-add-groups'),
    path('<int:group_id>/', GroupDeleteView.as_view(), name='remove-group'),

    path('<int:group_id>/members/', GroupListMembersView.as_view(), name='list-members-group'),
    path('<int:group_id>/members/add/', GroupAddMembersView.as_view(), name='add-members-group'),
    path('<int:group_id>/members/remove/', GroupDeleteMembersView.as_view(), name='remove-members-group'),
    path('<int:group_id>/members/change/', GroupChangeMembersPermissionView.as_view(), name='modify-members-group'),
]