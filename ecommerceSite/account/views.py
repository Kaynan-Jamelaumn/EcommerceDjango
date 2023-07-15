from django.shortcuts import render, redirect

# from .models import account
from django.contrib.auth.models import User  # REGISTER  # REGISTER

from validator import password_validator  # REGISTER
from validator import state_city_validator  # State_On_Change

from django.contrib.auth import authenticate, login, logout  # LOGIN

from django.http import JsonResponse  # State_on_change
from .models import Address  # Address Address_register Address_delete

from ecommerceSite.order.models import Orders

import re  # i  dont know regex

password_pattern = "^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$"


# Create your views here.
def user_login(request):
    if request.user.is_authenticated:
        return redirect('ecommerce:product:index')

    if request.method == 'GET':
        return render(request, 'account/login.html')

    if request.method == 'POST':
        email = request.POST.get('email')  # EMAIL OR USERNAME
        password = request.POST.get('password')
        try:
            the_user_filtered_by_email = User.objects.get(email=email)
            the_username = the_user_filtered_by_email.username
            user = authenticate(request,
                                username=the_username,
                                password=password)
        except:
            user = authenticate(request, username=email, password=password)
        finally:
            if user is None:
                return render(request, 'account/login.html',
                              {'message': 'credentials are wrong'})
            login(request, user)
            return redirect('ecommerce:product:index')


def register(request):
    if request.user.is_authenticated:
        return redirect('ecommerce:product:index')
    if request.method == 'GET':
        return render(request, 'account/register.html')

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_confirmation = request.POST.get('password-confirmation')
        if not (name or email or password or password_confirmation):
            return render(request, 'account/register.html',
                          {'message': "Verify if there's an empty field"})
        is_password_valid = password_validator(
            password, password_confirmation)  # Validator
        if is_password_valid != True:
            return render(request, 'account/register.html',
                          {'message': is_password_valid[0]})

        pat = "^[a-zA-Z0-9-_]+@[a-zA-Z0-9]+\.[a-z]{1,3}$"
        if not re.match(pat, email):
            return render(request, 'account/register.html',
                          {'message': 'e-mail is invalid'})
        if not User.objects.filter(email=email) and not User.objects.filter(
                username=name):
            user = User.objects.create_user(username=name,
                                            email=email,
                                            password=password)
            user.save()
            login(request, user)
            return redirect('ecommerce:product:index')
        return render(request, 'account/register.html',
                      {'message': 'user or email already registred'})


def user_logout(request):
    logout(request)
    return redirect('ecommerce:account:login')


def user_update(request):
    if request.method == 'GET':
        return render(request, 'account/update.html')
    if request.method == 'POST':
        password = request.POST.get('password')
        password_confirmation = request.POST.get('password_confirmation')
        if re.match(password_pattern, password):
            if password == password_confirmation:
                """
                User.objects.filter(pk=request.user.pk).update(
                    password=password)
                """
                u = User.objects.get(pk=request.user.pk)
                u.set_password(password)
                u.save()
                return render(request, 'account/dashboard.html',
                              {'message': 'password updated successfuly'})
            return render(request, 'account/update.html',
                          {'message': 'password not valid'})
        return render(request, 'account/update.html',
                      {'message': 'password not valid'})


def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('ecommerce:account:login')

    orders = Orders.objects.filter(user=request.user).order_by('-id')
    return render(request, 'account/dashboard.html', {'orders': orders})


def address(request):
    if not request.user.is_authenticated:
        redirect('ecommerce:account:login')

    addresses = Address.objects.filter(user=request.user)
    return render(request, 'account/address.html', {'addresses': addresses})


def address_delete(request, id):
    if not request.user.is_authenticated:
        return redirect('ecommerce:account:login')

    address = Address.objects.get(id=id, user=request.user)
    if address is not None:
        address.delete()

    return redirect('ecommerce:account:address')


