from flask import Flask, abort, redirect, render_template, send_from_directory, request, url_for, Response
from datetime import datetime

from site_content import (
    CONTENT_UI,
    HOME_SERVICE_CARDS,
    HOME_SERVICE_ORDER,
    INFO_PAGES,
    SERVICE_PAGES,
)

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
        'nav_services': 'Ydelser',
        'nav_om': 'Om os',
        'nav_kontakt': 'Kontakt',
        'hero_h1': 'Mindre manuelt arbejde. Bedre beslutninger.',
        'hero_p': 'Vi automatiserer arbejdsgange, analyserer data og bygger digitale løsninger.',
        'projects_h2': 'Vores projekter',
        'services_h2': 'Det hjælper vi med',
        'founders_h2': 'Om Datara',
        'contact_h2': 'Kontakt os',
        'contact_description': 'Har I en opgave, vi skal se på, eller et spørgsmål? Ring, skriv eller find os på LinkedIn.',
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
        'hero_p': 'We automate workflows, analyse data and build digital tools.',
        'projects_h2': 'Our projects',
        'services_h2': 'What we can help with',
        'founders_h2': 'About Datara',
        'contact_h2': 'Contact us',
        'contact_description': 'Have a task you would like us to look at, or simply a question? Call, email or find us on LinkedIn.',
        'newsletter_label': 'Subscribe to our newsletter',
        'newsletter_button': 'Subscribe',
        'breadcrumb_back': '← Back',
        'lang_code': 'en'
    }
}


# The canonical production origin. Absolute URLs (canonical/og/hreflang and the
# sitemap) are built from this so the frozen static output is host-independent.
SITE_BASE = 'https://datara.dk'


def current_language():
    """The language is part of the URL: pages under /en/ are English."""
    path = request.path
    if path == '/en' or path.startswith('/en/'):
        return 'en'
    return 'da'


def _alternate_path():
    """Path of the same page in the other language."""
    path = request.path
    if path == '/en' or path.startswith('/en/'):
        rest = path[3:]
        return rest if rest else '/'
    return '/en/' if path == '/' else '/en' + path


@app.context_processor
def inject_strings():
    lang = current_language()
    strings = translations.get(lang, translations['da'])
    alternate = _alternate_path()

    def page_url(endpoint, **values):
        """url_for that stays inside the current language variant."""
        if lang == 'en':
            endpoint = f'{endpoint}_en'
        return url_for(endpoint, **values)

    da_path = request.path if lang == 'da' else alternate
    en_path = alternate if lang == 'da' else request.path
    return dict(
        strings=strings,
        footer_ui=CONTENT_UI[lang],
        page_url=page_url,
        alternate_url=alternate,
        lang_prefix='' if lang == 'da' else '/en',
        canonical_url=SITE_BASE + request.path,
        hreflang_da=SITE_BASE + da_path,
        hreflang_en=SITE_BASE + en_path,
        site_base=SITE_BASE,
    )

# Favicons are served from the project's `static/` folder and referenced
# in templates using `url_for('static', filename=...)`. No explicit routes
# are required here.

# Serve favicon.ico from the `static/` folder (canonical location for static assets)
@app.route('/favicon.ico')
def favicon():
    return send_from_directory('static', 'favicon.ico')


@app.route('/')
@app.route('/en/', endpoint='index_en')
def index():
    lang = current_language()
    homepage_services = [
        {
            'slug': slug,
            **HOME_SERVICE_CARDS[slug][lang],
        }
        for slug in HOME_SERVICE_ORDER[lang]
    ]
    return render_template(
        'index.html',
        homepage_services=homepage_services,
        year=datetime.now().year,
    )

# Footer info pages
@app.route('/privatliv')
@app.route('/en/privatliv', endpoint='privatliv_en')
def privatliv():
    return render_info_page('privatliv')

@app.route('/cookies')
@app.route('/en/cookies', endpoint='cookies_en')
def cookies():
    return render_info_page('cookies')

@app.route('/vilkar')
@app.route('/en/vilkar', endpoint='vilkar_en')
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
@app.route('/en/services/dataanalyse', endpoint='service_dataanalyse_en')
def service_dataanalyse():
    return render_service_page('dataanalyse')

@app.route('/services/forretningsudvikling')
@app.route('/en/services/forretningsudvikling', endpoint='service_forretningsudvikling_en')
def service_forretningsudvikling():
    return render_service_page('forretningsudvikling')

@app.route('/services/automatisering')
@app.route('/en/services/automatisering', endpoint='service_automatisering_en')
def service_automatisering():
    return render_service_page('automatisering')

