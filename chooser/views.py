from django.shortcuts import render, redirect


def home_chooser(request):
    print('chooser', request.session.get("choice"))
    if request.session.get("choice") == 'Contacts':
        request.session['choice'] = 'Work'
        print('redirect work', request.session.get("choice"))
        return redirect('home_works')
    elif request.session.get("choice") == 'Work':
        request.session['choice'] = 'Original'
        print('redirect contacts', request.session.get("choice"))
        return redirect('home_original')
    else:
        request.session['choice'] = 'Contacts'
        print('redirect contacts', request.session.get("choice"))
        return redirect('home_contacts')