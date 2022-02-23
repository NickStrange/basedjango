from django.shortcuts import render, redirect


def home_chooser(request, home_type):
    if home_type == "work":
        request.session['choice'] = 'Works'
        return redirect('home_works')
    elif home_type == 'original':
        if not request.user.is_superuser:
            request.session['choice'] = 'Contacts'
            return redirect('home_contacts')
        else:
            request.session['choice'] = 'Original'
            return redirect('home_original')
    else:
        request.session['choice'] = 'Contacts'
        return redirect('home_contacts')