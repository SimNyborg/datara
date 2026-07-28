from flask import Flask, abort, render_template, send_from_directory, request, redirect, Response
from datetime import datetime
from urllib.parse import urljoin, urlparse

from site_content import CONTENT_UI, INFO_PAGES, SERVICE_PAGES

app = Flask(__name__)


@app.after_request
def add_security_headers(response):
    """Add conservative headers that do not interfere with the existing site."""
    response.headers.setdefault('X-Content-Type-Options', 'nosniff')
    response.headers.setdefault('Referrer-Policy', 'strict-origin-when-cross-origin')
    response.headers.setdefault('X-Frame-Options', 'SAMEORIGIN')
    response.headers.setdefault('Content-Security-Policy', "frame-ancestors 'self'")
    response.headers.setdefault(
        'Permissions-Policy',
        'camera=(), microphone=(), geolocation=()',
    )
    return response

# Simple translations for navbar and major UI strings
translations = {
    'da': {
        'nav_projekter': 'Projekter',
        'nav_services': 'Services',
        'nav_om': 'Om os',
        'nav_kontakt': 'Kontakt',
        'hero_h1': 'Mindre manuelt arbejde. Bedre beslutninger.',
        'hero_p': 'Vi automatiserer arbejdsgange, analyserer data og bygger digitale løsninger, der passer til jeres hverdag.',
        'projects_h2': 'Vores projekter',
        'projects_subheading': 'Her er nogle af de opgaver, vi har løst med data, automatisering og software.',
        'services_h2': 'Det hjælper vi med',
        'services_subheading': 'Vi tager udgangspunkt i jeres arbejdsgange og bygger kun det, der gør en konkret forskel.',
        'founders_h2': 'Om Datara',
        'contact_h2': 'Kontakt os',
        'contact_description': 'Har I en opgave, vi skal se på – eller et spørgsmål? Ring, skriv eller find os på LinkedIn.',
        'newsletter_label': 'Tilmeld nyhedsbrev',
        'newsletter_button': 'Tilmeld',
        'breadcrumb_back': '← Tilbage',
        'lang_code': 'da'
    },
    'en': {
        'nav_projekter': 'Projects',
        'nav_services': 'Services',
        'nav_om': 'About us',
        'nav_kontakt': 'Contact',
        'hero_h1': 'Less manual work. Better decisions.',
        'hero_p': 'We automate workflows, analyse data and build digital tools that fit the way you work.',
        'projects_h2': 'Our projects',
        'projects_subheading': 'A few examples of how we have used data, automation and software to solve real tasks.',
        'services_h2': 'What we can help with',
        'services_subheading': 'We start with the way you work and build only what makes a practical difference.',
        'founders_h2': 'About Datara',
        'contact_h2': 'Contact us',
        'contact_description': 'Have a task you would like us to look at, or simply a question? Call, email or find us on LinkedIn.',
        'newsletter_label': 'Subscribe to our newsletter',
        'newsletter_button': 'Subscribe',
        'breadcrumb_back': '← Back',
        'lang_code': 'en'
    }
}


def current_language():
    lang = request.cookies.get('site_lang', 'da')
    return lang if lang in translations else 'da'


@app.context_processor
def inject_strings():
    lang = current_language()
    strings = translations.get(lang, translations['da'])
    return dict(strings=strings, footer_ui=CONTENT_UI[lang])

# Favicons are served from the project's `static/` folder and referenced
# in templates using `url_for('static', filename=...)`. No explicit routes
# are required here.

# Serve favicon.ico from the `static/` folder (canonical location for static assets)
@app.route('/favicon.ico')
def favicon():
    return send_from_directory('static', 'favicon.ico')


@app.route('/setlang/<lang>')
def set_language(lang):
    target = request.referrer or '/'
    host = urlparse(request.host_url)
    resolved = urlparse(urljoin(request.host_url, target))
    if resolved.scheme not in ('http', 'https') or resolved.netloc != host.netloc:
        target = '/'

    resp = redirect(target)
    if lang in translations:
        resp.set_cookie(
            'site_lang',
            lang,
            max_age=30 * 24 * 3600,
            samesite='Lax',
            secure=request.is_secure,
        )
    return resp
@app.route('/')
def index():
    return render_template('index.html', year=datetime.now().year)

