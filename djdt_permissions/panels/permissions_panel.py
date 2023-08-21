from debug_toolbar.panels import Panel
from django.utils.translation import gettext_lazy as _


class PermissionsPanel(Panel):
    name = 'Permissions'
    template = "djdt_permissions/permissions_panel.html"
    has_content = True

    def __init__(self, toolbar, get_response):
        self.request = None
        super().__init__(toolbar, get_response)

    def nav_title(self):
        return _('Permissions')

    def title(self):
        return _('Permissions')

    def process_request(self, request):
        self.request = request
        # At this stage, the request has no user information, just collect the reference.
        return super().process_request(request)

    @property
    def content(self):
        # At this stage, the request has user information.
        data = {
            'groups': {},
        }
        if not hasattr(self.request, 'user'):
            data['username'] = "None"
            data['user_descriptor']: ""
            data['data_available'] = False
        else:
            user = self.request.user
            data['username'] = user.username if user.username else "None"
            data['user_descriptor'] = (f"(authenticated: {'Yes' if user.is_authenticated else 'No'}, "
                                       f"staff: {'Yes' if user.is_staff else 'No'}, "
                                       f"superuser: {'Yes' if user.is_superuser else 'No'})")
            data['data_available'] = user.is_authenticated
            data['groups'], data['num_groups'] = self.collect_user_perms_and_groups(self.request)
            data['personal_permissions'], data['num_personal_permissions'] = (
                self.collect_personal_permissions(self.request))
            data['all_permissions'], data['total_num_permissions'] = (
                self.collect_all_permissions(self.request))

        self.record_stats(data)
        return super().content

    # noinspection PyUnusedLocal
    @classmethod
    def collect_user_perms_and_groups(cls, request) -> ([], int):
        """ Collect all permissions owned by the current user through group membership in a dictionary.
        :return: A list of dictionaries (one per group).
        :return: The number of groups.
        """
        result = []
        user = request.user
        count = 0
        for grp in user.groups.all().order_by("name"):
            data = {'name': grp.name, 'id': grp.pk, 'permissions': []}
            count += 1
            perm_count = 0
            for p in grp.permissions.all().order_by("content_type__app_label", "codename"):
                perm_count += 1
                data['permissions'].append({"code": f"{p.content_type.app_label}.{p.codename}", "name": p.name})
            data['num_permissions'] = perm_count
            result.append(data)
        return result, count

    # noinspection PyUnusedLocal
    @classmethod
    def collect_personal_permissions(cls, request) -> ([], int):
        """ Collect all permissions owned personally by the current user in a dictionary.
        :return: A list of dictionaries (one per permission).
        :return: The number of permissions.
        """
        # user.get_user_permissions() return a set. Could be more efficient to query models directly?
        my_list = list(request.user.get_user_permissions())
        my_list.sort()
        data = []
        for p in my_list:
            data.append(p)
        return data, len(my_list)

    # noinspection PyUnusedLocal
    @classmethod
    def collect_all_permissions(cls, request) -> ([], int):
        """ Collect all permissions owned by the current user in a dictionary.
        :return: A list of dictionaries (one per permission).
        :return: The total number of permissions.
        """
        # user.get_all_permissions() return a set. Could be more efficient to query models directly?
        my_list = list(request.user.get_all_permissions())
        my_list.sort()
        data = []
        for p in my_list:
            data.append(p)

        return data, len(my_list)
