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

