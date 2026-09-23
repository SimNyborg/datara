import json
import re
import unittest

import affaldskort_content
from app import app
import freeze


class AffaldskortProjectTests(unittest.TestCase):
    """The waste-debate map: project article, homepage card and the static map app."""

    def setUp(self):
        app.config.update(TESTING=True)
        self.client = app.test_client()

    def _html(self, path, status=200):
        response = self.client.get(path)
        self.assertEqual(response.status_code, status, path)
        html = response.get_data(as_text=True)
        response.close()
        return html

    def test_homepage_card_links_to_the_article_in_both_languages(self):
        for prefix, title in (('', 'Debatkortlægning'), ('/en', 'Debate mapping')):
            with self.subTest(prefix=prefix):
                html = self._html(prefix + '/' if prefix else '/')
                self.assertRegex(
                    html,
                    rf'<a class="project-card" href="{prefix}/projekter/affaldsdebatten">\s*'
                    r'<img class="project-card-map" src="/static/affaldskort-debatkort\.jpg"[\s\S]*?' + title,
                )

    def test_article_renders_in_both_languages_with_links_to_the_map(self):
        stats = affaldskort_content.STATS
        n_da = f"{stats['n_docs']:,}".replace(',', '.')
        n_en = f"{stats['n_docs']:,}"
        for path, lang, number, title in (
            ('/projekter/affaldsdebatten', 'da', n_da, 'Hvem fører debatten om affald'),
            ('/en/projekter/affaldsdebatten', 'en', n_en, 'Who leads the debate on waste'),
        ):
            with self.subTest(path=path):
                html = self._html(path)
                self.assertIn(f'<html lang="{lang}">', html)
                self.assertIn(title, html)
                self.assertIn(number, html)
                self.assertIn('class="project-app-links"', html)
                self.assertIn('href="/affaldskort/"', html)
                self.assertIn('href="/affaldskort/debatkort.html"', html)
                self.assertIn('/static/affaldskort-debatkort.jpg', html)
                self.assertEqual(len(re.findall(r'<h1(?:\s|>)', html)), 1)
                self.assertNotIn('–', html)
                self.assertNotIn('—', html)

    def test_article_mentions_the_latest_update(self):
        html = self._html('/projekter/affaldsdebatten')
        self.assertIn(affaldskort_content.STATS['updated_da'], html)

    def test_sitemap_lists_article_and_map(self):
        sitemap = self._html('/sitemap.xml')
        self.assertIn('https://datara.dk/projekter/affaldsdebatten</loc>', sitemap)
        self.assertIn('https://datara.dk/en/projekter/affaldsdebatten</loc>', sitemap)
        self.assertIn('https://datara.dk/affaldskort/</loc>', sitemap)

    def test_freeze_builds_the_article_and_copies_the_map_app(self):
        self.assertIn('/projekter/affaldsdebatten', freeze.DA_PAGES)
        self.assertEqual(freeze.APPS.get('affaldskort'), 'affaldskort')

    @unittest.skipUnless((affaldskort_content.APP_DIR / 'index.html').is_file(), 'kortet er ikke publiceret endnu')
    def test_map_app_is_public_and_complete(self):
        index = self._html('/affaldskort/')
        self.assertIn('<html lang="da">', index)
        self.assertIn('class="datara-bar"', index)
        self.assertIn('href="../projekter/affaldsdebatten"', index)
        for script in ('summary', 'actors', 'network', 'docs', 'documents', 'documents_2', 'documents_3'):
            self.assertIn(f'src="data/{script}.js"', index)
            self.assertTrue((affaldskort_content.APP_DIR / 'data' / f'{script}.js').is_file(), script)
        for page in ('debatkort.html', 'aktoerkort.html'):
            self.assertTrue((affaldskort_content.APP_DIR / page).is_file(), page)
        # internal working notes stay out of the public build
        self.assertNotIn('Sådan opdateres kortet', index)
        self.assertNotIn('run_update.py', index)
        docs_js = (affaldskort_content.APP_DIR / 'data' / 'docs.js').read_text(encoding='utf-8')
        docs = json.loads(docs_js[docs_js.index('{'):docs_js.rindex('}') + 1])
        self.assertNotIn('FORTSAET', docs['docs'])
        self.assertNotIn('INDSAMLINGSPLAN', docs['docs'])
        self.assertTrue(all(set(s) <= {'name', 'url', 'kind', 'coverage'} for s in docs['sources']))

    def test_unknown_map_file_is_a_404(self):
        self._html('/affaldskort/findes-ikke.html', status=404)


if __name__ == '__main__':
    unittest.main()
