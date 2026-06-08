from django.db import migrations


def migrate_old_digitador(apps, schema_editor):
    Group = apps.get_model("auth", "Group")
    User = apps.get_model("auth", "User")

    old = Group.objects.filter(name="Digitador").first()
    new, _ = Group.objects.get_or_create(name="digitador")

    if old:
        for user in User.objects.filter(groups=old):
            user.groups.add(new)
        old.delete()


def reverse_migrate(apps, schema_editor):
    Group = apps.get_model("auth", "Group")
    User = apps.get_model("auth", "User")

    new = Group.objects.filter(name="digitador").first()
    old, _ = Group.objects.get_or_create(name="Digitador")

    if new:
        for user in User.objects.filter(groups=new):
            user.groups.add(old)


class Migration(migrations.Migration):
    dependencies = [
        ("usuarios", "0001_create_groups"),
    ]

    operations = [
        migrations.RunPython(migrate_old_digitador, reverse_migrate),
    ]
