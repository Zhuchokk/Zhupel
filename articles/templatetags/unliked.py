from django import template
register = template.Library()


@register.filter
def unliked(obj):
    obj.like_count -= 1
    obj.save()
    print("unliked", obj.like_count)