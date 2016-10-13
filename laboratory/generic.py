'''
Created on 11/8/2016

@author: natalia
'''
from __future__ import unicode_literals

from django.views.generic.edit import CreateView, DeleteView
from laboratory.models import Shelf, Object, LaboratoryRoom, Furniture
from django.views.generic.list import ListView
from django.core.urlresolvers import reverse_lazy, reverse
from django.db.models.query import QuerySet
from django_ajax.mixin import AJAXMixin
from django import forms
import json
from django_ajax.decorators import ajax
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404


class ObjectDeleteFromShelf(DeleteView):
    model = Object
    success_url = reverse_lazy('laboratory:object-list')


@method_decorator(login_required, name='dispatch')
class ObjectList(ListView):
    model = Object


@method_decorator(login_required, name='dispatch')
class ObjectCreate(CreateView):
    model = Object
    fields = '__all__'
    success_url = "/"


@method_decorator(login_required, name='dispatch')
class LaboratoryRoomsList(ListView):
    model = LaboratoryRoom


@method_decorator(login_required, name='dispatch')
class LabroomCreate(CreateView):
    model = LaboratoryRoom
    fields = '__all__'
    success_url = reverse_lazy('laboratory:laboratoryroom_create')

    def get_context_data(self, **kwargs):
        context = CreateView.get_context_data(self, **kwargs)

        context['object_list'] = self.model.objects.all()
        return context


class LaboratoryRoomDelete(DeleteView):
    model = LaboratoryRoom
    success_url = reverse_lazy('laboratory:laboratoryroom_create')


@method_decorator(login_required, name='dispatch')
class LabRoomList(ListView):
    model = LaboratoryRoom


class ShelfForm(forms.ModelForm):
    col = forms.IntegerField(widget=forms.HiddenInput)
    row = forms.IntegerField(widget=forms.HiddenInput)

    class Meta:
        model = Shelf
        fields = ['name', 'type', 'furniture']
        widgets = {
            'furniture': forms.HiddenInput()
        }


@method_decorator(login_required, name='dispatch')
class ShelfCreate(AJAXMixin, CreateView):
    model = Shelf
    success_url = "/"
    form_class = ShelfForm

    def get_form_kwargs(self):
        kwargs = CreateView.get_form_kwargs(self)
        kwargs['initial']['furniture'] = self.request.GET.get('furniture')
        kwargs['initial']['col'] = self.request.GET.get('col')
        kwargs['initial']['row'] = self.request.GET.get('row')
        return kwargs

    def form_valid(self, form):
        self.object = form.save(commit=False)
        furniture = form.cleaned_data['furniture']
        col = form.cleaned_data['col']
        row = form.cleaned_data['row']
        if furniture is None or col is None or row is None:
            return self.form_invalid(form)
        try:
            col, row = int(col), int(row)
        except:
            return self.form_invalid(form)

        self.object.furniture = furniture
        self.object.save()
        dataconfig = self.set_dataconfig(furniture,
                                         col, row,
                                         self.object.pk)

        dev = render_to_string(
            "laboratory/shelf_rows.html",
            {"crow": row,
             "ccol": col,
             "col": Shelf.objects.filter(
                 pk__in=dataconfig[row][col] + [self.object.pk])})

        return {
            'inner-fragments': {
                '#row_%d_col_%d' % (row, col): dev,
                "#modalclose": "<script>closeModal();</script>"
            },
        }

    def set_dataconfig(self, furniture, col, row, value):
        return json.loads(furniture.dataconfig)


@login_required
@ajax
def ShelfDelete(request, pk, row, col):
    row, col = int(row), int(col)
    shelf = get_object_or_404(Shelf, pk=pk)
    shelf.delete()
    url = reverse('laboratory:shelf_delete', args=(pk, row, col))
    #url = url.replace("/", "\\/")
    print(url)
    return {'inner-fragments': {
        "#modalclose": """<script>$("a[href$='%s']").closest('li').remove();</script>""" % (url)
    }, }


@method_decorator(login_required, name='dispatch')
class ShelfListView(ListView):
    model = Shelf
