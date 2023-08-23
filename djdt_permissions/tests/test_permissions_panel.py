from debug_toolbar.toolbar import DebugToolbar
from django.contrib.auth.models import User, Permission, Group
from django.http import HttpResponse
from django.test import override_settings, TestCase, RequestFactory
from django.urls import reverse


# noinspection DuplicatedCode
@override_settings(DEBUG=True)
class TestPermissionPanel(TestCase):
    databases = {'default'}
    panel = None
    rf = None
    request = None
    toolbar = None

    def setUp(self):
        # The HistoryPanel keeps track of previous stores in memory.
        # This bleeds into other tests and violates their idempotency.
        # Clear the store before each test.
        for key in list(DebugToolbar._store.keys()):
            del DebugToolbar._store[key]
        super().setUp()

        self.rf = RequestFactory()
        self.request = self.rf.get("/")
        self.toolbar = DebugToolbar(self.request, lambda request: HttpResponse())
        self.toolbar.stats = {}

        self.panel = self.toolbar.get_panel_by_id("PermissionsPanel")
        self.panel.enable_instrumentation()

    def tearDown(self):
        if self.panel:
            self.panel.disable_instrumentation()
        super().tearDown()

    def test_panel_disabled(self):
        config = {"DISABLE_PANELS": {"djdt_permissions.panels.permissions_panel.PermissionsPanel"}}
        self.assertTrue(self.panel.enabled)
        with self.settings(DEBUG_TOOLBAR_CONFIG=config):
            self.assertFalse(self.panel.enabled)

    def test_panel_title_no_authenticated_user(self):
        response = self.client.get(reverse("home"))
        self.assertContains(
            response, '<a class="PermissionsPanel" href="#" title="Permissions">Permissions</a>',
            html=True
        )
        self.assertContains(
            response,
            """            
            <div class="djdt-hidden djdt-panelContent" id="PermissionsPanel">
                <div class="djDebugPanelTitle">
                <button class="djDebugClose" type="button">
                ×
                </button><h3>
                Permissions
                </h3>
                </div>
                <div class="djDebugPanelContent">
                    <div class="djdt-scroll">
                        <p>Current user:<b>None</b>(authenticated: No, staff: No, superuser: No)</p>
                        <p>No data available.</p>
                    </div>
                </div>
                </div>
            """,
            html=True,
        )

    def test_with_superuser(self):
        my_admin = User.objects.create_superuser('test_admin', 'myemail@test.com')
        self.client.force_login(my_admin)
        response = self.client.get(reverse("home"))
        self.assertContains(
            response, """
            <p>Current user:<b>test_admin</b>(authenticated: Yes, staff: Yes, superuser: Yes)</p>
            """,
            html=True
        )
        self.assertContains(response, "Groups (0)")
        num_permissions = Permission.objects.count()
        self.assertContains(response, f"Permissions ({num_permissions})")
        self.assertContains(response,
                            f"Alphabetical list of all permissions ({num_permissions})")

    def test_with_staff_user(self):
        """ staff user, 3 groups, non overlapping, no permission granted to the user."""
        user = User.objects.create_user('test_staff', 'myemail_staff@test.com')
        user.is_staff = True
        group1 = Group(name="group1")
        group2 = Group(name="group2")
        group3 = Group(name="group3")
        group1.save()
        group2.save()
        group3.save()
        group2.permissions.add(Permission.objects.get(codename="add_user"))
        group3.permissions.add(Permission.objects.get(codename="add_group"))
        group3.permissions.add(Permission.objects.get(codename="view_group"))
        group3.permissions.add(Permission.objects.get(codename="change_group"))
        user.groups.add(group1)
        user.groups.add(group2)
        user.groups.add(group3)
        user.save()
        group1.save()
        group2.save()
        group3.save()
        self.client.force_login(user)
        response = self.client.get(reverse("home"))
        self.assertContains(
            response, """
            <p>Current user:<b>test_staff</b>(authenticated: Yes, staff: Yes, superuser: No)</p>
            """,
            html=True
        )
        self.assertContains(response, "Groups (3)")
        self.assertContains(response, "Permissions (0)")
        num_permissions = 4
        self.assertContains(response, f"Alphabetical list of all permissions ({num_permissions})")

    def test_with_regular_user(self):
        """ Regular user, 3 groups, overlapping permissions, 1 permission granted to the user."""
        user = User.objects.create_user('test_regular', 'myemail_regular@test.com')
        group1 = Group(name="group1")
        group2 = Group(name="group2")
        group3 = Group(name="group3")
        group1.save()
        group2.save()
        group3.save()
        group2.permissions.add(Permission.objects.get(codename="add_user"))
        group2.permissions.add(Permission.objects.get(codename="view_group"))
        group3.permissions.add(Permission.objects.get(codename="add_group"))
        group3.permissions.add(Permission.objects.get(codename="view_group"))
        group3.permissions.add(Permission.objects.get(codename="change_group"))
        user.groups.add(group1)
        user.groups.add(group2)
        user.groups.add(group3)
        user.user_permissions.add(Permission.objects.get(codename="view_permission"))
        user.save()
        group1.save()
        group2.save()
        group3.save()
        self.client.force_login(user)
        response = self.client.get(reverse("home"))
        self.assertContains(
            response, """
               <p>Current user:<b>test_regular</b>(authenticated: Yes, staff: No, superuser: No)</p>
               """,
            html=True
        )
        self.assertContains(response, "Groups (3)")
        self.assertContains(response, "Permissions (1)")
        num_permissions = 5
        self.assertContains(response, f"Alphabetical list of all permissions ({num_permissions})")
