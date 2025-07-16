import enum

class UserRoleEnum(enum.Enum):
    admin = 'admin'
    team_lead = 'team_lead'
    employee = 'employee'
    salesman = 'salesman'