@app.route('/services/it-produktudvikling')
@app.route('/en/services/it-produktudvikling', endpoint='service_it_produktudvikling_en')
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
                'meta_description': 'Analysen vurderer 12.592 bygningers egnethed til lavtemperaturfjernvarme og kortlægger mulige kilder til overskudsvarme i Lyngby-Taarbæk.',
                'title': 'Hvor kan fjernvarme ved lav temperatur fungere?',
                'lead': 'Formålet med projektet er at identificere de bygninger og områder i Lyngby-Taarbæk, der har højt potentiale for fjernvarme ved lav temperatur, og de virksomheder, der kan levere overskydende varme tilbage til nettet. Kortlægningen viser både bygningernes egnethed og mulige lokale varmekilder.',
                'image_alt': 'Resultatkort over bygningers potentiale for lavtemperaturfjernvarme i Lyngby-Taarbæk',
                'image_caption': 'Blandt de 12.592 bygninger viser grøn højt potentiale, gul mulig egnethed efter forbedringer og rød lavt potentiale.',
                'sections': [
                    {
                        'title': 'Hvorfor sænke temperaturen?',
                        'paragraphs': [
                            '55/25 °C giver knap 40 procent mindre varmetab fra rørene end 80/40 °C. Den lavere temperatur kan også mindske behovet for rørisolering og gøre virksomheders overskudsvarme lettere at bruge. Nogle huse er dog ikke energieffektive nok og kan kræve forbedringer først, så beboerne ikke kommer til at fryse om vinteren.',
                        ],
                    },
                    {
                        'title': 'Bygningsdata samlet ét sted',
                        'paragraphs': [
                            'Analysen samler bygningsoplysninger fra BBR, energimærker, forventet årsforbrug fra Gasportalen og data om det eksisterende fjernvarmenet i Lyngby-Taarbæk Kommune. Manglende værdier estimeres med statistiske modeller, der er udviklet til analysen. På baggrund af det samlede datagrundlag vurderes bygningernes egnethed til lavtemperaturfjernvarme.',
                        ],
                    },
                    {
                        'title': 'Bygningernes potentiale',
                        'paragraphs': [
                            '1.922 bygninger har højt potentiale. 6.554 kan blive egnede efter forbedringer, mens 4.051 har lavt potentiale.',
                            'Resultaterne vises på et kort sammen med det eksisterende fjernvarmenet.',
                        ],
                    },
                    {
                        'title': 'Fra bygninger til veje',
                        'paragraphs': [
                            'Da temperaturen kun kan sænkes på vejniveau, er bygningerne med lavest potentiale afgørende for vejens samlede vurdering.',
                            'På kortet har grønne veje kun bygninger med højt eller muligt potentiale. På gule veje har højst 10 procent af bygningerne lavt potentiale. På røde veje er andelen højere.',
                        ],
                        'figure': {
                            'filename': 'fjernvarme-vejkort.png',
                            'alt': 'Vejkort med grønne, gule og røde vejstrækninger i Lyngby-Taarbæk',
                            'width': 1280,
                            'height': 720,
                        },
                    },
                    {
                        'title': 'Overskudsvarme i nærheden',
                        'paragraphs': [
                            'Overskudsvarme er varme fra for eksempel køling eller produktion, som ellers ikke bliver brugt.',
                            'Analysen undersøger 78 virksomheder med EnergyMAPS-data fra Varmeplan Danmark 2021. Ti steder udvælges derefter på baggrund af kommunens energiplan og en vurdering af køleanlæg. Resultaterne er skøn, som skal følges op med målinger og dialog med virksomhederne.',
                        ],
                        'figure': {
                            'filename': 'fjernvarme-overskudsvarmekilder.png',
                            'alt': 'Kort over ti steder i Lyngby-Taarbæk udvalgt til nærmere undersøgelse som mulige kilder til overskudsvarme',
                            'width': 1796,
                            'height': 924,
                        },
                    },
                    {
                        'title': 'Hvad analysen kan bruges til',
                        'paragraphs': [
                            'Analysen peger på de bygninger, vejstrækninger og virksomheder, der er mest relevante at undersøge nærmere.',
                        ],
                    },
                ],
                'cta_title': 'Har I data, der skal samles?',
                'cta_text': 'Vi kan samle og kontrollere dem, så de er lettere at bruge i det videre arbejde.',
                'cta_label': 'Tal med os om jeres data',
            },
            'en': {
                'seo_title': 'Mapping low-temperature district heating | Datara',
                'meta_description': 'The analysis assesses 12,592 buildings for low-temperature district heating and maps possible sources of surplus heat in Lyngby-Taarbæk.',
                'title': 'Where could low-temperature district heating work?',
                'lead': 'The purpose of the project is to identify the buildings and areas in Lyngby-Taarbæk with high potential for low-temperature district heating, as well as the businesses that can supply surplus heat to the district-heating network. The mapping shows both building suitability and possible local heat sources.',
                'image_alt': 'Results map showing building potential for low-temperature district heating in Lyngby-Taarbæk',
                'image_caption': 'Among the 12,592 buildings, green shows high potential, yellow possible suitability after improvements and red low potential.',
                'sections': [
                    {
                        'title': 'Why lower the temperature?',
                        'paragraphs': [
                            '55/25 °C produces nearly 40 per cent less heat loss from the pipes than 80/40 °C. The lower temperature can also reduce the need for pipe insulation and make surplus heat from businesses easier to use. Some homes are not energy-efficient enough and may need improvements first so residents can stay warm in winter.',
                        ],
                    },
                    {
                        'title': 'Building data in one place',
                        'paragraphs': [
                            'The analysis combines data from the Danish building register, energy labels, expected annual consumption from Gasportalen and information about the existing district-heating network in Lyngby-Taarbæk Municipality. Missing values are estimated with statistical models developed for the analysis. The combined data is used to assess each building’s suitability for low-temperature district heating.',
                        ],
                    },
                    {
                        'title': 'Building potential',
                        'paragraphs': [
                            '1,922 buildings have high potential. A further 6,554 may become suitable after improvements, while 4,051 have low potential.',
                            'The results are shown on a map alongside the existing district-heating network.',
                        ],
                    },
                    {
                        'title': 'From buildings to streets',
                        'paragraphs': [
                            'Because the temperature can only be lowered at street level, the buildings with the lowest potential determine the overall assessment of each street.',
                            'On the map, green streets contain only buildings with high or possible potential. On yellow streets, no more than 10 per cent of buildings have low potential. On red streets, the share is higher.',
                        ],
                        'figure': {
                            'filename': 'fjernvarme-vejkort.png',
                            'alt': 'Street map with green, yellow and red sections in Lyngby-Taarbæk',
                            'width': 1280,
                            'height': 720,
                        },
                    },
                    {
                        'title': 'Surplus heat nearby',
                        'paragraphs': [
                            'Surplus heat is heat from activities such as cooling or production that would otherwise go unused.',
                            'The analysis assesses 78 businesses using EnergyMAPS data from Varmeplan Danmark 2021. Ten sites are then selected using the municipal energy plan and an assessment of cooling systems. The results are estimates that need to be followed up with measurements and direct contact with the businesses.',
                        ],
                        'figure': {
                            'filename': 'fjernvarme-overskudsvarmekilder.png',
                            'alt': 'Map of ten sites in Lyngby-Taarbæk selected for closer investigation as potential sources of surplus heat',
                            'width': 1796,
                            'height': 924,
                        },
                    },
                    {
                        'title': 'How the analysis can be used',
                        'paragraphs': [
                            'The analysis points to the buildings, street sections and businesses that are most relevant for closer investigation.',
                        ],
                    },
                ],
                'cta_title': 'Do you need to bring data together?',
                'cta_text': 'We can combine and check it, making it easier to use in the next stage of work.',
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

PROJECT_SLUGS = {project['slug']: pid for pid, project in PROJECTS.items()}


@app.route('/projekter/<int:projekt_id>')
@app.route('/en/projekter/<int:projekt_id>', endpoint='projekt_detail_id_en')
def projekt_detail_by_id(projekt_id):
    """Old numeric URLs redirect permanently to the slug URLs."""
    project = PROJECTS.get(projekt_id)
    if not project:
        abort(404)
    prefix = '/en' if current_language() == 'en' else ''
    return redirect(f"{prefix}/projekter/{project['slug']}", code=301)


@app.route('/projekter/<slug>')
@app.route('/en/projekter/<slug>', endpoint='projekt_detail_en')
def projekt_detail(slug):
    projekt_id = PROJECT_SLUGS.get(slug)
    if projekt_id is None:
        abort(404)
    project = PROJECTS[projekt_id]

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
    return f"User-agent: *\nAllow: /\nSitemap: {SITE_BASE}/sitemap.xml", 200, {'Content-Type': 'text/plain; charset=utf-8'}

# SEO: sitemap.xml
@app.route('/sitemap.xml')
def sitemap():
    base_url = SITE_BASE
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
    for project in PROJECTS.values():
        urls.append((f"/projekter/{project['slug']}", 'monthly', '0.7'))

    # Legal/Info pages
    info_pages = [
        '/privatliv',
        '/cookies',
        '/vilkar',
    ]
    for page in info_pages:
        urls.append((page, 'yearly', '0.5'))

    # English variants live under /en/ (the Danish homepage's twin is /en/).
    urls += [
        ('/en/' if path == '/' else f'/en{path}', changefreq, priority)
        for path, changefreq, priority in list(urls)
    ]

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
