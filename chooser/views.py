from django.shortcuts import render, redirect


def home_chooser(request):
    if request.session.get("choice") == 'Contacts':
        request.session['choice'] = 'Work'
        return redirect('home_works')
    elif request.session.get("choice") == 'Work':
        if not request.user.is_superuser:
            request.session['choice'] = 'Contacts'
            return redirect('home_contacts')
        else:
            request.session['choice'] = 'Original'
            return redirect('home_original')
    else:
        request.session['choice'] = 'Contacts'
        return redirect('home_contacts')