
# Tests to be added:
Fixtures: 3 users, 3 groups, 6 perms (use auth perms)

# Without authentication: check for  (regex
# "Current user: None (authenticated: No, staff: No, superuser: No).*No data available."

# With authenticated admin superuser: "Current user: admin (authenticated: Yes, staff: Yes, superuser: Yes)
#  + no groups, no permissions via group. All permissions as personnal.
# alphabetical list identical

# With authenticated 'staff_member' user with is_staff in 3 groups, with 1, 2 ,3 permissions + no personnal perm.
# : "Current user: staff_member (authenticated: Yes, staff: Yes, superuser: No)
#  + check  groups, and perm + alphabetical list.

# With authenticated 'regular_user' user without is_staff in 2 groups, with 0 and 2 permissions + 3 personnal perms.
# : "Current user: staff_member (authenticated: Yes, staff: No, superuser: No)
#  + check  groups, and perm + alphabetical list.

# alphabetical list identical

