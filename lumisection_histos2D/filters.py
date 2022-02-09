import django_filters
from django import forms
from django.db import models
from lumisection_histos2D.models import LumisectionHisto2D

class InFilter(django_filters.filters.BaseInFilter, django_filters.filters.CharFilter):
    pass

class LumisectionHistos2DFilter(django_filters.FilterSet):

    title = django_filters.filters.AllValuesMultipleFilter(
        widget=forms.SelectMultiple(attrs={
            'class': 'form-control',
            'size': '10',
        })
    )

    lumisection__ls_number__in = InFilter(field_name='lumisection__ls_number', lookup_expr='in')
    lumisection__run__run_number__in = InFilter(field_name='lumisection__run__run_number', lookup_expr='in')

    class Meta:
        model = LumisectionHisto2D
        fields = {
            'lumisection__run__run_number': ['gte', 'lte',],
            'lumisection__ls_number': ['gte', 'lte',],
            'entries': ['gte', 'lte',],
        }
