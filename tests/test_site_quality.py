import re
import unittest

from app import app


PUBLIC_ROUTES = (
    '/',
    '/projekter/1',
    '/projekter/2',
    '/services/dataanalyse',
    '/services/forretningsudvikling',
    '/services/automatisering',
    '/services/it-produktudvikling',
    '/privatliv',
    '/cookies',
    '/vilkar',
)


class SiteQualityTests(unittest.TestCase):
    def setUp(self):
        app.config.update(TESTING=True)
        self.client = app.test_client()

    def _switch_language(self, language, return_path='/'):
        return self.client.get(
            f'/setlang/{language}',
            headers={'Referer': f'http://localhost{return_path}'},
        )

    def test_every_public_page_has_a_responsive_semantic_shell_in_both_languages(self):
        for language in ('da', 'en'):
            self._switch_language(language)
            for path in PUBLIC_ROUTES:
                with self.subTest(language=language, path=path):
                    response = self.client.get(path)
                    self.assertEqual(response.status_code, 200)
                    html = response.get_data(as_text=True)
                    self.assertIn(f'<html lang="{language}">', html)
                    self.assertRegex(
                        html,
                        r'<meta name="viewport" content="width=device-width, initial-scale=1\.0">',
                    )
                    self.assertEqual(len(re.findall(r'<main(?:\s|>)', html)), 1)
                    self.assertEqual(len(re.findall(r'<h1(?:\s|>)', html)), 1)
                    self.assertNotIn('\ufffd', html)
                    self.assertNotIn('/newsletter-signup', html)

    def test_shared_pages_load_the_refresh_stylesheet(self):
        for path in PUBLIC_ROUTES:
            with self.subTest(path=path):
                html = self.client.get(path).get_data(as_text=True)
                self.assertIn('/static/site-refresh.css', html)

    def test_language_redirect_rejects_external_referrers(self):
        response = self.client.get(
            '/setlang/en',
            headers={'Referer': 'https://example.org/not-datara'},
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.headers['Location'], '/')
        self.assertIn('SameSite=Lax', response.headers.get('Set-Cookie', ''))

    def test_security_headers_are_present(self):
        response = self.client.get('/')
        self.assertEqual(response.headers['X-Content-Type-Options'], 'nosniff')
        self.assertEqual(response.headers['X-Frame-Options'], 'SAMEORIGIN')
        self.assertEqual(
            response.headers['Referrer-Policy'],
            'strict-origin-when-cross-origin',
        )
        self.assertEqual(
            response.headers['Content-Security-Policy'],
            "frame-ancestors 'self'",
        )

    def test_cookie_copy_matches_the_language_cookie(self):
        cookies = self.client.get('/cookies').get_data(as_text=True)
        self.assertIn('site_lang', cookies)
        self.assertIn('30 dage', cookies)

        self._switch_language('en')
        cookies = self.client.get('/cookies').get_data(as_text=True)
        self.assertIn('site_lang', cookies)
        self.assertIn('30 days', cookies)

    def test_founder_buttons_and_profile_pages_are_retired(self):
        for language in ('da', 'en'):
            self._switch_language(language)
            html = self.client.get('/').get_data(as_text=True)
            for text in ('Mød Simon', 'Mød Albert', 'Meet Simon', 'Meet Albert'):
                self.assertNotIn(text, html)
            self.assertNotIn('/founder/', html)

        for path in ('/founder/simon-nyborg', '/founder/albert-koba'):
            with self.subTest(path=path):
                response = self.client.get(path)
                self.assertEqual(response.status_code, 301)
                self.assertEqual(response.headers['Location'], '/#hvemervi')

        sitemap = self.client.get('/sitemap.xml').get_data(as_text=True)
        self.assertNotIn('/founder/', sitemap)

    def test_manifest_icons_resolve(self):
        manifest_response = self.client.get('/static/site.webmanifest')
        self.assertEqual(manifest_response.status_code, 200)
        manifest = manifest_response.get_json()
        manifest_response.close()
        self.assertEqual(manifest['name'], 'Datara')
        for icon in manifest['icons']:
            with self.subTest(icon=icon['src']):
                response = self.client.get(icon['src'])
                self.assertEqual(response.status_code, 200)
                response.close()

    def test_unknown_page_uses_the_branded_404(self):
        response = self.client.get('/denne-side-findes-ikke')
        self.assertEqual(response.status_code, 404)
        html = response.get_data(as_text=True)
        self.assertIn('content-page', html)
        self.assertIn('<h1', html)
        self.assertIn('/static/site-refresh.css', html)

    def test_homepage_keeps_the_existing_photography(self):
        html = self.client.get('/').get_data(as_text=True)
        for filename in (
            'fjernvarme.jpg',
            'Pythonbillede.jpg',
            'SKylab%20billede.jpg',
            'DTU-B112%20efterår.jpg',
        ):
            self.assertIn(f'/static/{filename}', html)
        css_response = self.client.get('/static/style.css')
        css = css_response.get_data(as_text=True)
        css_response.close()
        self.assertIn('/static/K%C3%B8benhavn%20baggrundsbillede%20test.jpg', css)
        self.assertNotIn('projekt-fjernvarme.svg', html)
        self.assertNotIn('projekt-automatisering.svg', html)


if __name__ == '__main__':
    unittest.main()
