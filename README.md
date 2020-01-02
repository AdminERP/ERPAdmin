# ERPAdmin
..Sistema de planificación de recursos empresariales


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


Ademas de **psql (PostgreSQL) 9.5.14**

[Descargar settings.py](https://drive.google.com/open?id=1jwOzGao3aqZjwQTXcE27pduBF1OxbywJ)

**Por favor no subir la carpeta del ambiente al repositorio**



## Organización de carpetas

**apps**: Donde deberian ir las apps relacionadas con los módulos de cada grupo.

**static**: Archivos estaticos. js/css/html

**templates**: Se encuentra el archivo base.html

**templates en las apps**:
```
.
├── apps
│   ├── mi_app
│   │   ├── templates
│   │   │   └── mi_app
│   │   │       ├── editar.html
│   │   │       ├── crear.html
│   │   │       ├── eliminar.html
│   │   │       ├── consultar.html
```


## Módulos del proyecto

 1. Compras
 2. Datos maestros, perfiles, roles e Inventario
 3. Cuentas por Pagar
 4. Cuentas por Cobrar
 5. Gestión de cuentas contables
 6. Recursos humanos
 7. Ordenes de servicio

## Construido con

 - [Django](https://github.com/django/django)
 - [MaterialAdminLTE](https://github.com/DucThanhNguyen/MaterialAdminLTE)
 - [Bootstrap](https://github.com/twbs/bootstrap)
