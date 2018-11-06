from django import template
register = template.Library()


@register.filter(name='index')
def indice(lista, indice):
    return lista[int(indice)]