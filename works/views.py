from datetime import datetime

from django.db.models import Q
from django.http import HttpResponse

from django.shortcuts import render, redirect
from .forms import WorkLoadForm, SearchForm, WorkForm, WorkDDLForm
import csv

from .models import OldWork, Work
from io import StringIO
from django.contrib import messages

sort_field = 'id'
search_field = ''

def strip_cols(full_col):
    result = [f.name for f in full_col]
    return result

def decode_image(name:str) -> str:
    name = name.strip()
    if not name or name=='':
        return None
    if not name.startswith('remote:'):
        print('Error', name)

    st = name.find(':')
    end = name.find('JPG')
    if end == -1:
        end = name.find('jpg')
    print('y', st, end, 'x', name[st+1: end+3])
    return name[st+1:end+3]


def upload_old_works(request) -> HttpResponse:
    form = WorkLoadForm(request.POST or None, request.FILES or None)
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
            old_work = OldWork(index=row[0],
                               item_id=row[1],
                               source=row[2],
                               notes=row[3],
                               location=row[4],
                               value=row[5] if row[5] else None,
                               inventory_date=datetime.strptime(row[6], '%m/%d/%Y') if row[6] else None,
                               title=row[7],
                               series=row[8],
                               type=row[9],
                               date_year=row[10],
                               medium=' '.join(row[11].split()),
                               signature_and_writing=row[12],
                               condition=row[13],
                               category=row[14],
                               height=row[15] if row[15] and row[15] != '?' else None,
                               width=row[16] if row[16] and row[16] != '?' else None,
                               depth=row[17] if row[17] else None,
                               size_note=row[18],
                               dimensions=row[19],
                               file1=decode_image(row[20]),
                               file2=decode_image(row[21]),
                               file3=decode_image(row[22]),
                               file4=decode_image(row[23]),
                               file5=decode_image(row[24]),
                               url1=row[20],
                               url2=row[21],
                               url3=row[22],
                               url4=row[23],
                               url5=row[24]
                               )
            old_work.save()

    context = {'form': form, }
    return render(request, 'works/file_load.html', context)


def upload_works(request) -> HttpResponse:
    form = WorkLoadForm(request.POST or None, request.FILES or None)
    Work.objects.all().delete()
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


def view_old_works(request) -> HttpResponse:
    context = {
        'old_works': OldWork.objects.all()
    }
    return render(request, 'works/view_old_work.html', context)


def work_home(request) -> HttpResponse:
    global search_field
    cols = strip_cols(Work._meta.get_fields())

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
    context = {
        'form': form,
        'works': Work.objects.all().filter(search
    ).order_by(sort_field, "id"),
        'cols': strip_cols(Work._meta.get_fields())
    }
    return render(request, "works/works.html", context=context)

def clear_work(request):
    global search_field
    search_field = ''
    return redirect('works_home')


def create_work(request):
    if request.method == 'POST':
        form = WorkDDLForm(request.POST)
        if form.is_valid():
            form.save()
            # username = form.cleaned_data.get('username')
            messages.success(request, f'{form.instance} has been created')
            return redirect('works_home')
    else:
        form = WorkDDLForm()
    return render(request, "works/create_work.html", {'form': form})


def work_edit(request, id):
    work = Work.objects.get(id=id)
    if request.method == 'POST':
        form = WorkDDLForm(request.POST, instance=work)
        if form.is_valid():
            form.save()
            messages.success(request, f'{work} has been modified')
            return redirect('works_home')
    else:
        form = WorkDDLForm(instance=work)
    return render(request, "works/work_edit.html", {'form': form})

def work_delete(request, id):
    work = Work.objects.get(id=id)
    if request.method == 'POST':
        work.delete()
        messages.success(request, f'{work} has been deleted')
        return redirect('works_home')
    return render(request, "works/delete_work.html", {'work': work})


def view_work(request, id) -> HttpResponse:
    last = -1 if id ==1 else id-1
    next = id+1
    context = {
        'work': Work.objects.get(id=id),
        'last': last,
        'next': next
    }
    return render(request, 'works/work.html', context)


def download_old_works(request):
    response = HttpResponse(
        content_type='text/csv',
        headers={'Content-Disposition': 'attachment; filename="old_inventory.csv"'},
    )
    cols=[f.name for f in OldWork._meta.get_fields()]

    writer = csv.writer(response)
    writer.writerow(cols)
    oldworks = OldWork.objects.all()

    for work in oldworks:
        row = [getattr(oldworks, f.name) for f in OldWork._meta.get_fields()]
        writer.writerow(row)

    return response


def download_works(request):
    response = HttpResponse(
        content_type='text/csv',
        headers={'Content-Disposition': 'attachment; filename="inventory.csv"'},
    )
    cols = [f.name for f in OldWork._meta.get_fields()]

    writer = csv.writer(response)
    writer.writerow(cols)
    works = Work.objects.all()
    for work in works:
        row = [getattr(work, f.name) for f in Work._meta.get_fields()]
        writer.writerow(row)

    return response
