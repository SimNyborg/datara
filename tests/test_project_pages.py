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
        self.assertIn('12.592', heating)
        self.assertIn('1.922', heating)
        self.assertIn('6.554', heating)
        self.assertIn('gennemført af en gruppe på tre', heating)
        self.assertIn('EnergyMAPS', heating)
        self.assertIn('tabindex="-1"', heating)
        self.assertIn('/static/brugerunders%C3%B8gelse%20forside.jpg', automation)
        self.assertIn('/static/fjernvarme-resultatkort.png', heating)
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
        self.assertIn('12,592', heating)
        self.assertIn('three-person project focused on', heating)
        self.assertIn('EnergyMAPS', heating)
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

    def test_homepage_keeps_the_original_project_photos(self):
        homepage = self._html('/')
        self.assertIn('/static/fjernvarme.jpg', homepage)
        self.assertIn('/static/Pythonbillede.jpg', homepage)
        self.assertNotIn('projekt-fjernvarme.svg', homepage)
        self.assertNotIn('projekt-automatisering.svg', homepage)


if __name__ == '__main__':
    unittest.main()
