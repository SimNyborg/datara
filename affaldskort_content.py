"""Projektet om affaldsdebatten: projektsidens tekst og forsidekortet.

Nøgletallene (antal dokumenter, aktører, opdateringsdato ...) læses fra
apps/affaldskort/stats.json, som Affaldskort-pipelinen skriver hver gang
kortet publiceres (pipeline/publish_datara.py). Selve det interaktive kort
ligger i apps/affaldskort/ og bliver af freeze.py kopieret til /affaldskort/.
"""
import json
from pathlib import Path

APP_DIR = Path(__file__).resolve().parent / 'apps' / 'affaldskort'
APP_URL = '/affaldskort/'
SLUG = 'affaldsdebatten'

_DEFAULT_STATS = {
    'updated': '2026-09-19',
    'updated_da': '19. september 2026',
    'updated_en': '19 September 2026',
    'n_docs': 33259,
    'n_actors': 1632,
    'n_clusters': 83,
    'n_clusters_fine': 154,
    'n_sources': 900,
    'year_from': 1996,
}


def load_stats():
    stats = dict(_DEFAULT_STATS)
    try:
        stats.update(json.loads((APP_DIR / 'stats.json').read_text(encoding='utf-8')))
    except (OSError, ValueError):
        pass
    return stats


def _da(n):
    return f'{n:,}'.replace(',', '.')


def _en(n):
    return f'{n:,}'


