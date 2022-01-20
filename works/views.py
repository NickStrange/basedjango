from datetime import datetime

from django.http import HttpResponse

from django.shortcuts import render
from .forms import WorkLoadForm, OldWorkForm, WorkForm
import csv

from .models import OldWork, Work
from io import StringIO

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

def view_works(request) -> HttpResponse:
    # works=Work.objects.all()
    # d = {work.category:True for work in works}
    # print('distinct', d)
    context = {
        'works': Work.objects.all()
    }
    return render(request, 'works/view_work.html', context)

def view_work(request, id) -> HttpResponse:
    # works=Work.objects.all()
    # d = {work.category:True for work in works}
    # print('distinct', d)

    context = {
        'work': Work.objects.get(id=id)
    }
    return render(request, 'works/work.html', context)


def download_old_works(request):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(
        content_type='text/csv',
        headers={'Content-Disposition': 'attachment; filename="old_inventory.csv"'},
    )
    cols = [
          'Index',
          'Item_id',
          'Source',
          'Notes',
          'Location',
          'Value',
          'Inventory_date',
          'Title',
          'Series',
          'Date_year',
          'Medium',
          'Signatures_and_writing',
          'Condition',
          'Category',
          'Height',
          'Width',
          'Depth',
          'Size_notes'
          'File1',
          'File2',
          'File3',
          'File4',
          'File5',
    ]

    writer = csv.writer(response)
    writer.writerow(cols)
    oldworks = OldWork.objects.all()

    for work in oldworks:
        row = [work.index,
               work.item_id,
               work.source,
               work.notes,
               work.location,
               work.value,
               work.inventory_date,
               work.title,
               work.series,
               work.date_year,
               work.medium,
               work.signature_and_writing,
               work.condition,
               work.category,
               work.height,
               work.width,
               work.depth,
               work.size_note,
               work.file1,
               work.file2,
               work.file3,
               work.file4,
               work.file5
               ]
        writer.writerow(row)

    return response


def download_works(request):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(
        content_type='text/csv',
        headers={'Content-Disposition': 'attachment; filename="inventory.csv"'},
    )

    cols = [
          'Id',
          'Item',
          'Source',
          'Notes',
          'Location',
          'Value',
          'Inventory_date',
          'Title',
          'Date_year',
          'Medium',
          'Signatures_and_writing',
          'Condition',
          'Category',
          'File1',
          'File2',
          'File3',
          'File4',
          'File5',
    ]

    writer = csv.writer(response)
    writer.writerow(cols)
    works = Work.objects.all()
    for work in works:
        row = [work.id,
               work.item_id,
               work.source,
               work.notes,
               work.location,
               work.value,
               work.inventory_date,
               work.title,
               work.date_year,
               work.medium,
               work.signature_and_writing,
               work.condition,
               work.category,
               work.file1,
               work.file2,
               work.file3,
               work.file4,
               work.file5
               ]
        writer.writerow(row)

    return response
