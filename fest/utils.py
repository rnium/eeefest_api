from fest.models import Registration

def get_registrations_queryset(contest, approval):
    registrations = None
    if contest == 'all':
        if approval == 'all':
            registrations = Registration.objects.all()
        elif approval == 'approved':
            registrations = Registration.objects.filter(is_approved=True)
        else:
            registrations = Registration.objects.filter(is_approved=False)
    else:
        if approval == 'all':
            registrations = Registration.objects.filter(contest=contest)
        elif approval == 'approved':
            registrations = Registration.objects.filter(
                contest=contest, is_approved=True)
        else:
            registrations = Registration.objects.filter(
                contest=contest, is_approved=False)
    if registrations != None:
        registrations = registrations.order_by('is_approved', '-added_at')
    return registrations

def get_group_type_excel_data(contest, approval):
    registrations = list(get_registrations_queryset(contest, approval))
    data = []
    header = ["SL", 'Applied at', 'Contest', 'Approval Status', 'Team Name', 'Total Members', 'Team Leader']
    max_members = 1
    for index, reg in enumerate(registrations):
        unit_data = [index+1]
        unit_data.append(reg.added_at.strftime("%Y-%m-%d %H:%M:%S"))
        unit_data.append(reg.contest)
        unit_data.append("Approved" if reg.is_approved else "Pending")
        unit_data.append(reg.team_name)
        unit_data.append(reg.group_members_count)
        group_members_qs = reg.groupmember_set.all()
        max_members = max(max_members, group_members_qs.count())
        for member in group_members_qs:
            info = member.name.title()
            info += f" ({member.inst},"
            if reg_num:=member.reg_num:
                info += f" Registration No.{reg_num},"
            if dept:=member.dept:
                info += f" Department: {dept},"
            if tshirt:=member.tshirt:
                info += f" Tshirt: {tshirt.upper()},"
            if phone:=member.phone:
                info += f" Phone: {phone},"
            if email:=member.email:
                info += f" Email: {email.lower()})"
            unit_data.append(info)
        data.append(unit_data)
    header.extend([f"Group Member {i+1}" for i in range(1, max_members)])
    data.insert(0, header)
    return data


def get_individual_type_excel_data(contest, approval):
    registrations = list(get_registrations_queryset(contest, approval))
    data = []
    header = ["SL", 'Applied at', 'Contest', 'Approval status', 'Contestant Info']
    for index, reg in enumerate(registrations):
        unit_data = [index+1]
        unit_data.append(reg.added_at.strftime("%Y-%m-%d %H:%M:%S"))
        unit_data.append(reg.contest)
        unit_data.append("Approved" if reg.is_approved else "Pending")
        member = reg.groupmember_set.all().first()
        info = member.name.title()
        info += f" ({member.inst},"
        if reg_num:=member.reg_num:
            info += f" Registration No.{reg_num},"
        if dept:=member.dept:
            info += f" Department: {dept},"
        if phone:=member.phone:
            info += f" Phone: {phone},"
        if email:=member.email:
            info += f" Email: {email.lower()})"
        unit_data.append(info)
        data.append(unit_data)
    data.insert(0, header)
    return data
        
      
