from datetime import datetime

from django.http import HttpResponse
from django.shortcuts import render

from django.shortcuts import render
from .forms import WorkLoadForm, OldWorkForm
import csv

from .models import OldWork
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
    print('y',st, end,'x',name[st+1:end+3])
    return name[st+1:end+3]


def upload_old_works (request) -> HttpResponse:
    form = WorkLoadForm(request.POST or None, request.FILES or None)
    # check whether it's valid:
    if form.is_valid():
        file=form.cleaned_data['file_name']
        csvf=StringIO(file.read().decode())
        reader = csv.reader(csvf, delimiter=',')
        cnt=0
        for row in reader:
            cnt += 1
            if cnt == 1:
                continue
            old_work = OldWork(index =row[0],
                               item_id =row[1],
                               source =row[2],
                               notes =row[3],
                               location =row[4],
                               value =row[5] if row[5] else None,
                               inventory_date = datetime.strptime(row[6], '%m/%d/%Y') if row[6] else None,
                               title =row[7],
                               series =row[8],
                               type =row[9],
                               date_year =row[10],
                               medium =' '.join(row[11].split()),
                               signature_and_writing =row[12],
                               condition =row[13],
                               category =row[14],
                               height =row[15] if row[15] and row[15] != '?' else None,
                               width =row[16] if row[16] and row[16] != '?' else  None,
                               depth =row[17] if row[17] else None,
                               size_note =row[18],
                               dimensions =row[19],
                               file1 =decode_image(row[20]),
                               file2 =decode_image(row[21]),
                               file3 =decode_image(row[22]),
                               file4 =decode_image(row[23]),
                               file5 =decode_image(row[24]),
                               url1 =row[20],
                               url2 =row[21],
                               url3 =row[22],
                               url4 =row[23],
                               url5 =row[24]
            )
            old_work.save()

    context = {'form': form, }
    return render(request, 'works/file_load.html', context)

def view_old_works (request) -> HttpResponse:
    context = {
        'old_works': OldWork.objects.all()
    }
    return render(request, 'works/view_old_work.html', context)

def download_old_works(request):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(
        content_type='text/csv',
        headers={'Content-Disposition': 'attachment; filename="old_inventory.csv"'},
    )

    cols=[
          'Index',
          'Item',
          'Id',
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
    works = OldWork.objects.all()
    for work in works:
        row = [work.index,
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


