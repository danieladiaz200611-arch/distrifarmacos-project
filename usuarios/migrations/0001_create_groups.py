from django.db import migrations


def create_groups(apps, schema_editor):
    Group = apps.get_model("auth", "Group")
    Permission = apps.get_model("auth", "Permission")
    ContentType = apps.get_model("contenttypes", "ContentType")

    FormulaBase = apps.get_model("radicacion", "FormulaBase")
    FormulaBaseTecnologia = apps.get_model("radicacion", "FormulaBaseTecnologia")
    SoporteFormulaBase = apps.get_model("radicacion", "SoporteFormulaBase")

    formula_ct = ContentType.objects.get_for_model(FormulaBase)
    tecnologia_ct = ContentType.objects.get_for_model(FormulaBaseTecnologia)
    soporte_ct = ContentType.objects.get_for_model(SoporteFormulaBase)

    all_formula_perms = Permission.objects.filter(
        content_type__in=[formula_ct, tecnologia_ct, soporte_ct]
    )

    view_formula_perms = Permission.objects.filter(
        content_type__in=[formula_ct, tecnologia_ct, soporte_ct],
        codename__startswith="view_",
    )

    dig_group, _ = Group.objects.get_or_create(name="digitador")
    dig_group.permissions.set(all_formula_perms)

    gc_group, _ = Group.objects.get_or_create(name="gestor_calidad")
    gc_group.permissions.set(view_formula_perms)


def remove_groups(apps, schema_editor):
    Group = apps.get_model("auth", "Group")
    Group.objects.filter(name__in=["digitador", "gestor_calidad"]).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("radicacion", "0006_delete_detalleregistrocontrato"),
    ]

    operations = [
        migrations.RunPython(create_groups, remove_groups),
    ]
