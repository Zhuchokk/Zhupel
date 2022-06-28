from django import template
register = template.Library()


@register.filter
def uncomment(obj):
    obj.comment_count -= 1
    obj.save()
    print("uncomment", obj.comment_count)