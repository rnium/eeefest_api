from django.urls import reverse
from fest.models import Registration
import base64
from django.template.loader import render_to_string
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from django.conf import settings
from django.core.exceptions import ValidationError


sendgrid_api_key = settings.SENDGRID_API_KEY_1




def send_html_email(receiver, subject, body):
    message = Mail(
        from_email=('seceeefest2k24@gmail.com', "TechnoVenture3.0"),
        to_emails=receiver,
        subject=subject,
        html_content=body)
    
    sg = SendGridAPIClient(sendgrid_api_key)
    response = sg.send(message)
    status = response.status_code
    if status >= 400:
        raise ValidationError("API Error")




def send_confirmation_email(baseUrl, registration):
    email_subject = "Confirmation of Contest Registration and Entry Pass Download Link"
    all_members = registration.groupmember_set.all().order_by('id')
    receiver = None
    member_name = ""
    for member in all_members:
        if mail_id:=member.email:
            receiver = mail_id
            member_name = member.name
            break
    reg_code = get_encoded_reg_id(registration)
    link = baseUrl + reverse('download_entrypass', args=(reg_code,))
    email_body = render_to_string('fest/email/reg_confirmation.html', context={
        "member_name": member_name,
        "contest": registration.get_contest_display(),
        "entrypass_url": link,
    })
    send_html_email(receiver, email_subject, email_body)
    
    
def send_deletion_notification_email(registration, reason):
    email_subject = "Contest Registration Deletion Notification"
    all_members = registration.groupmember_set.all().order_by('id')
    receiver = None
    member_name = ""
    for member in all_members:
        if mail_id:=member.email:
            receiver = mail_id
            member_name = member.name
            break
    
    email_body = render_to_string('fest/email/reg_deletion.html', context={
        "member_name": member_name,
        "contest_name": registration.get_contest_display(),
        "reg_id": registration.id,
        "reason": reason,
    })
    send_html_email(receiver, email_subject, email_body)
        

def get_encoded_reg_id(reg: Registration):
    raw_str = f"{reg.id}-{reg.contest}"
    encoded = base64.b64encode(raw_str.encode())
    return encoded.decode(encoding="utf-8")


def get_decoded_reg_id(code):
    decoded = base64.b64decode(code.encode())
    text = decoded.decode()
    reg_id = int(text.split("-")[0])
    return reg_id


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
    header = ["SL", 'Applied at', 'Contest', 'Approval Status',
              'Team Name', 'Total Members', 'Team Leader']
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
            if reg_num := member.reg_num:
                info += f" Registration No.{reg_num},"
            if dept := member.dept:
                info += f" Department: {dept},"
            if tshirt := member.tshirt:
                info += f" Tshirt: {tshirt.upper()},"
            if phone := member.phone:
                info += f" Phone: {phone},"
            if email := member.email:
                info += f" Email: {email.lower()})"
            if reg.contest == 'gaming-fifa':
                if member.game_controller:
                    info += f" Controller: {member.get_game_controller_display()})"
                else:
                    info += f" Controller: <Not Selected>"
            unit_data.append(info)
        data.append(unit_data)
    header.extend([f"Group Member {i+1}" for i in range(1, max_members)])
    data.insert(0, header)
    return data


def get_individual_type_excel_data(contest, approval):
    registrations = list(get_registrations_queryset(contest, approval))
    data = []
    header = ["SL", 'Applied at', 'Contest',
              'Approval status', 'Contestant Info']
    for index, reg in enumerate(registrations):
        unit_data = [index+1]
        unit_data.append(reg.added_at.strftime("%Y-%m-%d %H:%M:%S"))
        unit_data.append(reg.contest)
        unit_data.append("Approved" if reg.is_approved else "Pending")
        member = reg.groupmember_set.all().first()
        info = member.name.title()
        info += f" ({member.inst},"
        if reg_num := member.reg_num:
            info += f" Registration No.{reg_num},"
        if dept := member.dept:
            info += f" Department: {dept},"
        if phone := member.phone:
            info += f" Phone: {phone},"
        if email := member.email:
            info += f" Email: {email.lower()})"
        if reg.contest == 'gaming-fifa':
            if member.game_controller:
                info += f" Controller: {member.get_game_controller_display()})"
            else:
                info += f" Controller: <Not Selected>"
        unit_data.append(info)
        data.append(unit_data)
    data.insert(0, header)
    return data
