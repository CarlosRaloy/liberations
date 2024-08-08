from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import ReleaseForm, ReleaseEditForm, DeletePartForm, UserRegistrationForm, CustomAuthenticationForm
from .models import ReleaseModel, DeletePartsModel, Profile


def solicitudes_list_view(request):
    solicitudes = ReleaseModel.objects.all()
    if request.method == 'POST' and 'login' in request.POST:
        login_form = CustomAuthenticationForm(data=request.POST)
        if login_form.is_valid():
            user = login_form.get_user()
            login(request, user)
            return redirect('releases:panel')
    else:
        login_form = CustomAuthenticationForm()

    return render(request, 'panel.html', {'solicitudes': solicitudes, 'login_form': login_form})


@login_required
def create_solicitud_view(request):
    if request.user.profile.level != 1 and request.user.profile.level != 0:
        return redirect('releases:panel')

    if request.method == 'POST':
        release_form = ReleaseForm(request.POST, user=request.user)
        delete_part_form = DeletePartForm(request.POST)
        if release_form.is_valid() and delete_part_form.is_valid():
            release = release_form.save(commit=False)
            release.id_user = request.user.profile
            release.save()
            delete_part = delete_part_form.save(commit=False)
            delete_part.id_release = release
            delete_part.save()
            return redirect('releases:panel')
    else:
        release_form = ReleaseForm(user=request.user)
        delete_part_form = DeletePartForm()
    return render(request, 'create_solicitud.html', {
        'release_form': release_form,
        'delete_part_form': delete_part_form,
    })


@login_required
def edit_solicitud_view(request, pk):
    solicitud = get_object_or_404(ReleaseModel, pk=pk)
    if request.user.profile.level != 1:
        return redirect('releases:panel')

    if request.method == 'POST':
        form = ReleaseEditForm(request.POST, instance=solicitud)
        if form.is_valid():
            form.save()
            return redirect('releases:panel')
    else:
        form = ReleaseEditForm(instance=solicitud)
    return render(request, 'edit_solicitud.html', {'form': form})


def detail_solicitud_view(request, pk):
    solicitud = get_object_or_404(ReleaseModel, pk=pk)
    return render(request, 'detail_solicitud.html', {'solicitud': solicitud})


@login_required
def register_user_view(request):
    if request.user.profile.level != 1:
        return redirect('releases:panel')

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            Profile.objects.create(user=user, level=form.cleaned_data['level'])
            return redirect('releases:panel')
    else:
        form = UserRegistrationForm()

    return render(request, 'register_user.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('releases:panel')
