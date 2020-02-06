from django import template
from django.db.models import Count, Sum, F, CharField

register = template.Library()


@register.simple_tag(takes_context=True)
def relative_url(value, field_name, urlencode=None):
    url = '?{}={}'.format(field_name, value)
    if urlencode:
        querystring = urlencode.split('&')
        filtered_querystring = filter(lambda p: p.split('=')[0] != field_name, querystring)
        encoded_querystring = '&'.join(filtered_querystring)
        url = '{}&{}'.format(url, encoded_querystring)
    return url

@register.filter
def in_school(beneficiaries, school):
    return beneficiaries.filter(school_name=school)

@register.filter
def get_total_amount_to_beneficiaries(beneficiaries, school):
	amount = beneficiaries.filter(school_name=school).aggregate(total=Sum('school_type__amount_allocated'))
	return amount['total']

@register.filter
def get_cheque_number(beneficiaries, school):
	cheque_number = beneficiaries.filter(school_name=school).values_list('cheque_number__cheque_number', flat=True).distinct()
	return cheque_number[0]