from datetime import datetime
from os.path import exists


from django.db.models import Q
from django.http import HttpResponse

from django.shortcuts import render, redirect
from .forms import WorkLoadForm
import csv

from .models import OldWork
from io import StringIO
from django.contrib import messages
from django.core.paginator import Paginator
from common.CategoryChoices import CategoryChoices

# CATEGORY_CHOICES = [
#     ('Painting', 'Painting'),
#     ('Container', 'Container'),
#     ('Drawing', 'Drawing'),
#     ('Photography', 'Photography'),
#     ('Sketch Pad', 'Sketch Pad'),
#     ('Electromedia', 'Electromedia'),
#     ('Videograms', 'Videograms'),
#     ('Poetry Poster', 'Poetry Poster'),
#     ('Notebook', 'Notebook'),
#     ('Album', 'Album'),
# ]

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


def decode_category(before: str) -> str:
    if not before:
        return before
    for (key, val) in CategoryChoices.category_choices():
        if before.strip() == val:
            return key
    raise ValueError(before)


def decode_image(name: str, index, id) -> str:
    name = name.strip()
    if not name or name == '':
        if index == 0:
            file=f"{id}.jpg"
            file_exists = exists(f'/Users/nickstrange/PycharmProjects/foundation/basedjango/contacts/static/thumbs/{file}')
            if file_exists:
                return file
        return None

    if not name.startswith('remote:'):
        print('Error', name)

    st = name.find(':')
    end = name.find('JPG')
    if end == -1:
        end = name.find('jpg')
    return name[st + 1:end + 3]


def check_null_category(category, item_id):
    return category if category else CategoryChoices.decode_item_id(item_id)
    # if not category:
    #     if item_id.startswith('AT.PP'):
    #         category = 'Poetry Poster'
    #     elif item_id.startswith('AT.D'):
    #         category = 'Drawing'
    #     elif item_id.startswith('AT.P'):
    #         category = 'Painting'
    #     elif item_id.startswith('AT.E'):
    #         category = 'Electromedia'
    #     elif item_id.startswith('AT.B'):
    #         category = 'Container'
    #     else:
    #         print(item_id)
    # return category


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

            row[14] = check_null_category(row[14], row[1])

            if row[1].strip() == 'AT.P 0774':
                print('ignore', row[1])
            else:
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
                                   file1=decode_image(row[20], 0, row[1]),
                                   file2=decode_image(row[21], 1, row[1]),
                                   file3=decode_image(row[22], 2, row[1]),
                                   file4=decode_image(row[23], 3, row[1]),
                                   file5=decode_image(row[24], 4, row[1]),
                                   url1=row[20],
                                   url2=row[21],
                                   url3=row[22],
                                   url4=row[23],
                                   url5=row[24]
                                   )
                old_work.save()

    context = {'form': form, }
    return render(request, 'original/file_load.html', context)


def home_original(request) -> HttpResponse:
    search_field=''
    sort_field="index"
    search = Q(index__contains=search_field) | Q(item_id__contains=search_field) | \
        Q(source__contains=search_field)
    page_number = request.GET.get('page')
    work_list = OldWork.objects.all().filter(search).order_by(sort_field, "index")
    paginator = Paginator(work_list, 15)
    old_works = paginator.get_page(page_number)
    context = {
        'old_works': old_works
    }
    return render(request, 'original/home_original.html', context)


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
