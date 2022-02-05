from datetime import datetime

from django.db.models import Q
from django.http import HttpResponse

from django.shortcuts import render, redirect
from .forms import WorkLoadForm
import csv

from .models import OldWork
from io import StringIO
from django.contrib import messages

CATEGORY_CHOICES = [
    ('Painting', 'Painting'),
    ('Photography', 'Photography'),
    ('Sketch Pad', 'Sketch Pad'),
    ('Electromedia', 'Electromedia'),
    ('Videograms', 'Videograms'),
    ('Poetry Poster', 'Poetry Poster'),
    ('Notebook', 'Notebook'),
    ('Album', 'Album'),
]

SOURCE_CHOICES = [
    ('Aldo foundation', 'Aldo foundation'),
    ('Anna', 'Anna'),
    ('Gifted', 'Gifted'),
]

def decode_source(before:str)->str:
    if not before:
        return before
    for (key, val) in SOURCE_CHOICES:
        if before.strip() == val:
            return key
    raise ValueError


def decode_category(before:str)->str:
    if not before:
        return before
    for (key, val) in CATEGORY_CHOICES:
        if before.strip() == val:
            return key
    raise ValueError

def decode_image(name: str) -> str:
    name = name.strip()
    if not name or name == '':
        return None
    if not name.startswith('remote:'):
        print('Error', name)

    st = name.find(':')
    end = name.find('JPG')
    if end == -1:
        end = name.find('jpg')
    print('y', st, end, 'x', name[st + 1: end + 3])
    return name[st + 1:end + 3]


def upload_old_works(request) -> HttpResponse:
    form = WorkLoadForm(request.POST or None, request.FILES or None)
    # check whether it's valid:
    if form.is_valid():
        file = form.cleaned_data['file_name']
        csvf = StringIO(file.read().decode())
        reader = csv.reader(csvf, delimiter=',')
        cnt = 0
        OldWork.objects.all().delete()
        for row in reader:
            cnt += 1
            if cnt == 1:
                continue
            print(cnt, row[6])
# first
#

            old_work = OldWork(index=cnt-1,
                               item_id=row[1],
                               source=row[2],
                               notes=row[3],
                               location=row[4],
                               value=row[5] if row[5] else None,
                               inventory_date=datetime.strptime(row[6], '%m/%d/%Y') if row[6] else None,
                               #selected file placeholder
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
    return render(request, 'original/file_load.html', context)


def home_old_works(request) -> HttpResponse:
    context = {
        'old_works': OldWork.objects.all()
    }
    return render(request, 'original/view_old_work.html', context)


def download_old_works(request):
    now = datetime.now()  # current date and tim
    date_time = now.strftime("%m/%d/%Y")

    response = HttpResponse(
        content_type='text/csv',
        headers={'Content-Disposition': f'attachment; filename="inventory{date_time}.csv"'},
    )
    cols = [f.name for f in OldWork._meta.get_fields()
            if f.name not in ['dimensions', 'type', 'url1', 'url2', 'url3', 'url4', 'url5']]
    print(cols)
    writer = csv.writer(response)
    writer.writerow(cols)
    oldworks = OldWork.objects.all()

    for work in oldworks:
        work.category = decode_category(work.category)
        work.source = decode_source(work.source)
        row = [getattr(work, f) for f in cols]
        writer.writerow(row)

    return response
