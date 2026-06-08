from django import forms

from .models import Medicamento


class MedicamentoForm(forms.ModelForm):
    class Meta:
        model = Medicamento
        fields = ["cum", "nombre_generico", "titular_registro", "concentracion", "activo"]
        widgets = {
            "cum": forms.TextInput(attrs={"class": "form-control", "placeholder": "Código CUM"}),
            "nombre_generico": forms.TextInput(attrs={"class": "form-control", "placeholder": "Nombre genérico"}),
            "titular_registro": forms.TextInput(attrs={"class": "form-control", "placeholder": "Titular del registro"}),
            "concentracion": forms.TextInput(attrs={"class": "form-control", "placeholder": "Concentración"}),
            "activo": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name == "activo":
                continue
            if field.required:
                field.widget.attrs["data-req"] = "true"
