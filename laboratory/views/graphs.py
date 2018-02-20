'''
Created on 17 feb. 2018

@author: luisza
'''

from random import shuffle
from chartjs.views.lines import BaseLineChartView
from laboratory.models import Object, Laboratory
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from laboratory.decorators import check_lab_permissions 
from django.contrib.auth.decorators import login_required
from chartjs.colors import next_color, COLORS
from django.utils.translation import ugettext as _


@method_decorator(check_lab_permissions, name='dispatch')
@method_decorator(login_required, name='dispatch')
class LaboratoryIMDGChart(BaseLineChartView):
    def get(self, request, *args, **kwargs):
        self.lab = get_object_or_404(Laboratory, pk=kwargs['lab_pk'])
        self.lab_pk=kwargs['lab_pk']
        del  kwargs['lab_pk']
        self.filter_precursor = False
        filter_precursor = request.GET.get('precursor', "")
        self.filter_precursor = filter_precursor != ""
        return super(LaboratoryIMDGChart, self).get(request, *args, **kwargs)
    
    def get_labels(self):
        """Return 7 labels for the x-axis."""
        return list(map(lambda x: x[1],  Object.IDMG_CHOICES))

    def get_providers(self):
        """Return names of datasets."""
        return [_("Objects based on IDMG code")]

    def get_data(self):
        """Return 3 datasets to plot."""
        data=[]
        for id, name in Object.IDMG_CHOICES:
            args={
                "shelfobject__shelf__furniture__labroom__laboratory__pk": self.lab_pk,
                "imdg_code": id
            }
            if self.filter_precursor:
                args["is_precursor"]=True
            
            data.append(
                Object.objects.filter(**args).count()
                        )
        return [data]
    
    def get_colors(self):
        """Return a new shuffle list of color so we change the color
        each time."""
        colors = COLORS[:]
        shuffle(colors)
        return next_color(colors)
    
@method_decorator(check_lab_permissions, name='dispatch')
@method_decorator(login_required, name='dispatch')
class LaboratoryTypeChart(BaseLineChartView):
    def get(self, request, *args, **kwargs):
        self.lab = get_object_or_404(Laboratory, pk=kwargs['lab_pk'])
        self.lab_pk=kwargs['lab_pk']
        del  kwargs['lab_pk']

        return super(LaboratoryTypeChart, self).get(request, *args, **kwargs)
    
    def get_labels(self):
        """Return 7 labels for the x-axis."""
        return list(map(lambda x: x[1],  Object.TYPE_CHOICES))

    def get_providers(self):
        """Return names of datasets."""
        return [_("Type of objects")]

    def get_data(self):
        """Return 3 datasets to plot."""
        data=[]
        for id, name in Object.TYPE_CHOICES:
            data.append(
                Object.objects.filter(
                    shelfobject__shelf__furniture__labroom__laboratory__pk=self.lab_pk,
                    type=id
                              ).count()
                        )
        return [data]

    def get_colors(self):
        """Return a new shuffle list of color so we change the color
        each time."""
        colors = COLORS[:]
        shuffle(colors)
        return next_color(colors)
    
    
@method_decorator(check_lab_permissions, name='dispatch')
@method_decorator(login_required, name='dispatch')
class LaboratoryIDMGAmountsChart(BaseLineChartView):
    def get(self, request, *args, **kwargs):
        self.lab = get_object_or_404(Laboratory, pk=kwargs['lab_pk'])
        self.lab_pk=kwargs['lab_pk']
        del  kwargs['lab_pk']
        self.filter_precursor = False
        filter_precursor = request.GET.get('precursor', "")
        self.filter_precursor = filter_precursor != ""
        return super(LaboratoryIMDGChart, self).get(request, *args, **kwargs)
    
    def get_labels(self):
        """Return 7 labels for the x-axis."""
        return list(map(lambda x: x[1],  Object.IDMG_CHOICES))

    def get_providers(self):
        """Return names of datasets."""
        return [_("Objects based on IDMG code")]

    def get_data(self):
        """Return 3 datasets to plot."""
        data=[]
        for id, name in Object.IDMG_CHOICES:
            args={
                "shelfobject__shelf__furniture__labroom__laboratory__pk": self.lab_pk,
                "imdg_code": id
            }
            if self.filter_precursor:
                args["is_precursor"]=True
            
            data.append(
                Object.objects.filter(**args).count()
                        )
        return [data]
    
    def get_colors(self):
        """Return a new shuffle list of color so we change the color
        each time."""
        colors = COLORS[:]
        shuffle(colors)
        return next_color(colors)