# ERPAdmin
Sistema de planificación de recursos empresariales


[![Django Version](https://img.shields.io/badge/django-2.0.1-yellow.svg)](https://docs.djangoproject.com/en/2.1/releases/2.0.1/) [![python version](https://img.shields.io/badge/python-3.5.2-blue.svg)](https://www.python.org/downloads/release/python-350/)

## Empezando
Se deben instalar los paquetes, dependencias y demás.

Se recomienda python >= 3.5
 - Verificar que tengan python 3.5.2
	 - `python3.5 --version`
 - [Instalar](https://www.python.org/download/releases/3.5.2/) python 3.5.2 (en caso de no tenerlo)
 - Crear un ambiente virtual
	 - `virtualenv nombre_ambiente --python python3.x`
 - Instalar Django 2.01

O instalar el archivo requirements.txt

    pip install -r requirements.txt


## Organización de carpetas

**apps**: Donde deberian ir las apps relacionadas con los módulos de cada grupo.

**static**: Archivos estaticos. js/css/html

**templates**: Se encuentra el archivo base.html

## Módulos del proyecto

 1. Compras
 2. Datos maestros, perfles, roles e Inventario
 3. Cuntas por Pagar
 4. Cuentas por Cobrar
 5. Gestión de cuentas contables
 6. Recursos humanos

## Construido con

 - [Django](https://github.com/django/django)
 - [MaterialAdminLTE](https://github.com/DucThanhNguyen/MaterialAdminLTE)
 - [Bootstrap](https://github.com/twbs/bootstrap)
