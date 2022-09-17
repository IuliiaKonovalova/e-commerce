"""Views for the profiles app."""
from django.views import View
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.http import JsonResponse, HttpResponseRedirect
from .models import Role, Profile, Address
from .forms import ProfileForm, AddressForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash


class UserProfileView(View):
    """View for the profile page."""
    def get(self, request, *args, **kwargs):
        """Get the profile page."""
        if request.user.is_authenticated:
            my_profile = get_object_or_404(
                Profile,
                user=request.user
            )
            my_addresses = Address.objects.filter(
                user=request.user
            )
            primary_address = Address.objects.filter(
                user=request.user,
                is_primary=True
            )
            context = {
                'my_profile': my_profile,
                'my_addresses': my_addresses,
                'primary_address': primary_address
            }
            return render(
                request,
                'profiles/my_profile.html',
                context
            )
        else:
            return render(
                request,
                'account/login.html'
            )


class EditAvatarAjaxView(View):
    """View for the edit avatar page."""
    def post(self, request, *args, **kwargs):
        """Post request for the edit avatar page."""
        if request.is_ajax():
            user = request.user
            new_avatar = request.FILES['avatar']
            user.profile.avatar = new_avatar
            user.profile.save()
            avatar_url = user.profile.avatar.url
            return JsonResponse({'success': True, 'avatar_url': avatar_url})
        return JsonResponse({'success': False})


class ResetAvatarView(View):
    """View for the reset avatar page."""
    def post(self, request, *args, **kwargs):
        """Post request for the reset avatar page."""
        if request.is_ajax():
            user = request.user
            user.profile.avatar = None
            user.profile.save()
            return JsonResponse({'success': True})
        return JsonResponse({'success': False})


class EditUserProfileView(View):
    """View for the edit profile page."""
    def get(self, request, *args, **kwargs):
        """Get request for the edit profile page."""
        if request.user.is_authenticated:
            profile_form = ProfileForm(instance=request.user.profile)
            password_form = PasswordChangeForm(user=request.user)
            password_form.fields[
                'old_password'
            ].widget.attrs['autofocus'] = False
            context = {
                'profile_form': profile_form,
                'password_form': password_form
            }
            return render(
                request,
                'profiles/edit_profile.html',
                context
            )
        else:
            return render(
                request,
                'account/login.html'
            )

    def post(self, request, *args, **kwargs):
        """Post request for the edit profile page."""
        if request.user.is_authenticated:
            if request.POST['form_type'] == 'profile':
                profile_form = ProfileForm(
                    request.POST, instance=request.user.profile)
                if profile_form.is_valid():
                    request.user.profile = profile_form.save()
                    return JsonResponse({'success': True})
                return JsonResponse(
                    {'success': False, 'errors': profile_form.errors}
                )
            if request.POST['form_type'] == 'password':
                password_form = PasswordChangeForm(request.user, request.POST)
                if password_form.is_valid():
                    password_form.save()
                    update_session_auth_hash(request, password_form.user)
                    return JsonResponse({'success': True})
                return JsonResponse(
                    {'success': False, 'errors': password_form.errors}
                )
        else:
            return render(
                request,
                'account/login.html'
            )


class DeleteProfileView(View):
    """View for the delete profile page."""
    def post(self, request, *args, **kwargs):
        """request for the delete profile page."""
        if request.is_ajax():
            if request.user.is_authenticated:
                user = request.user
                user.delete()
                return JsonResponse(
                    {'success': True}
                )
        return JsonResponse({'success': False})


class AddressesView(View):
    """View for the addresses page."""
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            addresses = Address.objects.filter(user=request.user)
            context = {
                'addresses': addresses,
            }
            return render(
                request,
                'profiles/my_addresses.html',
                context
            )
        else:
            return render(
                request,
                'account/login.html'
            )


class AddAddressView(View):
    """View for the add address page."""
    def get(self, request, *args, **kwargs):
        """Get request for the add address page."""
        if request.user.is_authenticated:
            address_form = AddressForm()
            user = request.user.username
            context = {
                'address_form': address_form,
                'user': user
            }
            return render(
                request,
                'profiles/add_address.html',
                context
            )
        else:
            return render(
                request,
                'account/login.html'
            )

    def post(self, request, *args, **kwargs):
        """Post request for the add address page."""
        if request.user.is_authenticated:
            address_form = AddressForm(request.POST)
            user_name = request.user.username
            if address_form.is_valid():
                address = address_form.save(commit=False)
                address.user = request.user
                address.save()
                return HttpResponseRedirect(
                    reverse(
                        'my_addresses',
                        kwargs={'user': user_name}
                    )
                )
            return render(
                request,
                'profiles/add_address.html',
                {'address_form': address_form}
            )
        else:
            return render(
                request,
                'account/login.html'
            )


class EditAddressView(View):
    """View for the edit address page."""
    def get(self, request, *args, **kwargs):
        """Get request for the edit address page."""
        if request.user.is_authenticated:
            address_id = kwargs['pk']
            address = get_object_or_404(Address, id=address_id)
            address_form = AddressForm(instance=address)
            user = request.user.username
            context = {
                'address_form': address_form,
                'address': address,
                'user': user
            }
            return render(
                request,
                'profiles/edit_address.html',
                context
            )
        else:
            return render(
                request,
                'account/login.html'
            )

    def post(self, request, *args, **kwargs):
        """Post request for the edit address page."""
        if request.user.is_authenticated:
            address_id = kwargs['pk']
            address = get_object_or_404(Address, id=address_id)
            address_form = AddressForm(request.POST, instance=address)
            user = request.user.username
            context = {
                'address_form': address_form,
                'address': address,
                'user': user
            }
            if address_form.is_valid():
                address_form.save()
                return HttpResponseRedirect(
                    reverse(
                        'my_addresses',
                        kwargs={'user': user}
                    )
                )
            return render(
                request,
                'profiles/edit_address.html',
                context
            )
        else:
            return render(
                request,
                'account/login.html'
            )


class DeleteAddressView(View):
    """View for the delete address page."""
    def get(self, request, *args, **kwargs):
        """Get request for the delete address page."""
        if request.user.is_authenticated:
            address_id = kwargs['pk']
            address = get_object_or_404(Address, id=address_id)
            address.delete()
            return HttpResponseRedirect(
                reverse(
                    'my_addresses',
                    kwargs={'user': request.user.username}
                )
            )
        else:
            return render(
                request,
                'account/login.html'
            )


class ChangePrimaryAddressView(View):
    """View for changing primary address."""
    def post(self, request, *args, **kwargs):
        """Post request for changing primary address."""
        if request.is_ajax():
            address_id = request.POST['address_id']
            address = get_object_or_404(Address, id=address_id)
            primary = True
            if address.is_primary:
                address.is_primary = False
                address.save()
                primary = False
                return JsonResponse({'success': True, 'primary': primary})
            address.is_primary = True
            address.save()
            primary = True
            return JsonResponse({'success': True, 'primary': primary})
        else:
            return JsonResponse({'success': False})
