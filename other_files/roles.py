from rolepermissions.roles import AbstractUserRole


class Candidate(AbstractUserRole):
    available_permissions = {
        "all_access":True,
    }


class Employer(AbstractUserRole):
    available_permissions = {
        "all_access": True,

    }
