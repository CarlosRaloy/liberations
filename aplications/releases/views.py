from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import ReleaseForm, ReleaseEditForm, DeletePartForm, DeletePartFormSet, UserRegistrationForm, CustomAuthenticationForm
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

    return render(request, 'panel.html', {
        'solicitudes': solicitudes,
        'release_form': ReleaseForm(),
        'delete_part_form': DeletePartForm(),
        'delete_part_formset': DeletePartFormSet(queryset=DeletePartsModel.objects.none()),
        'login_form': login_form,
    })


@login_required
def create_solicitud_view(request):
    if request.method == 'POST':
        default_code = request.POST.get('default_code')
        massive_changes = request.POST.get('massive_changes') == 'on'
        parts = request.POST.getlist('parts[]')

        release = ReleaseModel.objects.create(
            id_user=request.user.profile,
            default_code=default_code,
            massive_changes=massive_changes
        )

        for part in parts:
            if part:
                DeletePartsModel.objects.create(id_release=release, part=part)

        return JsonResponse({'success': True})
    return JsonResponse({'success': False}, status=400)

@login_required
def edit_solicitud_view(request, pk):
    solicitud = get_object_or_404(ReleaseModel, pk=pk)
    if request.user.profile.level != 1:  # Solo los administradores pueden editar
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
