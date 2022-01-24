import csv
import io

from django.shortcuts import render, redirect
from .models import Contact
from .forms import ContactForm, UploadFileForm, SearchForm
from django.contrib import messages
from django.db.models import Q

sort_field = 'id'
search_field = ''


def strip_cols(full_col):
    result = [f.name for f in full_col]
    return result


def contact_home(request):
    global search_field
    cols = strip_cols(Contact._meta.get_fields())

    if request.method == 'POST':
        form = SearchForm(request.POST, initial={'search_text': search_field})
        if form.is_valid():
            search_field = form.cleaned_data['search_text']
    else:
        form = SearchForm(initial={'search_text': search_field})
    search = Q(last_name__contains=search_field) | Q(id__contains=search_field) | \
             Q(title__contains=search_field) | Q(first_name__contains=search_field) | \
             Q(phone_number__contains=search_field) | Q(email_address__contains=search_field) | \
             Q(company_name__contains=search_field) | Q(address__contains=search_field) | \
             Q(city__contains=search_field) | Q(country__contains=search_field) | \
             Q(state__contains=search_field) | Q(post_code__contains=search_field)
    context = {
        'form': form,
        'contacts': Contact.objects.all().filter(search
    ).order_by(sort_field, "id"),
        'cols': strip_cols(Contact._meta.get_fields())
    }
    return render(request, "contacts/home.html", context=context)


def contact_edit(request, id):
    contact = Contact.objects.get(id=id)
    if request.method == 'POST':
        form = ContactForm(request.POST, instance=contact)
        if form.is_valid():
            form.save()
            messages.success(request, f'{contact} has been modified')
            return redirect('contacts-home')
    else:
        form = ContactForm(instance=contact)
    return render(request, "contacts/contact_edit.html", {'form': form})


def create_contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            # username = form.cleaned_data.get('username')
            messages.success(request, f'{form.instance} has been created')
            return redirect('contacts-home')
    else:
        form = ContactForm()
    return render(request, "contacts/create_contact.html", {'form': form})


def contact_delete(request, id):
    contact = Contact.objects.get(id=id)
    if request.method == 'POST':
        contact.delete()
        messages.success(request, f'{contact} has been deleted')
        return redirect('contacts-home')
    return render(request, "contacts/delete_contact.html", {'contact': contact})


def contact_sort(request, column):
    global sort_field
    sort_field = column
    return redirect('contacts-home')


def contact_reverse_sort(request, column):
    global sort_field
    sort_field = f'-{column}'
    return redirect('contacts-home')


def read_file(file_name):
    file = file_name.read().decode('utf-8')
    reader = csv.DictReader(io.StringIO(file))

    # Generate a list comprehension
    data = [line for line in reader]
    for line in data:
        contact = Contact(id=line['id'], title=line['title'], first_name=line['first_name'],
                          last_name=line['last_name'], phone_number=line['phone_number'],
                          email_address=line['email_address'], company_name=line['company_name'],
                          address=line['address'], city=line['city'] , state=line['state'],
                          country=line['country'], post_code=line['post_code'])
        contact.save()
        print(contact)


def load_contacts(request):
    print('read', request)
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            read_file(request.FILES['file'])
            return redirect('contacts-home')
    else:
        form = UploadFileForm()
    return render(request, "contacts/load-contact.html", {'form': form})


def clear_contact(request):
    global search_field
    search_field = ''
    return redirect('contacts-home')
