import base64
import gzip
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
                    r'<img class="project-card-map" src="/static/affaldskort-kort\.jpg"[\s\S]*?' + title,
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
                # to knapper: hele kortet i fuld skærm (først, også billedets link) og fokuskortet
                self.assertIn('href="/affaldskort/debatkort.html"', html)
                self.assertIn('href="/affaldskort/fokus/"', html)
                self.assertLess(html.index('href="/affaldskort/debatkort.html"'), html.index('href="/affaldskort/fokus/"'))
                self.assertNotIn('href="/affaldskort/"', html)
                self.assertIn('/static/affaldskort-debatkort.jpg', html)
                self.assertEqual(len(re.findall(r'<h1(?:\s|>)', html)), 1)
                self.assertNotIn('–', html)
                self.assertNotIn('—', html)

    def test_no_mention_of_the_inspiration_from_dtu(self):
        # Simon 25-09-2026: kortet og siden må ikke omtale, at de er inspireret af DTU/ECHO Lab
        for path in ('/projekter/affaldsdebatten', '/en/projekter/affaldsdebatten', '/', '/en/'):
            with self.subTest(path=path):
                html = self._html(path)
                self.assertNotIn('ECHO', html)
        if (affaldskort_content.APP_DIR / 'index.html').is_file():
            self.assertNotIn('ECHO', self._html('/affaldskort/'))

    def test_article_mentions_the_latest_update(self):
        html = self._html('/projekter/affaldsdebatten')
        self.assertIn(affaldskort_content.STATS['updated_da'], html)

    def test_sitemap_lists_article_and_map(self):
        sitemap = self._html('/sitemap.xml')
        self.assertIn('https://datara.dk/projekter/affaldsdebatten</loc>', sitemap)
        self.assertIn('https://datara.dk/en/projekter/affaldsdebatten</loc>', sitemap)
        self.assertIn('https://datara.dk/affaldskort/</loc>', sitemap)
        self.assertIn('https://datara.dk/affaldskort/fokus/</loc>', sitemap)

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

    def test_project_pages_link_to_the_focused_map(self):
        for path, label in (('/projekter/affaldsdebatten', 'Se fokuskortet'), ('/en/projekter/affaldsdebatten', 'See the focused map \(in Danish\)')):
            with self.subTest(path=path):
                html = self._html(path)
                self.assertRegex(html, r'<a class="content-secondary-button" href="/affaldskort/fokus/">' + label + '</a>')

    @unittest.skipUnless((affaldskort_content.APP_DIR / 'fokus' / 'index.html').is_file(), 'fokuskortet er ikke publiceret endnu')
    def test_focused_map_is_public_and_links_back(self):
        fokus = self._html('/affaldskort/fokus/')
        self.assertIn('<html lang="da">', fokus)
        self.assertIn('| Datara</title>', fokus)
        self.assertIn('<link rel="canonical" href="https://datara.dk/affaldskort/fokus/">', fokus)
        self.assertIn('<meta name="description"', fokus)
        self.assertIn('href="/static/favicon-32x32.png"', fokus)
        self.assertIn('<a id="akf-back" href="../#debatkort" target="_top">Se hele debatten</a>', fokus)
        self.assertNotIn('ECHO', fokus)
        self.assertNotIn('DTU', fokus)
        for m in re.findall(r'src="(index_data_\d+\.js)"', fokus):
            self.assertTrue((affaldskort_content.APP_DIR / 'fokus' / m).is_file(), m)
        # dashboardets debatkort-fane kan skifte til fokuskortet
        index = self._html('/affaldskort/')
        self.assertIn('id="kortvalg"', index)
        self.assertIn('data-kort="fokus" aria-pressed="false"', index)
        self.assertIn('data-kort="hele" aria-pressed="true"', index)
        self.assertIn("fokus/index.html", index)
        self.assertIn('iframe id="kort-frame" data-src="debatkort.html"', index)

    @unittest.skipUnless((freeze.DEST / 'affaldskort' / 'index.html').is_file(), 'sitet er ikke frosset endnu')
    def test_frozen_site_has_the_focused_map(self):
        page = freeze.DEST / 'affaldskort' / 'fokus' / 'index.html'
        self.assertTrue(page.is_file(), page)
        html = page.read_text(encoding='utf-8')
        self.assertIn('Se hele debatten', html)
        self.assertIn('href="../#debatkort"', html)
        self.assertNotIn('ECHO', html)
        self.assertNotIn('DTU ECHO', html)
        self.assertTrue(list(page.parent.glob('index_data_*.js')))

    @unittest.skipUnless(list((affaldskort_content.APP_DIR / 'fokus').glob('index_data_*.js')), 'fokuskortet er ikke publiceret endnu')
    def test_focused_map_has_no_media_teasers(self):
        # svæveteksten (summary_short) og søgeteksten må ikke indeholde mediernes manchetter, som på hele kortet
        blob = ''
        for f in sorted((affaldskort_content.APP_DIR / 'fokus').glob('index_data_*.js')):
            blob += ''.join(re.findall(r'AKD\["hoverDataEncoded"\] = \(AKD\["hoverDataEncoded"\] \|\| ""\) \+ "([^"]*)"',
                                       f.read_text(encoding='utf-8')))
        self.assertTrue(blob, 'fandt ikke hoverDataEncoded i fokuskortets datafiler')
        hover = json.loads(gzip.decompress(base64.b64decode(blob)))
        self.assertIn('summary_short', hover)
        self.assertIn('search_text', hover)
        self.assertGreater(sum(not s for s in hover['summary_short']), 1000)   # mange mediedokumenter uden manchet
        for teaser in ('Vi får ikke genanvendt elektronik mere og bedre',   # Information
                       'Aktiekursen i renovationsselskabet RenoN',          # Finans
                       'Flere kommuner har fjernet skraldespande'):         # DR
            with self.subTest(teaser=teaser):
                self.assertFalse(any(teaser in s for s in hover['summary_short']))
                self.assertFalse(any(teaser.lower() in s for s in hover['search_text']))

    def test_unknown_map_file_is_a_404(self):
        self._html('/affaldskort/findes-ikke.html', status=404)


if __name__ == '__main__':
    unittest.main()
