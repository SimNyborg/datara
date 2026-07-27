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

    def test_every_live_page_uses_the_same_footer_in_both_languages(self):
        for language in ('da', 'en'):
            self._switch_language(language)
            paths = (*PUBLIC_ROUTES, '/denne-side-findes-ikke')
            for path in paths:
                with self.subTest(language=language, path=path):
                    response = self.client.get(path)
                    expected_status = 404 if path == '/denne-side-findes-ikke' else 200
                    self.assertEqual(response.status_code, expected_status)
                    html = response.get_data(as_text=True)
                    response.close()

                    self.assertEqual(html.count('<footer'), 1)
                    self.assertEqual(html.count('class="unified-footer"'), 1)
                    self.assertIn('class="unified-footer-brand"', html)
                    self.assertIn('>DATARA</a>', html)
                    self.assertIn('class="unified-footer-contact"', html)
                    self.assertIn('class="unified-footer-links"', html)
                    self.assertIn('class="unified-footer-copyright"', html)
                    self.assertIn('href="mailto:shn@datara.dk"', html)
                    self.assertIn('href="tel:+4552390360"', html)
                    self.assertIn('href="/privatliv"', html)
                    self.assertIn('href="/cookies"', html)
                    self.assertIn('href="/vilkar"', html)
                    self.assertNotIn('class="site-footer"', html)
                    self.assertNotIn('class="project-footer"', html)

                    if language == 'da':
                        self.assertIn('Skriv til os', html)
                        self.assertIn('Privatliv', html)
                        self.assertIn('Vilkår', html)
                        self.assertIn('Alle rettigheder forbeholdes.', html)
                        self.assertIn('aria-label="Juridiske links"', html)
                    else:
                        self.assertIn('Email us', html)
                        self.assertIn('Privacy', html)
                        self.assertIn('Terms', html)
                        self.assertIn('All rights reserved.', html)
                        self.assertIn('aria-label="Legal links"', html)

    def test_every_page_uses_the_same_navigation_system(self):
        for language in ('da', 'en'):
            self._switch_language(language)
            for path in PUBLIC_ROUTES:
                with self.subTest(language=language, path=path):
                    html = self.client.get(path).get_data(as_text=True)
                    self.assertIn('class="navbar site-navbar', html)
                    self.assertIn('id="navbar-burger"', html)
                    self.assertIn('id="navbar-mobile-menu"', html)
                    self.assertNotIn('class="project-site-header"', html)
                    self.assertNotIn('class="content-site-header"', html)

        header_script = self.client.get('/static/js/site-header.js')
        self.assertEqual(header_script.status_code, 200)
        self.assertIn(
            "burger.setAttribute('aria-expanded'",
            header_script.get_data(as_text=True),
        )
        header_script.close()

    def test_project_article_navigation_auto_hides_on_scroll(self):
        header_script_response = self.client.get('/static/js/site-header.js')
        header_script = header_script_response.get_data(as_text=True)
        header_script_response.close()
        self.assertIn(
            "document.body.classList.contains('project-detail-page')",
            header_script,
        )
        self.assertIn("navbar.classList.add('navbar-hidden')", header_script)
        self.assertIn('window.requestAnimationFrame', header_script)
        self.assertIn("{ passive: true }", header_script)

        css_response = self.client.get('/static/site-refresh.css')
        css = css_response.get_data(as_text=True)
        css_response.close()
        self.assertIn(
            '.project-detail-page .site-navbar--inner.navbar-hidden',
            css,
        )
        self.assertIn('transform: translateY(calc(-100% - 8px))', css)

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

    def test_desktop_language_switch_clears_the_page_rail(self):
        css_response = self.client.get('/static/site-refresh.css')
        css = css_response.get_data(as_text=True)
        css_response.close()
        self.assertIn('--header-rail-clearance: 16px', css)
        self.assertIn(
            'right: calc(var(--page-margin-line-offset) + '
            'var(--header-rail-clearance))',
            css,
        )

    def test_homepage_service_cards_use_compact_responsive_layouts(self):
        css_response = self.client.get('/static/site-refresh.css')
        css = css_response.get_data(as_text=True)
        css_response.close()
        self.assertIn(
            'grid-template-columns: repeat(4, minmax(0, 1fr))',
            css,
        )
        self.assertIn(
            'grid-template-columns: 34px minmax(0, 1fr)',
            css,
        )
        self.assertIn('#services.services-section', css)
        self.assertRegex(
            css,
            r'\.home-page \.service-card \{\s+min-height: 0;',
        )

    def test_about_and_contact_sections_have_compact_responsive_rules(self):
        css_response = self.client.get('/static/site-refresh.css')
        css = css_response.get_data(as_text=True)
        css_response.close()
        self.assertIn('height: clamp(350px, 28vw, 430px)', css)
        self.assertIn(
            'grid-template-columns: minmax(0, 1.12fr) '
            'minmax(280px, 0.88fr)',
            css,
        )
        self.assertIn(
            'grid-template-columns: repeat(2, minmax(0, 1fr)) !important',
            css,
        )

    def test_heating_article_results_use_prominent_responsive_maps(self):
        css_response = self.client.get('/static/site-refresh.css')
        css = css_response.get_data(as_text=True)
        css_response.close()
        self.assertIn(
            '.project-detail-page--lavtemperaturfjernvarme '
            '.project-gallery-grid',
            css,
        )
        self.assertIn('grid-template-columns: minmax(0, 1fr)', css)
        self.assertIn(
            '.project-detail-page--lavtemperaturfjernvarme '
            '.project-context-figure',
            css,
        )
        self.assertIn(
            'width: min(calc(100% - 36px), 900px)',
            css,
        )
        self.assertIn('height: clamp(260px, 24vw, 320px)', css)
        self.assertIn('width: min(100%, 920px)', css)
        self.assertIn('width: min(100%, 800px)', css)

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

    def test_homepage_keeps_the_requested_existing_media(self):
        html = self.client.get('/').get_data(as_text=True)
        for filename in (
            'fjernvarme-vejkort.png',
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
