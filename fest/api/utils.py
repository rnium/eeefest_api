from django.core.exceptions import ValidationError
allowed_gateways = ['rocket', 'nagad']

def check_registration_fields(reg_data):
    if reg_data['gateway'] not in allowed_gateways:
        raise ValidationError("Ivalid Gateway")
    lengths = [len(reg_data['transaction_id']), len(reg_data['paying_number'])]
    if not all(lengths):
        raise ValidationError("Some required fields left empty")
    
def check_member_fields(member_data):
    lengths = [
        len(member_data['name']), 
        len(member_data['inst']),
        len(member_data['dept']),
        len(member_data['phone']),
    ]
    if not all(lengths):
        raise ValidationError("Some required fields left empty")
    
def check_registration_data(formdata, members_data):
    check_registration_data(formdata)
    num_members = int(formdata['group_members_count'])
    members_with_data = []
    