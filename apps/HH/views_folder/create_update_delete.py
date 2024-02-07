from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import TemplateView
from apps.HH.forms import *
from apps.HH.models import *
from django.shortcuts import render, get_object_or_404
from apps.HH.services.api_hh_helper import suggest_func, suggest_func_reverse


class AddSkillsView(TemplateView):

    template_name = 'skills.html'

    def get(self, request):
        form = QueryForm(None)
        second_form = QuerySearchForm(None)
        context = {'form': form,
                   'second_form': second_form}
        return render(request, self.template_name, context)

    def post(self, request):

        form = QueryForm(request.POST)
        second_form = QuerySearchForm(request.POST)
        form.data._mutable = True
        form.data['area'] = suggest_func(form.data['area'])
        form.data['citizenship'] = suggest_func(form.data['citizenship'])
        form.data['work_ticket'] = suggest_func(form.data['work_ticket'])
        form.data._mutable = False
        if form.is_valid() and second_form.is_valid():
            qform = form.save(commit=False)
            qform.usr = request.user
            qform.save()
            fform_search = second_form.save(commit=False)
            fform_search.qform = qform
            fform_search.save()

        context = {
            'form': form,
            'second_form': second_form
        }

        return render(request, self.template_name, context)


class UpdateSkillsView(TemplateView):

    template_name = 'edit_skills.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        data_query = get_object_or_404(Queries, pk=self.kwargs['pk'])
        data_query_search = get_object_or_404(QuerySearch, pk=self.kwargs['pk'])
        data_query_search.area = suggest_func_reverse(data_query_search.area)
        data_query_search.citizenship = suggest_func_reverse(data_query_search.citizenship)
        data_query_search.work_ticket = suggest_func_reverse(data_query_search.work_ticket)
        context['data_query'] = data_query
        context['data_query_search'] = data_query_search
        context['form'] = QueryForm(instance=data_query)
        context['second_form'] = QuerySearchForm(instance=data_query_search)

        return context

    def post(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        data_query = get_object_or_404(Queries, pk=pk)
        form = QueryForm(request.POST, instance=data_query)
        form.data._mutable = True
        form.data['area'] = suggest_func(form.data['area'])
        form.data['citizenship'] = suggest_func(form.data['citizenship'])
        form.data['work_ticket'] = suggest_func(form.data['work_ticket'])
        form.data._mutable = False
        data_query_search = get_object_or_404(QuerySearch, pk=pk)
        second_form = QuerySearchForm(request.POST, instance=data_query_search)
        if form.is_valid() and second_form.is_valid():
            form.save()
            second_form.save()
            QuerySearch.objects.filter(pk=pk).update(searchurl=None)
            urls = Urls.objects.filter(idq=pk).update(old=True)
            print(urls)
        data_query.status = 1
        data_query.save(update_fields=['status'])

        return HttpResponseRedirect(reverse('update', kwargs={'pk': self.kwargs['pk']}))


class DeleteSkillsView(TemplateView):
    template_name = "delete_skills.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        data = get_object_or_404(Queries, pk=self.kwargs['pk'])
        data.delete = 0
        data.status = 3
        data.save(update_fields=['delete', 'status'])
        return context
