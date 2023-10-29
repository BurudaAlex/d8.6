from django import template

register = template.Library()

censored_word = ["редиска"]

@register.filter()
def censor(value):
    for word in censored_word:
        if word.lower() in value.lower():
            value = value.replace(word[2:], '*' * len(word))
    return value

@register.simple_tag(takes_context=True)
def url_replace(context, **kwargs):
   d = context['request'].GET.copy()
   for k, v in kwargs.items():
       d[k] = v
   return d.urlencode()