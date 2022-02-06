from datetime import datetime

from django.db.models import Q
from django.http import HttpResponse

from django.shortcuts import render, redirect
from .forms import SearchForm, WorkDDLForm, WorkLoadForm
import csv

from .models import Work
from io import StringIO
from django.contrib import messages
from django.core.management.color import no_style
from django.db import connection
from django.core.paginator import Paginator

sort_field = 'id'
search_field = ''

def strip_cols(full_col):
    result = [f.name for f in full_col]
    return result

def clear_works():
    # command = "update sqlite_sequence set seq=0 where sqlite_sequence.name='works_work'"
    # sequence_sql = connection.ops.sequence_reset_sql(no_style(), [works,])
    # with connection.cursor() as cursor:
    #     print('inside loops', sequence_sql)
    #     for sql in sequence_sql:
    #         print('sql', sql)
    #         cursor.execute(sql)
    Work.objects.all().delete()


def upload_works(request) -> HttpResponse:
    form = WorkLoadForm(request.POST or None, request.FILES or None)
    clear_works()
    # check whether it's valid:
    if form.is_valid():
        file = form.cleaned_data['file_name']
        csvf = StringIO(file.read().decode())
        reader = csv.reader(csvf, delimiter=',')
        cnt = 0
        for row in reader:
            cnt += 1
            if cnt == 1:
                continue

            work = Work(
                        item_id=row[1],
                        source=row[2],
                        notes=row[3],
                        location=row[4],
                        value=row[5] if row[5] else None,
                        inventory_date=datetime.strptime(row[6], '%Y-%m-%d') if row[6] else None,
                        title=row[7],
                        series=row[8],
                        date_year=row[9],
                        medium=' '.join(row[10].split()),
                        signature_and_writing=row[11],
                        condition=row[12],
                        category=row[13],
                        height=row[14] if row[14] else None,
                        width=row[15] if row[15] else None,
                        depth=row[16] if row[16] else None,
                        size_note=row[17],
                        file1=row[18],
                        file2=row[19],
                        file3=row[20],
                        file4=row[21],
                        file5=row[22],
                        )
            work.save()

    context = {'form': form, }
    return render(request, 'works/file_load.html', context)


def home_works(request) -> HttpResponse:
    global search_field
    # cols = strip_cols(Work._meta.get_fields())

    if request.method == 'POST':
        form = SearchForm(request.POST, initial={'search_text': search_field})
        if form.is_valid():
            search_field = form.cleaned_data['search_text']
    else:
        form = SearchForm(initial={'search_text': search_field})

    search = Q(item_id__contains=search_field) | Q(source__contains=search_field) | \
        Q(notes__contains=search_field) | Q(location__contains=search_field) | \
        Q(value__contains=search_field) | Q(inventory_date__contains=search_field) | \
        Q(title__contains=search_field) | \
        Q(series__contains=search_field) | Q(date_year__contains=search_field) | \
        Q(medium__contains=search_field) | Q(signature_and_writing__contains=search_field) | \
        Q(condition__contains=search_field) | Q(category__contains=search_field) | \
        Q(height__contains=search_field) | Q(width__contains=search_field) | \
        Q(depth__contains=search_field) | Q(size_note__contains=search_field) | \
        Q(condition__contains=search_field) | Q(category__contains=search_field)
    page_number = request.GET.get('page')
    work_list = Work.objects.all().filter(search).order_by(sort_field, "id")
    paginator = Paginator(work_list, 15)
    page_object = paginator.get_page(page_number)
    context = {
        'form': form,
        'works': page_object,
        'cols': strip_cols(Work._meta.get_fields())
    }
    return render(request, "works/home_works.html", context=context)


def clear_work(request):
    global search_field
    search_field = ''
    return redirect('home_works')


def create_work(request):
    if request.method == 'POST':
        form = WorkDDLForm(request.POST)
        if form.is_valid():
            form.save()
            # username = form.cleaned_data.get('username')
            messages.success(request, f'{form.instance} has been created')
            return redirect('home_works')
    else:
        form = WorkDDLForm()
    return render(request, "works/create_work.html", {'form': form})


def edit_work(request, id):
    work = Work.objects.get(id=id)
    if request.method == 'POST':
        form = WorkDDLForm(request.POST, instance=work)
        if form.is_valid():
            form.save()
            messages.success(request, f'{work} has been modified')
            return redirect('home_works')
    else:
        form = WorkDDLForm(instance=work)
    return render(request, "works/work_edit.html", {'form': form})


def delete_work(request, id):
    work = Work.objects.get(id=id)
    if request.method == 'POST':
        work.delete()
        messages.success(request, f'{work} has been deleted')
        return redirect('home_works')
    return render(request, "works/delete_work.html", {'work': work})


def view_work(request, id) -> HttpResponse:
    last = 1 if id == 1 else id-1
    next = id+1
    context = {
        'work': Work.objects.get(id=id),
        'last': last,
        'next': next
    }
    return render(request, 'works/view_work.html', context)


def download_works(request):
    now = datetime.now()  # current date and tim
    date_time = now.strftime("%m/%d/%Y")
    response = HttpResponse(
        content_type='text/csv',
        headers={'Content-Disposition': f'attachment; filename="inventory{date_time}.csv"'},
    )
    cols = [f.name for f in Work._meta.get_fields()]

    writer = csv.writer(response)
    writer.writerow(cols)
    works = Work.objects.all()
    for work in works:
        row = [getattr(work, f.name) for f in Work._meta.get_fields()]
        writer.writerow(row)

    return response


def work_sort(request, column):
    global sort_field
    sort_field = column
    return redirect('home_works')


def work_reverse_sort(request, column):
    global sort_field
    sort_field = f'-{column}'
    return redirect('home_works')
