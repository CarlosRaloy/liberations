from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import ReleaseForm, ReleaseEditForm, DeletePartForm, DeletePartFormSet, UserRegistrationForm, CustomAuthenticationForm
from .models import ReleaseModel, DeletePartsModel, Profile
from datetime import timedelta
from liberations.emails import email_user

def solicitudes_list_view(request):
    solicitudes = ReleaseModel.objects.all()

    # Calcular el tiempo transcurrido entre creación y modificación para cada solicitud
    for solicitud in solicitudes:
        time_diff = solicitud.updated_at - solicitud.created_at
        hours, remainder = divmod(time_diff.total_seconds(), 3600)
        minutes, seconds = divmod(remainder, 60)
        solicitud.time_diff_text = f"{int(hours)} hr {int(minutes)} min {int(seconds)} sec"

    # Manejando el inicio de sesión y los formularios como antes
    if request.method == 'POST' and 'login' in request.POST:
        login_form = CustomAuthenticationForm(data=request.POST)
        if login_form.is_valid():
            user = login_form.get_user()
            login(request, user)
            return redirect('releases:panel')
    else:
        login_form = CustomAuthenticationForm()

    # Pasamos las solicitudes con el cálculo de tiempo transcurrido al contexto
    return render(request, 'panel.html', {
        'solicitudes': solicitudes,
        'release_form': ReleaseForm(),
        'delete_part_form': DeletePartForm(),
        'login_form': login_form,
        'user_registration_form': UserRegistrationForm(),
    })


@login_required
def create_solicitud_view(request):
    if request.method == 'POST':
        default_code = request.POST.get('default_code')
        change_code = request.POST.get('change_code')
        massive_changes = request.POST.get('massive_changes') == 'true'
        parts = request.POST.getlist('parts[]')

        release = ReleaseModel.objects.create(
            id_user=request.user.profile,
            default_code=default_code,
            change_code=change_code,
            massive_changes=massive_changes
        )

        # Enviar el correo con los detalles de la solicitud
        email_user(default_code, change_code, parts, massive_changes)

        for part in parts:
            if part:
                DeletePartsModel.objects.create(id_release=release, part=part)

        return JsonResponse({'success': True})

    return JsonResponse({'success': False}, status=400)


@login_required
def edit_solicitud_view(request, pk):
    solicitud = get_object_or_404(ReleaseModel, pk=pk)

    if request.method == 'POST':
        form = ReleaseEditForm(request.POST, instance=solicitud)
        if form.is_valid():
            form.save()  # Guardar los cambios
            return redirect('releases:panel')  # Redirigir al panel
    else:
        form = ReleaseEditForm(instance=solicitud)

    return render(request, 'edit_solicitud.html', {'form': form})


def detail_solicitud_view(request, pk):
    solicitud = get_object_or_404(ReleaseModel, pk=pk)
    partes = DeletePartsModel.objects.filter(id_release=solicitud)

    return render(request, 'detail_solicitud.html', {
        'solicitud': solicitud,
        'partes': partes
    })


@login_required
def register_user_view(request):
    if request.user.profile.level != 1:
        return JsonResponse({'success': False, 'message': 'No tienes permisos para registrar usuarios'}, status=403)

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            profile = Profile.objects.create(user=user, level=form.cleaned_data['level'])
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)
    return JsonResponse({'success': False}, status=400)

def logout_view(request):
    logout(request)
    return redirect('releases:panel')


def logout_view(request):
    logout(request)
    return redirect('releases:panel')