def address_edit(request, id):
    if not request.user.is_authenticated:
        return redirect('ecommerce:account:login')
    if request.method == 'GET':
        address = Address.objects.get(id=id, user=request.user)
        if address is None:
            return redirect('ecommerce:account:address')
        states = (
            ('Acre'),
            ('Alagoas'),
            ('Amapá'),
            ('Amazonas'),
            ('Bahia'),
            ('Ceará'),
            ('Distrito Federal'),
            ('Espírito Santo'),
            ('Goiás'),
            ('Maranhão'),
            ('Mato Grosso'),
            ('Mato Grosso do Sul'),
            ('Minas Gerais'),
            ('Pará'),
            ('Paraíba'),
            ('Paraná'),
            ('Pernambuco'),
            ('Piauí'),
            ('Rio de Janeiro'),
            ('Rio Grande do Norte'),
            ('Rio Grande do Sul'),
            ('Rondônia'),
            ('Roraima'),
            ('Santa Catarina'),
            ('São Paulo'),
            ('Sergipe'),
            ('Tocantins'),
        )

        return render(request, 'account/address_edit.html', {
            'address': address,
            'states': states,
        })
    if request.method == 'POST':
        postcode = request.POST.get('postcode')
        address = request.POST.get('address')
        number = request.POST.get('number')
        state = request.POST.get('state')
        city = request.POST.get('city')
        if not (address or number or postcode):
            return render(request, 'account/register.html',
                          {'message': "Verify if there's an empty field"})
        if number != int:
            return render(request, 'account/register.html',
                          {'message': "Number must be integer"})
        if state not in states:
            return render(request, 'account/register.html',
                          {'message': "Stop Being silly"})
        Address.objects.filter(pk=id).update(address=address,
                                             number=number,
                                             post_code=postcode,
                                             state=state,
                                             city=city)
        return redirect('ecommerce:account:dashboard')


def address_register(request):

    if not request.user.is_authenticated:
        return redirect('ecommerce:account:login')
    states = (
        ('Acre'),
        ('Alagoas'),
        ('Amapá'),
        ('Amazonas'),
        ('Bahia'),
        ('Ceará'),
        ('Distrito Federal'),
        ('Espírito Santo'),
        ('Goiás'),
        ('Maranhão'),
        ('Mato Grosso'),
        ('Mato Grosso Do Sul'),
        ('Minas Gerais'),
        ('Pará'),
        ('Paraíba'),
        ('Paraná'),
        ('Pernambuco'),
        ('Piauí'),
        ('Rio De Janeiro'),
        ('Rio Grande Do Norte'),
        ('Rio Grande Do Sul'),
        ('Rondônia'),
        ('Roraima'),
        ('Santa Catarina'),
        ('São Paulo'),
        ('Sergipe'),
        ('Tocantins'),
    )

    if request.method == 'GET':
        return render(request, 'account/address_register.html',
                      {'states': states})
    if request.method == 'POST':
        postcode = request.POST.get('postcode')
        address = request.POST.get('address')
        number = request.POST.get('number')
        state = request.POST.get('state')
        city = request.POST.get('city')
        if not (address or number or postcode):
            return render(request, 'account/register.html',
                          {'message': "Verify if there's an empty field"})
        if number != int:
            return render(request, 'account/register.html',
                          {'message': "Number must be integer"})
        if state not in states:
            return render(request, 'account/register.html',
                          {'message': "Stop Being silly"})
        address_object = Address(user=request.user,
                                 address=address,
                                 number=number,
                                 post_code=postcode,
                                 state=state,
                                 city=city)
        address_object.save()
        return redirect('ecommerce:account:dashboard')


def state_on_change(request):
    if request.POST.get('action') == 'state_on_change':
        state_selected = request.POST.get('state_selected')
        receive_cities = state_city_validator(state_selected)

        if receive_cities:
            response = JsonResponse({'cities_in_state': receive_cities})
            return response
