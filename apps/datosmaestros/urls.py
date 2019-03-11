# Django
from django.urls import path

# App Views
from .views import (
    CategoriaListView,
    CategoriaCreateView,
    CategoriaUpdateView,
    CategoriaDeleteView,
    DatoListView,
    DatoCreateView,
    DatoUpdateView,
    DatoDeleteView
)

app_name = 'datosmaestros'

urlpatterns = [
    path(
        'categorias/',
        CategoriaListView.as_view(),
        name = 'listar_categorias'
    ),
    path(
        'categorias/crear/',
        CategoriaCreateView.as_view(),
        name = 'crear_categoria'
    ),
    path(
        'categorias/editar/<int:id_categoria>',
        CategoriaUpdateView.as_view(),
        name = 'editar_categoria'
    ),
    path(
        'categorias/eliminar/',
        CategoriaDeleteView.as_view(),
        name = 'eliminar_categoria'
    ),
    path(
        'categorias/<int:id_categoria>/datos/',
        DatoListView.as_view(),
        name = 'listar_datos'
    ),
    path(
        'categorias/<int:id_categoria>/datos/crear/',
        DatoCreateView.as_view(),
        name = 'crear_dato'
    ),
    path(
        'categorias/<int:id_categoria>/datos/editar/<int:id_dato>',
        DatoUpdateView.as_view(),
        name = 'editar_dato'
    ),
    path(
        'categorias/<int:id_categoria>/datos/eliminar/',
        DatoDeleteView.as_view(),
        name = 'eliminar_dato'
    ),
]
