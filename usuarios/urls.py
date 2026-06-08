from django.urls import path

from . import views

app_name = "usuarios"

urlpatterns = [
    path("", views.UsuarioListView.as_view(), name="lista"),
    path("crear/modal/", views.UsuarioCreateView.as_view(), name="crear_modal"),
    path("<int:pk>/editar/modal/", views.UsuarioUpdateView.as_view(), name="editar_modal"),
    path("<int:pk>/eliminar/", views.usuario_eliminar, name="eliminar"),
    path("<int:pk>/grupos/", views.usuario_grupos, name="grupos_modal"),
    path("datos/", views.usuarios_json, name="datos_json"),
]
