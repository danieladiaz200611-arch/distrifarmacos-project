from django.contrib.auth import get_user_model
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
from django.views.decorators.http import require_GET, require_POST
from django.views.generic import CreateView, ListView, UpdateView

from core.utils import GruposRequeridosMixin, grupos_requeridos, is_ajax_request

from .forms import UsuarioForm, UsuarioGruposForm

User = get_user_model()


def _serializar_usuario(u):
    groups = ", ".join(u.groups.values_list("name", flat=True))
    return {
        "id": u.pk,
        "username": u.username,
        "email": u.email or "",
        "first_name": u.first_name,
        "last_name": u.last_name,
        "full_name": f"{u.first_name} {u.last_name}".strip(),
        "is_active": u.is_active,
        "is_active_label": "Activo" if u.is_active else "Inactivo",
        "is_active_badge_class": "text-bg-success" if u.is_active else "text-bg-secondary",
        "groups": groups,
        "editar_url": reverse("usuarios:editar_modal", args=[u.pk]),
        "eliminar_url": reverse("usuarios:eliminar", args=[u.pk]),
        "grupos_url": reverse("usuarios:grupos_modal", args=[u.pk]),
    }


class AjaxModelFormMixin:
    ajax_template_name = None
    success_message = ""

    def form_invalid(self, form):
        if is_ajax_request(self.request) and self.ajax_template_name:
            html = render_to_string(
                self.ajax_template_name,
                self.get_context_data(form=form),
                request=self.request,
            )
            return HttpResponse(html, status=422)
        return super().form_invalid(form)

    def form_valid(self, form):
        self.object = form.save()
        if is_ajax_request(self.request):
            return JsonResponse(
                {
                    "ok": True,
                    "redirect_url": self.get_success_url(),
                    "id": self.object.pk,
                    "label": str(self.object),
                    "message": self.success_message,
                }
            )
        return redirect(self.get_success_url())


class UsuarioListView(GruposRequeridosMixin, ListView):
    model = User
    template_name = "usuarios/usuario_lista.html"
    context_object_name = "usuarios"

    def get_queryset(self):
        return User.objects.all().order_by("username")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        usuarios = list(context["usuarios"])
        context["usuarios_data"] = [_serializar_usuario(u) for u in usuarios]
        return context


@grupos_requeridos()
@require_GET
def usuarios_json(request):
    usuarios = User.objects.all().order_by("username")
    return JsonResponse({"data": [_serializar_usuario(u) for u in usuarios]})


class UsuarioCreateView(GruposRequeridosMixin, AjaxModelFormMixin, CreateView):
    model = User
    form_class = UsuarioForm
    template_name = "usuarios/usuario_modal_form.html"
    ajax_template_name = "usuarios/usuario_modal_form.html"
    success_url = reverse_lazy("usuarios:lista")
    success_message = "Usuario creado correctamente"


class UsuarioUpdateView(GruposRequeridosMixin, AjaxModelFormMixin, UpdateView):
    model = User
    form_class = UsuarioForm
    template_name = "usuarios/usuario_modal_form.html"
    ajax_template_name = "usuarios/usuario_modal_form.html"
    success_url = reverse_lazy("usuarios:lista")
    success_message = "Usuario actualizado correctamente"


@grupos_requeridos()
@require_POST
def usuario_eliminar(request, pk):
    usuario = get_object_or_404(User, pk=pk)
    nombre = str(usuario)
    usuario.delete()
    if is_ajax_request(request):
        return JsonResponse({"ok": True, "message": f"Usuario \"{nombre}\" eliminado correctamente"})
    return redirect("usuarios:lista")


@grupos_requeridos()
def usuario_grupos(request, pk):
    usuario = get_object_or_404(User, pk=pk)
    if request.method == "POST":
        form = UsuarioGruposForm(request.POST)
        if form.is_valid():
            usuario.groups.set(form.cleaned_data["groups"])
            if is_ajax_request(request):
                return JsonResponse({"ok": True, "message": "Grupos actualizados correctamente"})
            return redirect("usuarios:lista")
        if is_ajax_request(request):
            html = render_to_string("usuarios/usuario_grupos_modal.html", {"form": form, "usuario": usuario}, request=request)
            return HttpResponse(html, status=422)
    else:
        form = UsuarioGruposForm(initial={"groups": usuario.groups.all()})
    return render(request, "usuarios/usuario_grupos_modal.html", {"form": form, "usuario": usuario})
