from weasyprint import HTML, CSS
from weasyprint.text.fonts import FontConfiguration
from io import BytesIO
from django.conf import settings
from django.template.loader import render_to_string
from datetime import datetime
from django.urls import reverse
import os
import qrcode


schedules = {
    'lfr': '9:00 AM, 10 March 2024',
    'poster': '10:00 AM, 10 March 2024',
    'circuit-solve': '10:15 AM, 9 March 2024',
    'integration': '11:00 AM, 9 March 2024',
    'gaming-fifa': '5:00 PM, 9 March 2024',
    'gaming-chess': '3:00 PM, 9 March 2024',
}

contest_rules = {
    'circuit-solve': [
        'Any form of cheating or plagiarism will result in immediate disqualification.',
        'Respectful and sportsmanlike conduct is expected from all participants.',
        'You can raise concerns or disputes with the judges, but it must be done in a respectful and timely manner.',
    ],
    'integration': [
        'The Integration Bee will follow a specific format. Participants are responsible for understanding the rules and the structure of the competition.',
        'Maintain a quiet and focused atmosphere. Participants are expected to respect opponents and avoid any disruptive behavior during the contest.',
        'Food and drinks are allowed in designated areas only. Please keep the contest area clean.',
        'In case of emergency, follow instructions from the Integration Bee organizers and venue staff.',
        "The decision of the judges on all matters is considered final and binding. There will be no reconsideration or review of decisions once they have been rendered."
    ],
    'gaming-chess': [
        'Fair play is paramount. Any form of cheating, including electronic devices, is strictly prohibited. Violators will be disqualified.',
        'Maintain a quiet and focused atmosphere. Participants are expected to respect opponents and refrain from any disruptive behavior.',
        'All disputes and rule clarifications will be addressed by the tournament arbiters. Their decisions are final and binding.',
        'In case of emergency, follow instructions from the tournament organizers and venue staff.',
        "The decision of the judges on all matters is considered final and binding. There will be no reconsideration or review of decisions once they have been rendered."
    ],
    'gaming-fifa': [
        'Players can bring their controller/keyboard. The player must set his own control setup for custom control.',
        "The gaming platform is 'PC'",
        'All players are required to show up at least half an hour before the tournament and report to the organizers to get their desired pc.',
        'Players not present at the designated time for any match will be disqualified, the opponent will be the winner at 3-0 scores.',
        'One button or two buttons control mode is not allowed.',
        'For any difficulties, the player must inform the referee to make any decisions.',
        'After finishing the game players have to wait until the referee finishes scoring',
        'Only scores reported by the referee are official.',
    ]
}


def get_qr_code_path(request, reg_id):
    qrcode_filepath = settings.BASE_DIR / f'media/temp/reg_{reg_id}.png'
    os.makedirs("media/temp/", exist_ok=True)
    if os.path.exists(qrcode_filepath):
        return qrcode_filepath
    link = request.build_absolute_uri(reverse('verify_registration', args=(reg_id,)))
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=1,
    )
    qr.add_data(link)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    img.save(qrcode_filepath)
    return qrcode_filepath


def get_fonts_css_txt(font_names):
    css_text = ""
    for font_name in font_names.keys():
        font_path = settings.BASE_DIR/f"fest/pdf_generators/fonts/{font_names[font_name]}"
        css_text += f"""@font-face {{
                        font-family: {font_name};
                        src: url(file://{font_path});}}"""
    return css_text


def get_member_context(registration):
    members = registration.groupmember_set.all()
    members_count = members.count()
    group_members = []
    first_member = members.first()
    if members_count == 2:
        member = list(members)[1]
        group_members.append({
            'className': 'full-width',
            'title': 'Group Member 2',
            'obj': member
        })
    elif members_count > 2:
        for idx, member in enumerate(list(members)[1:]):
            group_members.append({
                'className': 'half-width',
                'title': f'Group Member {idx+2}',
                'obj': member
            })
    context = {
        'first_member': {
            'title': "Team Leader" if members_count > 1 else "Contestant Info",
            'obj': first_member
        },
        'group_members': group_members
    }
    return context
    

def render_entrypass(request, registration):
    context = {'qrcode_path': get_qr_code_path(request, registration.id)}
    context['schedule'] = schedules.get(registration.contest, 'N/A')
    contest_logo = settings.BASE_DIR/f'fest/pdf_generators/images/{registration.contest}.png'
    eee_logo = settings.BASE_DIR/f'fest/pdf_generators/images/sec_eee.png'
    context['contest_logo'] = contest_logo
    context['eee_logo'] = eee_logo
    formatted_time = datetime.now().strftime("%a, %d %b %Y %H:%M:%S UTC")
    context['server_time'] = formatted_time
    context['registration'] = registration
    context['member_context'] = get_member_context(registration)
    context['additional_notes'] = contest_rules.get(registration.contest)
    html_text = render_to_string('fest/pdf_templates/entrypass.html', context=context)
    fonts = {
        'DoctorGlitch': 'DoctorGlitch.otf',
        'RobotoRegular': 'Roboto-Regular.ttf',
        'RobotoMedium': 'Roboto-Medium.ttf',
    }
    font_config = FontConfiguration()
    fonts_css = get_fonts_css_txt(fonts)
    css_filepath = settings.BASE_DIR/f"fest/pdf_generators/styles/entrypass.css"
    with open(css_filepath, 'r') as f:
        css_text = f.read()
    html = HTML(string=html_text)
    css = CSS(string=css_text, font_config=font_config)
    css1 = CSS(string=fonts_css, font_config=font_config)
    buffer = BytesIO()
    html.write_pdf(buffer, stylesheets=[css, css1], font_config=font_config)
    return buffer.getvalue()

