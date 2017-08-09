from collections import namedtuple

from django import template
from django.core.urlresolvers import reverse

register = template.Library()

_NavItem = namedtuple('NavItem', ['url', 'title', 'active'])


@register.inclusion_tag('stats/partials/stats-navbar.html', takes_context=True)
def stats_navbar(context):
    return {
        'navbar': [
            _NavItem(
                url=reverse(name),
                title=title,
                active=context['request'].resolver_match.url_name == name,
            )
            for name, title in
            [
                ('stats', 'Summary'),
                ('stats_printing', 'Printing'),
                # TODO: probably a better place to put this
                ('pages_printed', 'Lifetime Pages Printed'),
                ('stats_accounts', 'Accounts'),
                ('stats_mirrors', 'Mirrors'),
            ]
        ],
    }


@register.filter
def humanize_size(value):
    # adapted from jvperrin/upload-to-box
    for unit in ['', 'KB', 'MB', 'GB', 'TB', 'PB']:
        if value < 1024.0:
            return '{:3.2f} {}'.format(value, unit)
        value /= 1024.0
