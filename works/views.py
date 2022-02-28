from datetime import datetime

from django.db.models import Q, F
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
import sqlite3
from django.urls import reverse
from django.contrib.auth.decorators import login_required


def strip_cols(full_col):
    result = [f.name for f in full_col]
    return result


def clear_works():
    Work.objects.all().delete()


def check_max(current_max, id):
    pieces = id.split('.')
    try:
        if int(pieces[2]) > current_max:
            current_max = int(pieces[2])
        return current_max
    except ValueError as e:
        return current_max


def set_seq(val):
    connection_db = sqlite3.connect('db.sqlite3')
    table_connection_db = connection_db.cursor()
    table_connection_db.execute(f"UPDATE sqlite_sequence set seq ={val} WHERE name ='works_work'")
    connection_db.commit()
    connection_db.close()
    print('set id', f"UPDATE sqlite_sequence set seq ={val} WHERE name ='works_work'")


@login_required
def upload_works(request) -> HttpResponse:
    form = WorkLoadForm(request.POST or None, request.FILES or None)
    clear_works()
    # check whether it's valid:
    max_id = 0
    set_seq(0)
    if form.is_valid():
        file = form.cleaned_data['file_name']
        csvf = StringIO(file.read().decode())
        reader = csv.reader(csvf, delimiter=',')
        cnt = 0
        for row in reader:
            cnt += 1
            if cnt == 1:
                continue

            max_id = check_max(max_id, row[1])

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
    set_seq(max_id+1)
    return render(request, 'works/file_load.html', context)


@login_required
def home_works(request) -> HttpResponse:
    cart = request.session.get('cart', {})
    search_field = request.session.get("work_search", "")
    # cols = strip_cols(Work._meta.get_fields())

    if request.method == 'POST':
        form = SearchForm(request.POST, initial={'search_text': search_field})
        if form.is_valid():
            search_field = form.cleaned_data['search_text']
            print ("new search", search_field)
            request.session["work_search"] = search_field
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
    sort_field = request.session.get('work_sort', 'id')
    if sort_field.startswith('-'):
        work_list = Work.objects.all().filter(search).order_by(F(sort_field[1:]).asc(nulls_last=True), F("id"))
    else:
        work_list = Work.objects.all().filter(search).order_by(F(sort_field).desc(nulls_last=True), F("id"))
    paginator = Paginator(work_list, 15)
    page_object = paginator.get_page(page_number)
    work_ids = ",".join([str(work.id) for work in page_object])
    context = {
        'form': form,
        'works': page_object,
        'cols': strip_cols(Work._meta.get_fields()),
        'ids': work_ids,
    }
    return render(request, "works/home_works.html", context=context)


@login_required
def clear_work(request):
    request.session["work_search"] = ''
    print('clear work')
    print('request.session after clear', str(request.session['work_search']))
    return redirect('home_works')


@login_required
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
    context = {'form': form,
               'home': reverse('home_works')}
    return render(request, "create_work.html", context)


@login_required
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
        work = Work.objects.get(id=id)

    context = {'form': form,
               'work': work,
               'home': reverse('home_works')}
    return render(request, "works/work_edit.html", context)


@login_required
def delete_work(request, id):
    work = Work.objects.get(id=id)
    if request.method == 'POST':
        work.delete()
        messages.success(request, f'{work} has been deleted')
        return redirect('home_works')
    return render(request, "works/delete_work.html", {'work': work})


@login_required
def view_work(request, id, ids) -> HttpResponse:
    id_nums = ids.split(',')
    offset = id_nums.index(str(id))
    if offset < 0:
        raise ValueError(f"Can't find {id}")
    last = 0 if offset == 0 else int(id_nums[offset -1])
    next = 0 if offset >= len(id_nums) - 1 else int(id_nums[offset + 1])
    print('id', id, 'offset', offset, 'last', last, 'next', next, 'ids', id_nums)
    context = {
        'work': Work.objects.get(id=id),
        'last': last,
        'next': next,
        'ids': ids
    }
    return render(request, 'works/view_work.html', context)


@login_required
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


@login_required
def work_sort(request, column):
    request.session['work_sort'] = column
    return redirect('home_works')


@login_required
def work_reverse_sort(request, column):
    request.session['work_sort'] = f'-{column}'
    return redirect('home_works')


@login_required
def work_test(request):
    return render(request, 'works/test.html')