def _floor_thousands(n):
    return (n // 1000) * 1000 if n >= 1000 else n


STATS = load_stats()
_n = STATS['n_docs']
_actors = STATS['n_actors']
_year = STATS.get('year_from') or 1996
_clusters = (STATS.get('n_clusters') or 0) + (STATS.get('n_clusters_fine') or 0)

PROJECT = {
    'slug': SLUG,
    'image': 'affaldskort-debatkort.jpg',
    'image_width': 1600,
    'image_height': 1000,
    'content': {
        'da': {
            'seo_title': 'Kortlægning af affaldsdebatten | Datara',
            'meta_description': (
                f'Et interaktivt kort over {_da(_n)} dokumenter fra debatten om affald i Danmark, '
                'fra Folketinget og byrådene til fagmedier og sociale medier.'
            ),
            'title': 'Hvem fører debatten om affald, og hvad handler den om?',
            'lead': (
                'Affald bliver diskuteret i Folketinget, i byrådene, i fag- og lokalmedier og på sociale medier. '
                f'Vi har samlet {_da(_n)} offentlige dokumenter fra debatten i ét kort. '
                'Kortet viser, hvilke emner der fylder, og hvem der deltager i dem.'
            ),
            'image_alt': 'Debatkortet med tusindvis af farvede punkter samlet i navngivne klynger',
            'image_caption': (
                'Hvert punkt er et dokument. Dokumenter med lignende indhold ligger tæt, '
                'og hver klynge har fået et navn efter sit emne.'
            ),
            'app_links': [
                {'label': 'Åbn kortet', 'href': APP_URL, 'primary': True},
                {'label': 'Debatkortet i fuld skærm', 'href': APP_URL + 'debatkort.html', 'primary': False},
            ],
            'sections': [
                {
                    'title': 'Et punkt for hvert dokument',
                    'paragraphs': [
                        f'Kortet rummer {_da(_n)} dokumenter: nyhedsartikler, debatindlæg, pressemeddelelser, '
                        'høringssvar, spørgsmål i Folketinget, punkter fra byråds- og udvalgsmøder og opslag på '
                        'sociale medier. Hvert dokument er placeret efter, hvad det handler om, så en artikel om '
                        'affaldsgebyrer ender tæt på et byrådspunkt om det samme.',
                        f'Dokumenterne falder i {_clusters} navngivne klynger. Punkterne kan farves efter tema, '
                        'dokumenttype eller afsender, og et tidsfilter nederst på kortet viser, hvad der blev '
                        'skrevet i en bestemt periode.',
                    ],
                },
                {
                    'title': 'Hvor dokumenterne kommer fra',
                    'paragraphs': [
                        'Folketingets åbne data giver alle spørgsmål, svar og sager om affald med spørgerens navn '
                        'og parti. Kommunernes dagsordener giver de lokale beslutninger om gebyrer, ordninger og '
                        'genbrugspladser. Resten kommer fra mediers og organisationers arkiver, pressemeddelelser, '
                        'rapporter og offentlige opslag på sociale medier.',
                        f'Samlet er der dokumenter fra mere end {_da(_floor_thousands(STATS.get("n_sources") or 0) or 100)} '
                        f'kilder. De ældste er fra {_year}, men de fleste er fra de seneste år, hvor sortering og '
                        'producentansvar har fyldt mest.',
                    ],
                },
                {
                    'title': 'Aktørerne bag debatten',
                    'paragraphs': [
                        f'Et register over {_da(_actors)} aktører knytter dokumenterne til dem, der udtaler sig eller '
                        'bliver omtalt: politikere, kommuner og affaldsselskaber, private virksomheder, '
                        'interesseorganisationer, forskere og medier.',
                        'Aktørkortet placerer aktørerne efter, hvad de taler om. Netværket viser, hvem der optræder i '
                        'de samme dokumenter, og dermed både lejrene i debatten og de aktører, der forbinder dem.',
                    ],
                },
                {
                    'title': 'Sådan er kortet lavet',
                    'paragraphs': [
                        'Titel og resumé for hvert dokument bliver omsat til en talvektor med en sprogmodel, der '
                        'forstår dansk. UMAP lægger vektorerne ud i to dimensioner, og HDBSCAN finder klyngerne, som '
                        'vi derefter har navngivet. Tonen i dokumenterne er vurderet med Alexandra Instituttets '
                        'danske sentimentmodel.',
                        'Metoden bygger på DTU ECHO Labs kort over folketingsvalget i 2026, og kortet er lavet med '
                        'DataMapPlot ligesom ECHO Labs.',
                    ],
                },
                {
                    'title': 'Kortet vokser løbende',
                    'paragraphs': [
                        'Nye dokumenter bliver høstet og lagt ind på det eksisterende kort, så punkterne bliver, hvor '
                        f'de er, og nye emner får deres egne klynger. Kortet blev senest opdateret {STATS["updated_da"]}.',
                        'Mangler der noget, eller er en aktør beskrevet forkert, hører vi gerne fra dig på '
                        'shn@datara.dk.',
                    ],
                },
            ],
            'note_title': 'Forbehold',
            'note': (
                'Dækningen er bedst for kilder uden betalingsmur. Opslag fra Facebook og LinkedIn er kun med, når de '
                'er offentlige og er blevet fundet ved søgning. For nyhedsartikler viser kortet titel, kilde og link, '
                'men ikke artiklens tekst.'
            ),
        },
        'en': {
            'seo_title': 'Mapping the Danish waste debate | Datara',
            'meta_description': (
                f'An interactive map of {_en(_n)} documents from the Danish debate about waste, '
                'from Parliament and city councils to trade media and social media.'
            ),
            'title': 'Who leads the debate on waste, and what is it about?',
            'lead': (
                'Waste is debated in the Danish Parliament, in city councils, in trade and local media and on social '
                f'media. We have gathered {_en(_n)} public documents from the debate into one map. It shows which '
                'topics take up space and who takes part in them.'
            ),
            'image_alt': 'The debate map with thousands of coloured points grouped into named clusters',
            'image_caption': (
                'Each point is a document. Documents with similar content sit close together, and each cluster is '
                'named after its topic.'
            ),
            'app_links': [
                {'label': 'Open the map (in Danish)', 'href': APP_URL, 'primary': True},
                {'label': 'Debate map in full screen', 'href': APP_URL + 'debatkort.html', 'primary': False},
            ],
            'sections': [
                {
                    'title': 'One point per document',
                    'paragraphs': [
                        f'The map holds {_en(_n)} documents: news articles, opinion pieces, press releases, '
                        'consultation responses, parliamentary questions, city council agenda items and social media '
                        'posts. Each document is placed according to what it is about, so an article on waste fees '
                        'ends up next to a council item on the same subject.',
                        f'The documents fall into {_clusters} named clusters. Points can be coloured by topic, '
                        'document type or sender, and a time filter at the bottom of the map shows what was written '
                        'in a given period.',
                    ],
                },
                {
                    'title': 'Where the documents come from',
                    'paragraphs': [
                        "The Danish Parliament's open data provides every question, answer and case about waste, "
                        "with the name and party of the member asking. Municipal agendas provide the local decisions "
                        "on fees, collection schemes and recycling sites. The rest comes from the archives of media "
                        "and organisations, press releases, reports and public social media posts.",
                        f'Altogether the documents come from more than {_en(_floor_thousands(STATS.get("n_sources") or 0) or 100)} '
                        f'sources. The oldest date from {_year}, but most are from recent years, when sorting and '
                        'producer responsibility have dominated.',
                    ],
                },
                {
                    'title': 'The actors behind the debate',
                    'paragraphs': [
                        f'A register of {_en(_actors)} actors links the documents to those who speak or are mentioned: '
                        'politicians, municipalities and waste companies, private businesses, interest groups, '
                        'researchers and media.',
                        'The actor map places the actors according to what they talk about. The network shows who '
                        'appears in the same documents, revealing both the camps in the debate and the actors who '
                        'connect them.',
                    ],
                },
                {
                    'title': 'How the map is made',
                    'paragraphs': [
                        'The title and summary of each document are turned into a numeric vector by a language model '
                        'that understands Danish. UMAP lays the vectors out in two dimensions, and HDBSCAN finds the '
                        "clusters, which we have then named. The tone of each document is scored with the Alexandra "
                        "Institute's Danish sentiment model.",
                        "The method follows DTU ECHO Lab's map of the 2026 Danish general election, and the map is "
                        'built with DataMapPlot, as ECHO Lab\'s is.',
                    ],
                },
                {
                    'title': 'The map keeps growing',
                    'paragraphs': [
                        'New documents are collected and added to the existing map, so the points stay where they are '
                        f'and new topics get their own clusters. The map was last updated on {STATS["updated_en"]}.',
                        'If something is missing, or an actor is described incorrectly, please let us know at '
                        'shn@datara.dk.',
                    ],
                },
            ],
            'note_title': 'Limitations',
            'note': (
                'Coverage is best for sources without a paywall. Facebook and LinkedIn posts are only included when '
                'they are public and have been found through search. For news articles the map shows the title, '
                "source and link, but not the article's text."
            ),
        },
    },
}

CARD = {
    'da': {
        'title': 'Debatkortlægning',
        'text': (
            f'Vi samlede over {_da(_floor_thousands(_n))} dokumenter om affald i ét kort over debattens temaer og '
            'aktører.'
        ),
        'image_alt': 'Kort over debatten om affald i Danmark med navngivne klynger',
    },
    'en': {
        'title': 'Debate mapping',
        'text': (
            f'We gathered more than {_en(_floor_thousands(_n))} documents about waste into one map of the '
            "debate's topics and actors."
        ),
        'image_alt': 'Map of the Danish waste debate with named clusters',
    },
}
