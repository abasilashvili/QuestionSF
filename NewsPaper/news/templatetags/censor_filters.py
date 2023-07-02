from django import template
import re

register = template.Library()


def censor(value, bad_words=None):
    if not bad_words:
        bad_words = ['лох', 'пох']

    def replace(match):
        word = match.group(0)
        return '*' * len(word)

    for bad_word in bad_words:
        regex = re.compile(r'\b' + bad_word + r'\b', re.IGNORECASE)
        value = regex.sub(replace, value)

    return value


register.filter('censor', censor)