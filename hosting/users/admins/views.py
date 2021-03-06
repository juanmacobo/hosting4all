# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from . import repository

@login_required
def index(request):
    tittle='Dashboard'
    sidebaractive='active'
    topmenu='current'
    context = {
        'tittle' : tittle,
        'activedashboard' : sidebaractive,
    }
    return render(request, 'index.html', context)


@login_required
def appusers(request):
    title='Hosting: App User Management'
    sidebaractive='active'
    topmenu='current'
    context = {
        'title' : title,
        'activeappusers' : sidebaractive,
        'currenttopmenu' : topmenu
    }
    user_repository = repository.UsersRepository()
    common_users, premium_users = user_repository.get_users()
    context['common_users'] = common_users
    context['premium_users'] = premium_users

    # List for delete users
    users = []
    for i in common_users:
        users.append(i)
    for i in premium_users:
        users.append(i)

    context['appusers'] = users

    return render(request, 'admin/appusers.html', context)


@login_required
def _adduser(request):
    user = {}
    username = request.POST['username']
    name = request.POST['name']
    surname = request.POST['surname']
    mail = request.POST['mail']
    premium = request.POST.get('premium', False)
    if premium is False:
        # common users gidNumber
        gidNumber = 2000
    else:
        # premium users gidNumber
        gidNumber = 2001
    user_repository = repository.UsersRepository()
    password_hash = user_repository.get_pwhash_for_user(request.POST['password'])
    uidNumber = user_repository.get_uidNumber_for_user()
    user['uid'] = username
    user['objectclass'] = ['top', 'inetOrgPerson', 'person', 'posixAccount']
    user['user_attributes'] = {
        'cn': username,
        'uid': username,
        'uidNumber': uidNumber,
        'gidNumber': gidNumber,
        'userPassword': password_hash,
        'homeDirectory': '/srv/hosting/' + username,
        'sn': surname,
        'mail': mail,
        'givenName': name}
    ldap_password = request.POST['ldap_password']
    user_repository.create_user(ldap_password, user)
    return redirect('/admin/appusers')

@login_required
def _deluser(request):
    username = request.POST['usertodel']
    ldap_password = request.POST['ldap_password']

    user_repository = repository.UsersRepository()
    user_repository._delete_app_user(ldap_password, username)
    return redirect('/admin/appusers')