@app.route('/founder/simon-nyborg')
@app.route('/founder/albert-koba')
def retired_founder_profiles():
    """Keep old bookmarks useful without maintaining separate profile pages."""
    return redirect('/#hvemervi', code=301)

# Footer info pages
@app.route('/privatliv')
def privatliv():
    return render_info_page('privatliv')

@app.route('/cookies')
def cookies():
    return render_info_page('cookies')

@app.route('/vilkar')
def vilkar():
    return render_info_page('vilkar')


def render_info_page(slug):
    lang = current_language()
    info = INFO_PAGES[slug]
    return render_template(
        'info.html',
        page=info['content'][lang],
        lang=lang,
        alternate_lang='en' if lang == 'da' else 'da',
        ui=CONTENT_UI[lang],
        year=datetime.now().year,
    )

# Service pages
@app.route('/services/dataanalyse')
def service_dataanalyse():
    return render_service_page('dataanalyse')

@app.route('/services/forretningsudvikling')
def service_forretningsudvikling():
    return render_service_page('forretningsudvikling')

@app.route('/services/automatisering')
def service_automatisering():
    return render_service_page('automatisering')

@app.route('/services/it-produktudvikling')
def service_it_produktudvikling():
    return render_service_page('it-produktudvikling')


def render_service_page(slug):
    lang = current_language()
    entry = SERVICE_PAGES[slug]
    service = {
        'slug': slug,
        **entry['content'][lang],
    }
    return render_template(
        'service.html',
        service=service,
        lang=lang,
        alternate_lang='en' if lang == 'da' else 'da',
        ui=CONTENT_UI[lang],
        year=datetime.now().year,
    )

