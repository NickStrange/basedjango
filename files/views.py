from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
# from .models import Post

# Create your views here.
from django.http import HttpResponse

# def file_load (request) -> HttpResponse:
#     # context = {
#     #     'posts': Post.objects.all()
#     # }
#     # return render(request, "blog/home.html", context)
#     # return HttpResponse("<h1>hello world</h1>")
#     return render(request, "works/file_load.html")


from django.shortcuts import render
from .forms import CsvForm
import csv

def file_load (request) -> HttpResponse:
    form = CsvForm(request.POST or None, request.FILES or None)
    # check whether it's valid:
    if form.is_valid():
        file=form.cleaned_data['file_name']
        for row in file:
            print(row)
    else:
        print("file is totally valid")

    context = {'form': form, }
    return render(request, 'works/file_load.html', context)

from django.http import HttpResponse


def file_write(request):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(
        content_type='text/csv',
        headers={'Content-Disposition': 'attachment; filename="somefilename.csv"'},
    )

    writer = csv.writer(response)
    writer.writerow(['First row', 'Foo', 'Bar', 'Baz'])
    writer.writerow(['Second row', 'A', 'B', 'C', '"Testing"', "Here's a quote"])

    return response
