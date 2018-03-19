from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^signin$', views.signin, name="signin"),
    url(r'^logout$', views.logout, name="logout"),
    url(r'^register$', views.register, name="register"),
    url(r'^login$', views.login, name="login"),
    url(r'^dashboard$', views.dashboard, name="dashboard"),
    url(r'^dashboard/admin$', views.adminDashboard, name="admin_dashboard"),
    url(r'^users/new$', views.new, name="new"),
    url(r'^users/edit$', views.editSelf, name="edit_self"),
    url(r'^users/edit/(?P<id>\d+)$', views.editUser, name="edit_user"),
    url(r'^users/show/(?P<id>\d+)$', views.show, name="show"),
    url(r'^users/update/(?P<id>\d+)$', views.updateInfo, name="update_info"),
    url(r'^users/admin_update/(?P<id>\d+)$', views.adminUpdateInfo, name="admin_update_info"),
    url(r'^users/update_password/(?P<id>\d+)$', views.updatePassword, name="update_password"),
    url(r'^users/update_description/(?P<id>\d+)$', views.updateDescription, name="update_description"),
    url(r'^users/remove/(?P<id>\d+)$', views.remove, name="remove"),
    url(r'^users/add_message/(?P<id>\d+)$', views.addMessage, name="add_message"),
    url(r'^users/add_comment/(?P<msg_id>\d+)/(?P<usr_id>\d+)$', views.addComment, name="add_comment"),
    url(r'^create/(?P<login>\w+)?$', views.createUser, name="create")
]