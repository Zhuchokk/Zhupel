from django import template
register = template.Library()


@register.filter(name="liked")
def liked(obj):
    obj.like_count += 1
    obj.save()
    print("liked", obj.like_count)