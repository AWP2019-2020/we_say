from django import template

from app.models import Vote

register = template.Library()

@register.filter(name='get_vote_value')
def get_vote_value(user, poll):
    return Vote.objects.filter(user=user, poll = poll).first().option