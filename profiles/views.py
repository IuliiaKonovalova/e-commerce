"""Views for the profiles app."""
from django.views import View
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponseRedirect
from .models import Role, Profile, Address
from .forms import ProfileForm, AddressForm
from django.contrib.auth.forms import PasswordChangeForm


class UserProfileView(View):
    """View for the profile page."""
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            my_profile = get_object_or_404(
                Profile,
                user=request.user
            )
            my_addresses = Address.objects.filter(
                user=request.user
            )
            context = {
                'my_profile': my_profile,
                'my_addresses': my_addresses
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
    def post(self, request, *args, **kwargs):
        user = request.user
        new_avatar = request.FILES['avatar']
        user.profile.avatar = new_avatar
        user.profile.save()
        avatar_url = user.profile.avatar.url
        return JsonResponse({'success': True, 'avatar_url': avatar_url})




class EditUserProfileView(View):
    """View for the edit profile page."""
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            profile_form = ProfileForm(instance=request.user.profile)
            password_form = PasswordChangeForm(user=request.user)
            password_form.fields['old_password'].widget.attrs['autofocus'] = False
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
        if request.user.is_authenticated:
            if request.POST['form_type'] == 'profile':
                profile_form = ProfileForm(
                    request.POST, instance=request.user.profile)
                print(request.FILES)
                print(request.POST)
                if profile_form.is_valid():
                    profile_form.save()
                    return JsonResponse({'success': True})
                return JsonResponse(
                    {'success': False, 'errors': profile_form.errors}
                )
            if request.POST['form_type'] == 'password':
                password_form = PasswordChangeForm(request.POST)
                if password_form.is_valid():
                    password_form.save()
                    return JsonResponse({'success': True})
                return JsonResponse(
                    {'success': False, 'errors': password_form.errors}
                )
        else:
            return render(
                request,
                'account/login.html'
            )
