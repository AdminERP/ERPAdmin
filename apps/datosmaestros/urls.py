# Django
from django.urls import path

# App Views
from .views import (
    CategoriaListView,
    CategoriaCreateView,
    CategoriaUpdateView,
    CategoriaDeleteView
)

app_name = 'datosmaestros'

urlpatterns = [
    path(
        'categorias/',
        CategoriaListView.as_view(),
        name = 'listar_categoria'
    ),
    path(
        'categorias/crear/',
        CategoriaCreateView.as_view(),
        name = 'crear_categoria'
    ),
    path(
        'categorias/editar/<int:pk>',
        CategoriaUpdateView.as_view(),
        name = 'editar_categoria'
    ),
    path(
        'categorias/eliminar/',
        CategoriaDeleteView.as_view(),
        name = 'eliminar_categoria'
    ),
]