# Published project cases. Shared media lives at the project level, while all
# visible copy is kept in the selected language to prevent the two versions
# from drifting apart.
PROJECTS = {
    1: {
        'slug': 'automatisering',
        'image': 'brugerundersøgelse forside.jpg',
        'image_width': 1536,
        'image_height': 1205,
        'content': {
            'da': {
                'seo_title': 'Automatisering af papirspørgeskemaer | Datara',
                'meta_description': '8.000 papirskemaer blev til et færdigt datasæt med mere end 90 procent mindre tastearbejde.',
                'eyebrow': 'Automatisering',
                'title': 'Fra papirskema til færdigt datasæt',
                'lead': 'Undersøgelsen gav 8.000 papirbesvarelser – og omkring 80 timers tastearbejde. Vi beholdt indsamlingsmetoden og automatiserede resten.',
                'image_alt': 'Brugerundersøgelse med papirskemaer på en genbrugsplads',
                'sections': [
                    {
                        'title': 'Papiret fungerede fint',
                        'paragraphs': [
                            'Et affaldsselskab gennemførte en brugerundersøgelse på mere end ti genbrugspladser og samlede i alt 8.000 skemaer ind. Papirskemaerne fungerede godt: De var nemme at dele ud, kunne bruges udendørs og gav mange svar.',
                            'Udfordringen kom bagefter: Hvert kryds og hver håndskrevet kommentar skulle tastes i Excel. Det tog omkring en time for 100 skemaer, så 8.000 skemaer svarede til cirka 80 timers manuelt tastearbejde.',
                        ],
                    },
                    {
                        'title': 'Skemaerne blev læst automatisk',
                        'paragraphs': [
                            'Vi byggede et program, der arbejder med de indscannede skemaer. Det finder markeringerne, aflæser de håndskrevne kommentarer og samler svarene i et struktureret Excel-ark.',
                        ],
                    },
                    {
                        'title': '80 timer blev til under syv',
                        'paragraphs': [
                            'Programmet kunne behandle 100 skemaer på cirka fem minutter. For 8.000 skemaer reducerede det selve tastearbejdet fra cirka 80 timer til under syv – en tidsbesparelse på mere end 90 procent.',
                            'Da dataene var på plads, analyserede vi svarene og lavede en rapport for hver genbrugsplads med klare grafer og en sammenligning med den forrige undersøgelse.',
                        ],
                    },
                ],
                'stats_title': 'Kort fortalt',
                'stats': [
                    {'value': '10+', 'label': 'genbrugspladser'},
                    {'value': '8.000', 'label': 'skemaer i alt'},
                    {'value': 'ca. 5 min.', 'label': 'pr. 100 skemaer'},
                    {'value': 'over 90 %', 'label': 'mindre tastearbejde'},
                ],
                'gallery_title': 'Fra skema til rapport',
                'gallery_intro': 'Billederne følger forløbet fra de udfyldte papirskemaer til Excel-arket og den færdige rapport.',
                'gallery': [
                    {
                        'filename': 'spørgeskema i kurv.jpg',
                        'alt': 'Udfyldte papirspørgeskemaer samlet i en kurv',
                        'caption': 'De udfyldte skemaer blev samlet ind og scannet.',
                        'width': 1536,
                        'height': 2048,
                    },
                    {
                        'filename': 'spørgeskema.jpg',
                        'alt': 'Et udfyldt spørgeskema fra brugerundersøgelsen',
                        'caption': 'Programmet fandt markeringer og håndskrevne kommentarer på hvert skema.',
                        'width': 1421,
                        'height': 2049,
                    },
                    {
                        'filename': 'Excel brugerundersøgelse output.png',
                        'alt': 'Svar fra brugerundersøgelsen samlet i et Excel-ark',
                        'caption': 'Svarene blev samlet i et struktureret Excel-ark.',
                        'width': 2843,
                        'height': 1470,
                    },
                    {
                        'filename': 'graf brugerundersøgelse.png',
                        'alt': 'Graf med et resultat fra brugerundersøgelsen',
                        'caption': 'Den færdige rapport viste resultaterne i enkle grafer.',
                        'width': 2253,
                        'height': 1207,
                    },
                ],
                'cta_title': 'Tager en gentagen opgave for lang tid?',
                'cta_text': 'Vi ser gerne på arbejdsgangen og vurderer, hvad der faktisk kan automatiseres.',
                'cta_label': 'Fortæl os om opgaven',
            },
            'en': {
                'seo_title': 'Automating paper questionnaires | Datara',
                'meta_description': '8,000 paper forms became a finished dataset with more than 90% less manual data entry.',
                'eyebrow': 'Automation',
                'title': 'From paper form to finished dataset',
                'lead': 'The survey produced 8,000 paper responses – and around 80 hours of manual data entry. We kept the collection method and automated the rest.',
                'image_alt': 'Paper-based user survey at a recycling site',
                'sections': [
                    {
                        'title': 'Paper worked well',
                        'paragraphs': [
                            'A waste company ran a user survey across more than ten recycling sites and collected 8,000 forms in total. Paper forms worked well: They were easy to hand out, worked outdoors and produced a strong response.',
                            'The problem came afterwards. Every answer had to be entered into Excel, tick by tick and comment by comment. At about one hour per 100 forms, all 8,000 amounted to roughly 80 hours of manual data entry.',
                        ],
                    },
                    {
                        'title': 'The forms were read automatically',
                        'paragraphs': [
                            'We built a program for the scanned forms. It locates the marked boxes, reads the handwritten comments and puts the responses into a structured Excel file.',
                        ],
                    },
                    {
                        'title': '80 hours were cut to under seven',
                        'paragraphs': [
                            'The software could process 100 forms in about five minutes. Across all 8,000 forms, it cut the data-entry work from roughly 80 hours to under seven – a saving of more than 90%.',
                            'With the data ready, we analysed the responses and produced a report for each recycling site, using clear charts and a comparison with the previous survey.',
                        ],
                    },
                ],
                'stats_title': 'At a glance',
                'stats': [
                    {'value': '10+', 'label': 'recycling sites'},
                    {'value': '8,000', 'label': 'forms in total'},
                    {'value': 'about 5 min', 'label': 'per 100 forms'},
                    {'value': 'over 90%', 'label': 'less data entry'},
                ],
                'gallery_title': 'From form to report',
                'gallery_intro': 'The images follow the work from the completed paper forms to the Excel file and final report.',
                'gallery': [
                    {
                        'filename': 'spørgeskema i kurv.jpg',
                        'alt': 'Completed paper questionnaires collected in a basket',
                        'caption': 'The completed forms were collected and scanned.',
                        'width': 1536,
                        'height': 2048,
                    },
                    {
                        'filename': 'spørgeskema.jpg',
                        'alt': 'A completed questionnaire from the user survey',
                        'caption': 'The software found marked boxes and handwritten comments on each form.',
                        'width': 1421,
                        'height': 2049,
                    },
                    {
                        'filename': 'Excel brugerundersøgelse output.png',
                        'alt': 'User survey responses collected in an Excel workbook',
                        'caption': 'The responses were gathered in a structured Excel workbook.',
                        'width': 2843,
                        'height': 1470,
                    },
                    {
                        'filename': 'graf brugerundersøgelse.png',
                        'alt': 'Chart showing a result from the user survey',
                        'caption': 'The final report presented the results in clear charts.',
                        'width': 2253,
                        'height': 1207,
                    },
                ],
                'cta_title': 'Is a repetitive task taking too long?',
                'cta_text': 'We can review the workflow and tell you what is worth automating.',
                'cta_label': 'Tell us about the task',
            },
        },
    },
    2: {
        'slug': 'lavtemperaturfjernvarme',
        'image': 'fjernvarme-resultatkort.png',
        'image_width': 1280,
        'image_height': 720,
        'content': {
            'da': {
                'seo_title': 'Kortlægning af lavtemperaturfjernvarme | Datara',
                'meta_description': 'Vi screenede 12.592 bygninger i Lyngby-Taarbæk og samlede resultatet i et kort til den tidlige planlægning af lavtemperaturfjernvarme.',
                'eyebrow': 'Fagprojekt · Lyngby-Taarbæk',
                'title': 'Hvor kan fjernvarme ved lav temperatur fungere?',
                'lead': 'Hvilke bygninger kan klare fjernvarme ved en lavere temperatur? Og hvor findes der virksomheder med varme til overs? Projektet samlede svarene i et kort til den tidlige varmeplanlægning.',
                'image_alt': 'Resultatkort over bygningers potentiale for lavtemperaturfjernvarme i Lyngby-Taarbæk',
                'image_caption': 'Blandt analysens 12.592 bygninger viser grøn højt potentiale, gul muligt potentiale efter forbedringer og rød lavt potentiale for at modtage lavtemperaturfjernvarme.',
                'sections': [
                    {
                        'title': 'Bygningsdata samlet ét sted',
                        'paragraphs': [
                            'Projektet blev gennemført af en gruppe på tre med Lyngby-Taarbæk Kommune som case. Gruppen samlede BBR-oplysninger, energimærker, forventet årsforbrug fra Gasportalen og data om det eksisterende fjernvarmenet.',
                            'Når forbruget manglede, blev det estimeret med en statistisk model. For bygninger uden energimærke estimerede en separat model, om mærket var B eller bedre. Derefter blev 12.592 bygninger vurderet ud fra opførelsesår, varmeforbrug pr. kvadratmeter og energimærke.',
                        ],
                    },
                    {
                        'title': 'Hvad kortet viste',
                        'paragraphs': [
                            'Screeningen placerede 1.922 bygninger i kategorien højt potentiale. 6.554 kan være relevante efter forbedringer, mens 4.051 blev vurderet til lavt potentiale. 65 blev udeladt, fordi datagrundlaget ikke var godt nok.',
                            'Resultaterne blev samlet i et interaktivt kort, så mønstre kan ses og sammenholdes med det nuværende ledningsnet.',
                        ],
                    },
                    {
                        'title': 'Overskudsvarme i nærheden',
                        'paragraphs': [
                            'På forsyningssiden blev 78 CVR-registrerede virksomheder screenet som mulige kilder til overskudsvarme med EnergyMAPS-data fra Varmeplan Danmark 2021. Værdierne ved de tre temperaturniveauer er modelberegnede og skal følges op med målinger, teknik, økonomi og dialog med virksomhederne.',
                        ],
                    },
                    {
                        'title': 'Et sted at begynde',
                        'paragraphs': [
                            'Lavere temperatur i fjernvarmenettet kan mindske varmetabet og gøre flere lokale varmekilder brugbare. Kortet samler screeningens resultater og giver et fælles udgangspunkt for de næste undersøgelser.',
                        ],
                    },
                ],
                'stats_title': 'Resultatet',
                'stats': [
                    {'value': '12.592', 'label': 'bygninger i analysen'},
                    {'value': '1.922', 'label': 'med højt potentiale'},
                    {'value': '6.554', 'label': 'mulige efter forbedringer'},
                    {'value': '78', 'label': 'virksomheder screenet'},
                ],
                'gallery_title': 'Resultaterne på kort',
                'gallery_intro': 'To kort viser, hvor en nærmere undersøgelse kan begynde.',
                'gallery': [
                    {
                        'filename': 'fjernvarme-vejkort.png',
                        'alt': 'Vejkort med grønne, gule og røde vejstrækninger i Lyngby-Taarbæk',
                        'title': 'Fra bygninger til veje',
                        'description': 'Bygningsresultaterne blev samlet på vejstrækninger, så sammenhængende områder er lettere at få øje på.',
                        'caption': 'Grønne veje har kun bygninger med højt eller muligt potentiale. Gule veje har højst 10 procent med lavt potentiale; røde veje har mere end 10 procent.',
                        'width': 1280,
                        'height': 720,
                        'featured': True,
                    },
                    {
                        'filename': 'fjernvarme-overskudsvarmekilder.png',
                        'alt': 'Kort over ti steder i Lyngby-Taarbæk udvalgt til nærmere undersøgelse som mulige kilder til overskudsvarme',
                        'title': 'Mulige kilder til overskudsvarme',
                        'description': 'Udvælgelsen kombinerede EnergyMAPS-data, kommunens energiplan og en visuel vurdering af køleanlæg.',
                        'caption': 'De ti markerede steder er kandidater til en nærmere lokal undersøgelse.',
                        'width': 1796,
                        'height': 924,
                    },
                ],
                'cta_title': 'Ligger jeres data spredt?',
                'cta_text': 'Vi hjælper med at samle, kontrollere og forklare data, så næste skridt bliver lettere at vælge.',
                'cta_label': 'Tal med os om jeres data',
            },
            'en': {
                'seo_title': 'Mapping low-temperature district heating | Datara',
                'meta_description': 'We screened 12,592 buildings in Lyngby-Taarbæk and mapped the results for early-stage low-temperature district-heating planning.',
                'eyebrow': 'Student project · Lyngby-Taarbæk',
                'title': 'Where could low-temperature district heating work?',
                'lead': 'Which buildings can be heated at a lower temperature, and where might local businesses have surplus heat to share? The project brought both sides together in a map for early-stage heat planning.',
                'image_alt': 'Results map of buildings assessed for low-temperature district heating in Lyngby-Taarbæk',
                'image_caption': 'Among the 12,592 buildings in the analysis, green shows high potential, yellow possible potential after improvements and red low potential for low-temperature district heating.',
                'sections': [
                    {
                        'title': 'Building data in one place',
                        'paragraphs': [
                            'The three-person project focused on Lyngby-Taarbæk Municipality. The team combined building-register data, energy labels, expected annual consumption from Gasportalen and data on the existing district-heating network.',
                            'Where consumption data was missing, it was estimated with a statistical model. For buildings without an energy label, a separate model estimated whether the rating was B or better. The project then assessed 12,592 buildings using their age, heat consumption per square metre and energy label.',
                        ],
                    },
                    {
                        'title': 'What the map showed',
                        'paragraphs': [
                            'The screening placed 1,922 buildings in the high-potential category. A further 6,554 may be suitable after improvements, while 4,051 were rated as low potential. Another 65 were excluded because the data was insufficient.',
                            'The results were brought together in an interactive map, making it possible to see patterns in relation to the current pipe network.',
                        ],
                    },
                    {
                        'title': 'Surplus heat nearby',
                        'paragraphs': [
                            'On the supply side, 78 registered businesses were screened as possible sources of surplus heat using EnergyMAPS data from the Danish report Varmeplan Danmark 2021. The values across the three temperature ranges are modelled and need to be followed up with measurements, technical work, financial analysis and conversations with the businesses.',
                        ],
                    },
                    {
                        'title': 'A place to start',
                        'paragraphs': [
                            'Lower network temperatures can reduce heat loss and make more local heat sources useful. The map brings the screening results into one view and provides a shared starting point for the next round of work.',
                        ],
                    },
                ],
                'stats_title': 'The result',
                'stats': [
                    {'value': '12,592', 'label': 'buildings assessed'},
                    {'value': '1,922', 'label': 'with high potential'},
                    {'value': '6,554', 'label': 'possible after improvements'},
                    {'value': '78', 'label': 'businesses screened'},
                ],
                'gallery_title': 'The results on the map',
                'gallery_intro': 'Two maps show where a closer assessment could begin.',
                'gallery': [
                    {
                        'filename': 'fjernvarme-vejkort.png',
                        'alt': 'Street map with green, yellow and red sections in Lyngby-Taarbæk',
                        'title': 'From buildings to streets',
                        'description': 'The building-level results were grouped by street, making continuous areas easier to spot.',
                        'caption': 'Green streets contain only buildings with high or possible potential. Yellow streets have no more than 10% in the low-potential group; red streets have more than 10%.',
                        'width': 1280,
                        'height': 720,
                        'featured': True,
                    },
                    {
                        'filename': 'fjernvarme-overskudsvarmekilder.png',
                        'alt': 'Map of ten sites in Lyngby-Taarbæk selected for closer investigation as potential sources of surplus heat',
                        'title': 'Potential sources of surplus heat',
                        'description': 'The selection combined EnergyMAPS data, the municipal energy plan and a visual review of cooling systems.',
                        'caption': 'The ten marked sites are candidates for closer local investigation.',
                        'width': 1796,
                        'height': 924,
                    },
                ],
                'cta_title': 'Is your data spread across several sources?',
                'cta_text': 'We bring data together, check it and explain it clearly, making the next step easier to choose.',
                'cta_label': 'Talk to us about your data',
            },
        },
    },
}

