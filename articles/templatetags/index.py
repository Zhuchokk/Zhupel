from django import template
register = template.Library()


@register.filter
def index(li,i):
    try:
        return li[i]
    except:
        return "no"
