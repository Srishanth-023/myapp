from django.contrib.auth.models import Group, Permission

def create_groups_and_permissions(sender, **kwargs):
    try:
        # CREATE GROUPS
        readers_group, created = Group.objects.get_or_create(name = "Readers")
        authors_group, created = Group.objects.get_or_create(name = "Authors")
        editors_group, created = Group.objects.get_or_create(name = "Editors")

        # CREATING PERMISSIONS
        # READERS GROUP
        readers_permissions = [
            Permission.objects.get(codename = "view_post")
        ]
        # AUTHORS GROUP
        authors_permissions = [
            Permission.objects.get(codename = "add_post"),
            Permission.objects.get(codename = "change_post"),
            Permission.objects.get(codename = "delete_post"),
        ]
        # EDITORS GROUP
        can_publish, created = Permission.objects.get_or_create(codename = "publish_post", content_type_id = 7, name = "Can publish post")
        editors_permissions = [
            can_publish,
            Permission.objects.get(codename = "add_post"),
            Permission.objects.get(codename = "change_post"),
            Permission.objects.get(codename = "delete_post"),
        ]

        # ASSIGNING PERMISSIONS TO GROUPS
        readers_group.permissions.set(readers_permissions)
        authors_group.permissions.set(authors_permissions)
        editors_group.permissions.set(editors_permissions)

        print("Success 🐦‍🔥")

    except Exception as e:
        print(f"An error occured : {e}")