PROJECT_UI = {
    'da': {
        'skip_label': 'Gå til artiklen',
        'nav_label': 'Projektmenu',
        'home_label': 'Gå til Datara-forsiden',
        'all_projects': 'Projekter',
        'language_short': 'EN',
        'language_label': 'Læs siden på engelsk',
        'back_label': 'Tilbage til projekter',
        'rights': 'Alle rettigheder forbeholdes.',
        'privacy': 'Privatliv',
        'terms': 'Vilkår',
    },
    'en': {
        'skip_label': 'Skip to the article',
        'nav_label': 'Project navigation',
        'home_label': 'Go to the Datara homepage',
        'all_projects': 'Projects',
        'language_short': 'DA',
        'language_label': 'Read this page in Danish',
        'back_label': 'Back to projects',
        'rights': 'All rights reserved.',
        'privacy': 'Privacy',
        'terms': 'Terms',
    },
}

@app.route('/projekter/<int:projekt_id>')
def projekt_detail(projekt_id):
    project = PROJECTS.get(projekt_id)
    if not project:
        abort(404)

    lang = current_language()

    projekt = {
        **project,
        **project['content'][lang],
    }
    return render_template(
        'projekt.html',
        projekt=projekt,
        projekt_id=projekt_id,
        lang=lang,
        alternate_lang='en' if lang == 'da' else 'da',
        ui=PROJECT_UI[lang],
        year=datetime.now().year,
    )


