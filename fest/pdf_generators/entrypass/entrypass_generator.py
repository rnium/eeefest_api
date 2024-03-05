from weasyprint import HTML, CSS
from weasyprint.text.fonts import FontConfiguration
from io import BytesIO
from django.conf import settings
from django.template.loader import render_to_string
from datetime import datetime


def get_fonts_css_txt(font_names):
    css_text = ""
    for font_name in font_names.keys():
        font_path = settings.BASE_DIR/f"fest/pdf_generators/fonts/{font_names[font_name]}"
        css_text += f"""@font-face {{
                        font-family: {font_name};
                        src: url(file://{font_path});}}"""
    return css_text


def render_entrypass(registration):
    context = {}
    contest_logo = settings.BASE_DIR/f'fest/pdf_generators/images/{registration.contest}.png'
    eee_logo = settings.BASE_DIR/f'fest/pdf_generators/images/sec_eee.png'
    context['contest_logo'] = contest_logo
    context['eee_logo'] = eee_logo
    formatted_time = datetime.now().strftime("%a, %d %b %Y %H:%M:%S UTC")
    context['server_time'] = formatted_time
    context['registration'] = registration
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

