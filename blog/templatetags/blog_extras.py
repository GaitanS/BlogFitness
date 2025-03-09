from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """
    Template filter to get an item from a dictionary using a variable as the key.
    Usage: {{ dictionary|get_item:key }}
    """
    return dictionary.get(key)

@register.filter(name='truncate_title')
def truncate_title(value, length):
    """
    Truncates a string to a specified length, adding an ellipsis if it exceeds the length.
    Usage: {{ title|truncate_title:50 }}
    """
    length = int(length)
    if len(value) > length:
        return value[:length] + "..."
    return value