@app.errorhandler(404)
def not_found(_error):
    lang = current_language()
    return render_template(
        '404.html',
        lang=lang,
        alternate_lang='en' if lang == 'da' else 'da',
        ui=CONTENT_UI[lang],
        year=datetime.now().year,
    ), 404

# SEO: robots.txt
@app.route('/robots.txt')
def robots():
    return "User-agent: *\nAllow: /\nSitemap: https://Datara.dk/sitemap.xml", 200, {'Content-Type': 'text/plain; charset=utf-8'}

# SEO: sitemap.xml
@app.route('/sitemap.xml')
def sitemap():
    base_url = 'https://Datara.dk'
    today = datetime.now().strftime('%Y-%m-%d')
    
    urls = [
        ('/', 'weekly', '1.0'),
    ]
    
    # Services
    services = [
        '/services/dataanalyse',
        '/services/forretningsudvikling',
        '/services/automatisering',
        '/services/it-produktudvikling',
    ]
    for service in services:
        urls.append((service, 'monthly', '0.8'))
    
    # Projects
    for projekt_id in PROJECTS.keys():
        urls.append((f'/projekter/{projekt_id}', 'monthly', '0.7'))

    # Legal/Info pages
    info_pages = [
        '/privatliv',
        '/cookies',
        '/vilkar',
    ]
    for page in info_pages:
        urls.append((page, 'yearly', '0.5'))
    
    # Build XML
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    
    for path, changefreq, priority in urls:
        xml += '  <url>\n'
        xml += f'    <loc>{base_url}{path}</loc>\n'
        xml += f'    <lastmod>{today}</lastmod>\n'
        xml += f'    <changefreq>{changefreq}</changefreq>\n'
        xml += f'    <priority>{priority}</priority>\n'
        xml += '  </url>\n'
    
    xml += '</urlset>'
    
    return Response(xml, mimetype='application/xml')

if __name__ == '__main__':
    app.run(debug=False)
