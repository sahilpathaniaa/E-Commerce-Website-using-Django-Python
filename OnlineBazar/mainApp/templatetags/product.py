from django import template
register = template.Library()


@register.filter("checkColor")
def checkColor(color, item):
    flag = False
    for i in color.split(","):
        if(i==item):
            flag=True
            break
    return flag

@register.filter("checkSize")
def checkSize(size, item):
    flag = False
    for i in size.split(","):
        if(i==item):
            flag=True
            break
    return flag