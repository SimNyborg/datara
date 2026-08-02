import re
import unittest
from urllib.parse import urlsplit

from app import app


class ProjectPageTests(unittest.TestCase):
    def setUp(self):
        app.config.update(TESTING=True)
        self.client = app.test_client()

    def _html(self, path):
        response = self.client.get(path)
        self.assertEqual(response.status_code, 200, path)
        html = response.get_data(as_text=True)
        response.close()
        return html

    def _switch_to_english(self, return_path='/projekter/1'):
        response = self.client.get(
            '/setlang/en',
            headers={'Referer': f'http://localhost{return_path}'},
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.headers['Location'], f'http://localhost{return_path}')

    def test_homepage_cards_link_to_different_articles(self):
        html = self._html('/')
        heating_card = re.search(
            r'<a class="project-card" href="/projekter/2">.*?Fjernvarmekortlægning',
            html,
            re.DOTALL,
        )
        automation_card = re.search(
            r'<a class="project-card" href="/projekter/1">.*?Automatisering',
            html,
            re.DOTALL,
        )
        self.assertIsNotNone(heating_card)
        self.assertIsNotNone(automation_card)

    def test_danish_articles_are_distinct_and_complete(self):
        automation = self._html('/projekter/1')
        heating = self._html('/projekter/2')

        self.assertIn('<html lang="da">', automation)
        self.assertIn('8.000', automation)
        self.assertIn('cirka 80 timers manuelt tastearbejde', automation)
        self.assertIn('Fra papirskema til færdigt datasæt', automation)
        self.assertIn('Hvor kan fjernvarme ved lav temperatur fungere?', heating)
        self.assertIn('Formålet med projektet er at identificere de bygninger og områder', heating)
        self.assertIn('områder i Lyngby-Taarbæk, der har højt potentiale', heating)
        self.assertIn('virksomheder, der kan levere overskydende varme tilbage til nettet', heating)
        self.assertIn('Kortlægningen viser både bygningernes egnethed', heating)
        self.assertIn('Hvorfor sænke temperaturen?', heating)
        self.assertIn('55/25 °C giver knap 40 procent mindre varmetab', heating)
        self.assertNotIn('Ved ellers samme rørforhold', heating)
        self.assertIn('knap 40 procent mindre varmetab fra rørene', heating)
        self.assertIn('så beboerne ikke kommer til at fryse om vinteren', heating)
        self.assertNotIn('Analysen samlede svarene i et kort', heating)
        self.assertNotIn('Projektet samlede svarene i et kort', heating)
        self.assertNotIn('Fagprojekt Â· Lyngby-TaarbÃ¦k', heating)
        self.assertNotIn('class="project-eyebrow"', automation)
        self.assertNotIn('class="project-eyebrow"', heating)
        self.assertNotIn('class="project-facts"', automation)
        self.assertNotIn('class="project-facts"', heating)
        self.assertIn('12.592', heating)
        self.assertIn('1.922', heating)
        self.assertIn('6.554', heating)
        self.assertIn(
            'statistiske modeller, der er udviklet til analysen',
            heating,
        )
        self.assertIn(
            'bygningernes egnethed til lavtemperaturfjernvarme',
            heating,
        )
        self.assertIn(
            'Lyngby-Taarbæk Kommune. Manglende værdier estimeres',
            heating,
        )
        self.assertIn(
            'Overskudsvarme er varme fra for eksempel køling eller produktion',
            heating,
        )
        self.assertNotIn(
            '65 blev udeladt, fordi datagrundlaget ikke var godt nok',
            heating,
        )
        self.assertNotIn('gruppe på tre', heating.lower())
        self.assertNotIn('gruppen', heating.lower())
        self.assertNotIn('som case', heating.lower())
        self.assertIn('EnergyMAPS', heating)
        self.assertIn('tabindex="-1"', heating)
        self.assertIn('/static/brugerunders%C3%B8gelse%20forside.jpg', automation)
        self.assertRegex(
            heating,
            r'<figure class="project-hero-figure">\s*'
            r'<img src="/static/fjernvarme-resultatkort\.png"',
        )
        self.assertIn('/static/fjernvarme-vejkort.png', heating)
        self.assertIn('/static/fjernvarme-overskudsvarmekilder.png', heating)
        self.assertEqual(
            heating.count('class="project-story-figure"'),
            2,
        )
        self.assertNotIn('project-gallery-section--results', heating)
        self.assertNotIn('Resultaterne på kort', heating)
        self.assertLess(
            heating.index('Hvorfor sænke temperaturen?'),
            heating.index('Bygningsdata samlet ét sted'),
        )
        self.assertLess(
            heating.index('Fra bygninger til veje'),
            heating.index('/static/fjernvarme-vejkort.png'),
        )
        self.assertLess(
            heating.index('/static/fjernvarme-vejkort.png'),
            heating.index('Overskudsvarme i nærheden'),
        )
        self.assertLess(
            heating.index('Overskudsvarme i nærheden'),
            heating.index('/static/fjernvarme-overskudsvarmekilder.png'),
        )
        self.assertLess(
            heating.index('/static/fjernvarme-overskudsvarmekilder.png'),
            heating.index('Hvad analysen kan bruges til'),
        )
        self.assertIn('temperaturen kun kan sænkes på vejniveau', heating)
        self.assertIn('bygningerne med lavest potentiale', heating)
        self.assertIn('Ti steder udvælges derefter', heating)
        for past_tense_phrase in (
            'Formålet var',
            'rørforhold gav',
            'Analysen samlede',
            'værdier manglede',
            'blev estimeret',
            'bygninger havde',
            'Resultaterne blev',
            'virksomheder undersøgt',
            'steder udvalgt',
        ):
            self.assertNotIn(past_tense_phrase, heating)
        self.assertIn(
            'Blandt de 12.592 bygninger viser grøn højt potentiale',
            heating,
        )
        self.assertNotIn('Kortet viser 12.522 af de 12.527', heating)
        self.assertNotIn('Vigtigt forbehold', heating)
        self.assertNotIn(
            'Resultatet er en screening – ikke dokumentation',
            heating,
        )
        self.assertNotIn('project-context-figure', heating)
        self.assertNotIn('/static/fjernvarme.jpg', heating)
        self.assertNotIn(
            'Fjernvarmerør under anlæg – den fysiske virkelighed',
            heating,
        )
        self.assertRegex(
            heating,
            r'<h2 id="section-4">Fra bygninger til veje</h2>[\s\S]*?'
            r'<img src="/static/fjernvarme-vejkort\.png"',
        )
        self.assertIn('Fra skema til rapport', automation)
        self.assertIn('Fra bygninger til veje', heating)
        self.assertNotIn('projekt-automatisering.svg', automation)
        self.assertNotIn('projekt-fjernvarme.svg', heating)
        self.assertIn('href="/setlang/en"', heating)
        self.assertNotEqual(automation, heating)
        self.assertNotIn('\ufffd', automation + heating)

    def test_english_articles_and_image_paths(self):
        self._switch_to_english('/projekter/2')
        automation = self._html('/projekter/1')
        heating = self._html('/projekter/2')

        self.assertIn('<html lang="en">', heating)
        self.assertIn('8,000', automation)
        self.assertIn('roughly 80 hours of manual data entry', automation)
        self.assertIn('From paper form to finished dataset', automation)
        self.assertIn('Where could low-temperature district heating work?', heating)
        self.assertIn('The purpose of the project is to identify the buildings', heating)
        self.assertIn('areas in Lyngby-Taarbæk with high potential', heating)
        self.assertIn('businesses that can supply surplus heat to the district-heating network', heating)
        self.assertIn('The mapping shows both building suitability', heating)
        self.assertIn('Why lower the temperature?', heating)
        self.assertIn('55/25 °C produces nearly 40 per cent less heat loss', heating)
        self.assertNotIn('Under otherwise comparable pipe conditions', heating)
        self.assertIn('nearly 40 per cent less heat loss from the pipes', heating)
        self.assertIn('so residents can stay warm in winter', heating)
        self.assertNotIn('brought both sides together in a map', heating)
        self.assertNotIn('Student project Â· Lyngby-TaarbÃ¦k', heating)
        self.assertNotIn('class="project-eyebrow"', automation)
        self.assertNotIn('class="project-eyebrow"', heating)
        self.assertNotIn('class="project-facts"', automation)
        self.assertNotIn('class="project-facts"', heating)
        self.assertIn('12,592', heating)
        self.assertIn(
            'statistical models developed for the analysis',
            heating,
        )
        self.assertIn(
            'assess each building’s suitability for low-temperature district heating',
            heating,
        )
        self.assertIn(
            'Surplus heat is heat from activities such as cooling or production',
            heating,
        )
        self.assertNotIn(
            'Another 65 were excluded because the data was insufficient',
            heating,
        )
        self.assertNotIn('three-person', heating.lower())
        first_heating_section = heating[
            heating.index('Building data in one place'):
            heating.index('Building potential')
        ]
        self.assertNotRegex(first_heating_section.lower(), r'\bteam\b')
        self.assertIn('EnergyMAPS', heating)
        self.assertIn(
            'Among the 12,592 buildings, green shows high potential',
            heating,
        )
        self.assertEqual(heating.count('class="project-story-figure"'), 2)
        self.assertNotIn('project-gallery-section--results', heating)
        self.assertNotIn('The results on the map', heating)
        self.assertLess(
            heating.index('Why lower the temperature?'),
            heating.index('Building data in one place'),
        )
        self.assertLess(
            heating.index('From buildings to streets'),
            heating.index('/static/fjernvarme-vejkort.png'),
        )
        self.assertLess(
            heating.index('/static/fjernvarme-vejkort.png'),
            heating.index('Surplus heat nearby'),
        )
        self.assertLess(
            heating.index('Surplus heat nearby'),
            heating.index('/static/fjernvarme-overskudsvarmekilder.png'),
        )
        self.assertLess(
            heating.index('/static/fjernvarme-overskudsvarmekilder.png'),
            heating.index('How the analysis can be used'),
        )
        self.assertIn('temperature can only be lowered at street level', heating)
        self.assertIn('buildings with the lowest potential', heating)
        self.assertIn('Ten sites are then selected', heating)
        for past_tense_phrase in (
            'The purpose was',
            'produced nearly 40 per cent',
            'The analysis combined',
            'values were missing',
            'were estimated',
            'buildings had high potential',
            'results were brought together',
            'businesses were assessed',
            'sites were then selected',
        ):
            self.assertNotIn(past_tense_phrase, heating)
        self.assertNotIn('An important limitation', heating)
        self.assertNotIn(
            'District-heating pipes under construction',
            heating,
        )
        self.assertNotIn('/static/fjernvarme.jpg', heating)
        self.assertIn('href="/setlang/da"', heating)
        self.assertNotIn('\ufffd', automation + heating)

        for path, html in (('/projekter/1', automation), ('/projekter/2', heating)):
            image_urls = re.findall(r'<img[^>]+src="([^"]+)"', html)
            self.assertTrue(image_urls, path)
            for image_url in image_urls:
                static_path = urlsplit(image_url).path
                response = self.client.get(static_path)
                self.assertEqual(response.status_code, 200, static_path)
                data = response.get_data()
                response.close()
                self.assertGreater(len(data), 100, static_path)

    def test_sitemap_only_lists_published_projects(self):
        sitemap = self._html('/sitemap.xml')
        self.assertIn('/projekter/1</loc>', sitemap)
        self.assertIn('/projekter/2</loc>', sitemap)
        self.assertNotIn('/projekter/3</loc>', sitemap)
        self.assertNotIn('/projekter/4</loc>', sitemap)

    def test_unknown_project_is_a_real_404(self):
        response = self.client.get('/projekter/999')
        self.assertEqual(response.status_code, 404)

    def test_homepage_uses_the_requested_project_media(self):
        homepage = self._html('/')
        self.assertRegex(
            homepage,
            r'<a class="project-card" href="/projekter/2">\s*'
            r'<img class="project-card-map" '
            r'src="/static/fjernvarme-vejkort\.png"',
        )
        self.assertIn('/static/Pythonbillede.jpg', homepage)
        self.assertNotIn('projekt-fjernvarme.svg', homepage)
        self.assertNotIn('projekt-automatisering.svg', homepage)


if __name__ == '__main__':
    unittest.main()
