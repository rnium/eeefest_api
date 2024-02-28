from django.core.exceptions import ValidationError
from fest.models import Registration
allowed_gateways = ['rocket', 'nagad', 'bkash']


def check_registration_fields(reg_data):
    if reg_data['gateway'] not in allowed_gateways:
        raise ValidationError("Ivalid Gateway")
    lengths = [len(reg_data['transaction_id']), len(reg_data['paying_number'])]
    if not all(lengths):
        raise ValidationError("Some required fields left empty")


def check_member_fields(member_data):
    lengths = [
        len(member_data['name']),
        len(member_data['inst'])
    ]
    if not all(lengths):
        raise ValidationError("Some required fields left empty")


def check_registration_data(registration_data, members_data):
    registrations_qs = Registration.objects.filter(transaction_id=registration_data['transaction_id'])
    if registrations_qs.count() > 0:
        return (False, "Transaction id already used in another registration")
    if registration_data['contest'] in ['lfr', 'poster']:
        if registration_data['group_members_count'] != len(members_data):
            return (False, "Member Count mismatch")
    else:
        if (len(members_data['group_member_1']['reg_num']) == 0):
            return (False, "Registration no. missing")
    lengths = [
        len(members_data['group_member_1']['name']),
        len(members_data['group_member_1']['inst']),
        len(members_data['group_member_1']['phone']),
    ]
    if len(members_data['group_member_1']['phone']) == 0:
        return (False, "First Member's phone no. missing")
    for m_key in members_data:
        lengths = [
            len(members_data[m_key]['name']),
            len(members_data[m_key]['inst'])
        ]
        if not all(lengths):
            return (False, f"{m_key}: Name or Institute Missing")
    return (True, "All ok")
