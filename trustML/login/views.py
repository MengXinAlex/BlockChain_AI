from django.contrib.auth import login, authenticate, update_session_auth_hash
from django.shortcuts import render, redirect
from .forms import SignUpForm, EditProfileForm
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib import messages
import os
import sys
sys.path.append(os.path.abspath(os.path.join('..', 'trustML')))
from trustML.compile_solidity_utils import w3

def index(request):
    return render(request, 'index.html')
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.wallet_address = w3.personal.newAccount("")
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(email=user.email, password=raw_password)
            login(request, user)
            return redirect('/user_home/')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def editprofile(request):
    if request.method == 'POST':
        if 'change_profile' in request.POST:
            form = EditProfileForm(request.POST, request.FILES, instance=request.user)
            if form.is_valid():
                form.save()
                messages.success(request, 'Profile successfully updated.')
                return redirect('/profile')
            else:
                messages.error(request, 'Profile failed to update.')
                return redirect('/profile')
        elif 'change_pw' in request.POST:
            change_pw_form = PasswordChangeForm(data=request.POST, user=request.user)
            if change_pw_form.is_valid():
                change_pw_form.save()
                update_session_auth_hash(request, change_pw_form.user)
                messages.success(request, 'Password successfully changed.')
                return redirect('/profile')
            else:
                messages.error(request, 'Password change failed. Please check that all requirements above are satisfied.')
                return redirect('/profile')
    else:
        form = EditProfileForm(instance=request.user)
        change_pw_form = PasswordChangeForm(user=request.user)
        args = {'form': form, 'change_pw_form': change_pw_form}
        #b = w3.fromWei(w3.eth.getBalance(w3.toChecksumAddress(args['wallet_address'])), 'ether')
        #args['balance'] = b
    return render(request, 'user_profile.html', args)
