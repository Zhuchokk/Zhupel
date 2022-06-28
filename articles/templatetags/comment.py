from django import template
register = template.Library()


@register.filter
def comment(obj):
    obj.comment_count += 1
    obj.save()
    print("comment", obj.comment_count)