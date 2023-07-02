from django import template


register = template.Library()


@register.filter()
def currency(value):
   """
   value: значение, к которому нужно применить фильтр
   """
   return f'{value} Р'