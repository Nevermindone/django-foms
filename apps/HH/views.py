from django.shortcuts import render, get_object_or_404, redirect

from .forms import *
from .models import *
from django.template import Context
from apps.HH.services.data_lists_service import DataListsCreate
from apps.HH.serializers import *
from .services.download_contact import download_zip


def skills_create_view(request):
    form = QueryForm(request.POST or None)
    form_search = QuerySearchForm(request.POST or None)

    if form.is_valid() and form_search.is_valid():
        qform = form.save(commit=False)
        qform.usr=request.user
        qform.save()
        fform_search = form_search.save(commit=False)
        fform_search.qform = qform
        fform_search.save()
    else:
        print(form.errors)
        print(form_search.errors)
    context = {
        'form': form,
        'form_search': form_search,
    }

    return render(request, 'skills.html', context)


def table_create_view(request):
    table_list = Queries.objects.all().select_related('children').filter(delete=1,
                                                                         usr=request.user)
    swap_dict = {1: 'Обработка запроса',
                 3: 'Резюме предоставлены'}
    for i in table_list:
        i.status = swap_dict[i.status]

    return render(request, 'tables.html', {'table_list': table_list,
                                           'swap_dict': swap_dict})

  
def skills_update_view(request, id):
    data_queries = get_object_or_404(Queries, id=id)
    data_query_search = get_object_or_404(QuerySearch, id=id)
    form = QueryForm(instance=data_queries)
    form_search = QuerySearchForm(instance=data_query_search)

    if request.method == "POST":
        form = QueryForm(request.POST, instance=data_queries)
        form_search = QuerySearchForm(request.POST, instance=data_query_search)

        if form.is_valid() and form_search.is_valid():
            qform = form.save()
            fform_search = form_search.save(commit=False)
            fform_search.qform = qform
            fform_search.save()
        else:
            print(form.errors)
            print(form_search.errors)
    context = {
        "form": form,
        'form_search': form_search

    }
    return render(request, 'edit_skills.html', context)
  

def skills_delete_view(request, id):
    obj = get_object_or_404(Queries, id=id)
    obj.delete = 0
    obj.status = 3
    obj.save(update_fields=['delete', 'status'])

    return render(request, "delete_skills.html")


def request_data(request, id):
    if request.method == 'POST':
        serializer = CheckboxResponse(data=request.POST)
        if serializer.is_valid():
            print(serializer.validated_data)
            idq_list = serializer.validated_data['choosed']
            if serializer.validated_data['button'][0] == 'Download':
                return download_zip(idq_list)
            else:
                Urls.objects.filter(pk__in=idq_list).update(isneedcontact=1)
                urls = Urls.objects.filter(idq=id, old=0).all()
                urls = DataListsCreate(urls).query_to_lists()
                return render(request, 'request_data.html', {'urls': urls})

    urls = Urls.objects.filter(idq=id, old=0).all()
    urls = DataListsCreate(urls).query_to_lists()
    return render(request, 'request_data.html', {'urls': urls})
