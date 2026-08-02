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
                    self.assertIn('>shn@datara.dk</a>', html)
                    self.assertIn('href="tel:+4552390360"', html)
                    self.assertIn('href="/privatliv"', html)
                    self.assertIn('href="/cookies"', html)
                    self.assertIn('href="/vilkar"', html)
                    self.assertNotIn('class="site-footer"', html)
                    self.assertNotIn('class="project-footer"', html)

                    if language == 'da':
                        self.assertNotIn('Skriv til os:', html)
                        self.assertIn('Privatliv', html)
                        self.assertIn('Vilkår', html)
                        self.assertIn('Alle rettigheder forbeholdes.', html)
                        self.assertIn('aria-label="Juridiske links"', html)
                    else:
                        self.assertNotIn('Email us:', html)
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

    def test_secondary_page_navigation_auto_hides_on_scroll(self):
        header_script_response = self.client.get('/static/js/site-header.js')
        header_script = header_script_response.get_data(as_text=True)
        header_script_response.close()
        self.assertIn(
            "navbar?.classList.contains('site-navbar--inner')",
            header_script,
        )
        self.assertNotIn(
            "document.body.classList.contains('project-detail-page')",
            header_script,
        )
        self.assertIn("navbar.classList.add('navbar-hidden')", header_script)
        self.assertIn(
            "if (mobileMenu.classList.contains('open'))",
            header_script,
        )
        self.assertIn('event.detail > 0', header_script)
        self.assertIn('currentScrollY > 50', header_script)
        self.assertNotIn('currentScrollY > 120', header_script)
        self.assertIn('window.requestAnimationFrame', header_script)
        self.assertIn("{ passive: true }", header_script)
        self.assertIn('reducedMotionMedia.matches', header_script)

        css_response = self.client.get('/static/site-refresh.css')
        css = css_response.get_data(as_text=True)
        css_response.close()
        self.assertIn(
            '.content-page .site-navbar--inner.navbar-hidden',
            css,
        )
        self.assertIn(
            '.project-detail-page .site-navbar--inner.navbar-hidden',
            css,
        )
        self.assertRegex(
            css,
            r'\.content-page \.site-navbar--inner,\s+'
            r'\.project-detail-page \.site-navbar--inner \{\s+'
            r'position: sticky;',
        )
        self.assertRegex(
            css,
            r'\.content-page \{[\s\S]*?overflow-x: clip;',
        )
        self.assertIn('transform: translateY(calc(-100% - 8px))', css)
        self.assertIn('.site-navbar.navbar-hidden', css)
        self.assertIn('transform: none !important', css)

    def test_active_service_pages_render_their_intended_structure_in_both_languages(self):
        service_paths = (
            '/services/dataanalyse',
            '/services/forretningsudvikling',
            '/services/automatisering',
            '/services/it-produktudvikling',
        )

        for language in ('da', 'en'):
            self._switch_language(language)
            for path in service_paths:
                with self.subTest(language=language, path=path):
                    html = self.client.get(path).get_data(as_text=True)
                    self.assertEqual(html.count('class="service-hero"'), 1)
                    self.assertEqual(
                        html.count(
                            'js/site-header.js?v=site-review-20260730-header-fold'
                        ),
                        1,
                    )
                    self.assertEqual(
                        html.count('class="service-benefit-card"'),
                        3,
                    )
                    self.assertNotIn('class="service-step-number"', html)
                    self.assertNotIn('class="content-section-number"', html)
                    self.assertNotIn('class="content-eyebrow"', html)
                    expected_list_items = {
                        '/services/dataanalyse': 4,
                        '/services/automatisering': 8,
                    }.get(path, 7)
                    self.assertEqual(
                        len(re.findall(r'<li(?:\s|>)', html)),
                        expected_list_items,
                    )
                    expected_story_sections = (
                        2 if path == '/services/dataanalyse' else 3
                    )
                    self.assertEqual(
                        html.count('class="service-story-section'),
                        expected_story_sections,
                    )
                    self.assertNotIn('project-contact-section', html)
                    self.assertNotIn('service-contact-section', html)
                    self.assertNotIn('project-contact-actions', html)
                    self.assertNotIn('class="content-cta"', html)
                    self.assertNotIn('\ufffd', html)
                    self.assertNotIn('\u2013', html)
                    self.assertNotIn('\u2014', html)

                    hero = re.search(
                        r'<header class="service-hero">([\s\S]*?)</header>',
                        html,
                    )
                    self.assertIsNotNone(hero)
                    self.assertNotIn('button', hero.group(1).lower())
                    self.assertNotIn('content-primary-button', hero.group(1))
                    self.assertNotIn('project-button', hero.group(1))

                    if path == '/services/dataanalyse':
                        self.assertNotIn('class="service-examples"', html)
                        self.assertNotIn(
                            'Eksempler'
                            if language == 'da'
                            else 'Examples',
                            html,
                        )
                        self.assertNotIn(
                            'class="content-secondary-button"',
                            html,
                        )

        data_page = self.client.get('/services/dataanalyse').get_data(as_text=True)
        automation_page = self.client.get(
            '/services/automatisering',
        ).get_data(as_text=True)
        business_page = self.client.get(
            '/services/forretningsudvikling',
        ).get_data(as_text=True)
        product_page = self.client.get(
            '/services/it-produktudvikling',
        ).get_data(as_text=True)

        self.assertNotIn('href="/projekter/2"', data_page)
        self.assertNotIn('href="/projekter/', automation_page)
        self.assertNotIn('href="/projekter/', business_page)
        self.assertNotIn('href="/projekter/', product_page)

    def test_service_copy_is_plain_and_consistent_in_both_languages(self):
        self._switch_language('da')
        danish_pages = {
            path: self.client.get(path).get_data(as_text=True)
            for path in (
                '/services/dataanalyse',
                '/services/forretningsudvikling',
                '/services/automatisering',
                '/services/it-produktudvikling',
            )
        }

        self.assertIn('Indsamling og analyse af data', danish_pages['/services/dataanalyse'])
        self.assertIn('Hvad analysen omfatter', danish_pages['/services/dataanalyse'])
        self.assertIn('Fra spørgsmål til resultat', danish_pages['/services/dataanalyse'])
        self.assertIn('Et resultat til videre brug', danish_pages['/services/dataanalyse'])
        self.assertIn('grafer, tabeller, kort eller en kort rapport', danish_pages['/services/dataanalyse'])
        self.assertNotIn('Et resultat med forbehold', danish_pages['/services/dataanalyse'])
        self.assertNotIn('Fra data til klare valg', danish_pages['/services/dataanalyse'])
        self.assertIn(
            '<h1>Analyse, prioritering og planlægning</h1>',
            danish_pages['/services/forretningsudvikling'],
        )
        self.assertIn('Hvad arbejdet omfatter', danish_pages['/services/forretningsudvikling'])
        self.assertIn('Fra udfordring til plan', danish_pages['/services/forretningsudvikling'])
        self.assertIn('Automatisering af arbejdsgange', danish_pages['/services/automatisering'])
        self.assertIn('Mindre manuel håndtering', danish_pages['/services/automatisering'])
        self.assertIn(
            'kan AI indgå som et afgrænset trin',
            danish_pages['/services/automatisering'],
        )
        self.assertIn(
            'Sortering og udtræk af oplysninger fra tekst med AI',
            danish_pages['/services/automatisering'],
        )
        self.assertNotIn('Fjern det gentagne arbejde', danish_pages['/services/automatisering'])
        self.assertIn(
            '<h1>Udvikling af software til arbejdsgange</h1>',
            danish_pages['/services/it-produktudvikling'],
        )
        self.assertIn('Hvad udviklingen omfatter', danish_pages['/services/it-produktudvikling'])
        self.assertIn('Fra behov til software', danish_pages['/services/it-produktudvikling'])
        self.assertIn(
            'forkorte udviklingstiden og reducere omkostningerne',
            danish_pages['/services/it-produktudvikling'],
        )
        self.assertIn(
            'Kode lavet med hjælp fra AI bliver gennemgået og testet som anden kode',
            danish_pages['/services/it-produktudvikling'],
        )
        self.assertNotIn(
            'Software, der passer til arbejdet',
            danish_pages['/services/it-produktudvikling'],
        )

        self._switch_language('en')
        english_pages = {
            path: self.client.get(path).get_data(as_text=True)
            for path in danish_pages
        }
        self.assertIn('Data collection and analysis', english_pages['/services/dataanalyse'])
        self.assertIn('What the analysis includes', english_pages['/services/dataanalyse'])
        self.assertIn('From question to result', english_pages['/services/dataanalyse'])
        self.assertIn('A result for further use', english_pages['/services/dataanalyse'])
        self.assertIn('charts, tables, maps or a short report', english_pages['/services/dataanalyse'])
        self.assertNotIn('A result with caveats', english_pages['/services/dataanalyse'])
        self.assertNotIn('From data to clear decisions', english_pages['/services/dataanalyse'])
        self.assertIn(
            '<h1>Analysis, prioritisation and planning</h1>',
            english_pages['/services/forretningsudvikling'],
        )
        self.assertIn('What the work includes', english_pages['/services/forretningsudvikling'])
        self.assertIn('From challenge to plan', english_pages['/services/forretningsudvikling'])
        self.assertIn('Workflow automation', english_pages['/services/automatisering'])
        self.assertIn('Less manual handling', english_pages['/services/automatisering'])
        self.assertIn(
            'AI can be used as a clearly defined step',
            english_pages['/services/automatisering'],
        )
        self.assertIn(
            'Sorting and extracting information from text with AI',
            english_pages['/services/automatisering'],
        )
        self.assertNotIn('Remove repetitive work', english_pages['/services/automatisering'])
        self.assertIn(
            '<h1>Software development for workflows</h1>',
            english_pages['/services/it-produktudvikling'],
        )
        self.assertIn('What development includes', english_pages['/services/it-produktudvikling'])
        self.assertIn('From need to software', english_pages['/services/it-produktudvikling'])
        self.assertIn(
            'shorten development time and reduce costs',
            english_pages['/services/it-produktudvikling'],
        )
        self.assertIn(
            'Code produced with AI support is reviewed and tested',
            english_pages['/services/it-produktudvikling'],
        )
        self.assertNotIn(
            'Software that fits the work',
            english_pages['/services/it-produktudvikling'],
        )

        for html in (*danish_pages.values(), *english_pages.values()):
            self.assertNotIn('\u2013', html)
            self.assertNotIn('\u2014', html)

    def test_service_layout_clears_divider_and_uses_responsive_rules(self):
        css_response = self.client.get('/static/site-refresh.css')
        css = css_response.get_data(as_text=True)
        css_response.close()

        self.assertIn('/* Unified editorial layout for all service articles. */', css)
        self.assertIn(
            '/* All four service articles share the same restrained article layout. */',
            css,
        )
        self.assertIn(
            '.service-page--it-produktudvikling .service-hero-inner,',
            css,
        )
        self.assertIn(
            '.service-page--forretningsudvikling .service-hero-inner,',
            css,
        )
        self.assertNotIn(
            '/* A tighter editorial layout for the Dataanalyse service article. */',
            css,
        )
        self.assertRegex(
            css,
            r'\.service-page \.service-article-wrap \{[\s\S]*?'
            r'padding: clamp\(64px, 8vw, 112px\) '
            r'clamp\(18px, 4vw, 48px\);',
        )
        self.assertRegex(
            css,
            r'\.service-page \.service-article-layout \{[\s\S]*?'
            r'width: min\(100%, 960px\);',
        )
        self.assertRegex(
            css,
            r'\.service-page \.service-story-section \{[\s\S]*?'
            r'width: min\(100%, 760px\);',
        )
        self.assertRegex(
            css,
            r'\.service-page section \+ section::before \{\s*'
            r'display: none;\s*content: none;',
        )
        self.assertRegex(
            css,
            r'\.service-page \.service-benefit-card::before \{\s*'
            r'display: none;\s*content: none;',
        )
        self.assertIn(
            '.service-page--dataanalyse .service-hero h1::before,',
            css,
        )
        self.assertRegex(
            css,
            r'@media \(min-width: 760px\)[\s\S]*?'
            r'\.service-page \.service-step-list \{\s*'
            r'grid-template-columns: repeat\(2, minmax\(0, 1fr\)\);',
        )
        self.assertRegex(
            css,
            r'@media \(min-width: 900px\)[\s\S]*?'
            r'\.service-page \.service-hero-inner \{\s*display: grid;',
        )
        self.assertRegex(
            css,
            r'\.service-page--automatisering \.service-hero \{\s*'
            r'padding-block: clamp\(40px, 5vw, 68px\);',
        )
        self.assertRegex(
            css,
            r'\.service-page--dataanalyse \.service-hero-inner,\s*'
            r'\.service-page--dataanalyse \.service-article-layout,\s*'
            r'\.service-page--automatisering \.service-hero-inner,\s*'
            r'\.service-page--automatisering \.service-article-layout \{\s*'
            r'width: min\(100%, 1080px\);',
        )
        self.assertRegex(
            css,
            r'\.service-page--automatisering \.service-hero-inner,\s*'
            r'\.service-page--automatisering \.service-article-layout \{\s*'
            r'width: min\(100%, 1080px\);',
        )
        self.assertIn('border-radius: 14px', css)
        self.assertRegex(
            css,
            r'\.unified-footer \{[\s\S]*?text-align: left;',
        )

    def test_article_pages_do_not_render_bottom_contact_prompts(self):
        article_paths = (
            '/projekter/1',
            '/projekter/2',
            '/services/dataanalyse',
            '/services/forretningsudvikling',
            '/services/automatisering',
            '/services/it-produktudvikling',
        )

        for language in ('da', 'en'):
            self._switch_language(language)
            for path in article_paths:
                with self.subTest(language=language, path=path):
                    html = self.client.get(path).get_data(as_text=True)
                    self.assertNotIn('project-contact-section', html)
                    self.assertNotIn('service-contact-section', html)
                    self.assertNotIn('project-contact-actions', html)
                    self.assertNotIn('service-cta-title', html)
                    self.assertNotIn('project-contact-title', html)

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
            '/* Homepage services: quiet, responsive list cards inspired by '
            'the supplied reference. */',
            css,
        )
        self.assertIn(
            'grid-template-columns: repeat(2, minmax(0, 1fr))',
            css,
        )
        self.assertRegex(
            css,
            r'\.home-page #services \.services-grid \{[\s\S]*?'
            r'grid-auto-rows: 1fr;',
        )
        self.assertRegex(
            css,
            r'\.home-page #services \.service-card \{[\s\S]*?'
            r'grid-template-columns: 56px minmax\(0, 1fr\) 22px;[\s\S]*?'
            r'border: 1px solid rgba\(226, 232, 240, 0\.8\);[\s\S]*?'
            r'border-radius: 16px;[\s\S]*?'
            r'box-shadow: 0 10px 30px rgba\(15, 23, 42, 0\.08\);[\s\S]*?'
            r'transform: none;',
        )
        self.assertRegex(
            css,
            r'@media \(min-width: 960px\)[\s\S]*?'
            r'\.home-page #services \.services-grid \{[\s\S]*?'
            r'grid-template-columns: repeat\(2, minmax\(0, 1fr\)\);',
        )
        self.assertRegex(
            css,
            r'@media \(max-width: 600px\)[\s\S]*?'
            r'\.home-page #services \.service-card \{[\s\S]*?'
            r'grid-template-columns: 50px minmax\(0, 1fr\) 20px;',
        )
        self.assertIn('.home-page #services .service-card-arrow', css)

        expected_cards = {
            'da': (
                ('/services/automatisering', 'Automatisering'),
                ('/services/dataanalyse', 'Dataanalyse'),
                ('/services/forretningsudvikling', 'Forretningsudvikling'),
                ('/services/it-produktudvikling', 'IT-produktudvikling'),
            ),
            'en': (
                ('/services/automatisering', 'Automation'),
                ('/services/forretningsudvikling', 'Business development'),
                ('/services/dataanalyse', 'Data analysis'),
                ('/services/it-produktudvikling', 'IT product development'),
            ),
        }
        expected_summaries = {
            'da': (
                'Automatisering af faste og gentagne arbejdsgange.',
                'Indsamling, strukturering og analyse af data.',
                'Analyse af arbejdsgange, muligheder og prioriteringer.',
                'Udvikling af software til konkrete arbejdsgange.',
            ),
            'en': (
                'Automation of fixed, repetitive workflow steps.',
                'Analysis of workflows, opportunities and priorities.',
                'Collection, structuring and analysis of data.',
                'Development of software for specific workflows.',
            ),
        }
        card_pattern = re.compile(
            r'<a href="([^"]+)"\s+class="service-card[^"]*">'
            r'([\s\S]*?)</a>',
        )

        for language, expected in expected_cards.items():
            self._switch_language(language)
            html = self.client.get('/').get_data(as_text=True)
            cards = card_pattern.findall(html)
            rendered = tuple(
                (
                    href,
                    re.search(r'<h3>(.*?)</h3>', body).group(1),
                )
                for href, body in cards
            )
            summaries = tuple(
                re.search(r'<p>(.*?)</p>', body).group(1)
                for _, body in cards
            )
            with self.subTest(language=language):
                self.assertEqual(rendered, expected)
                self.assertEqual(summaries, expected_summaries[language])
                self.assertTrue(
                    all(len(summary.rstrip('.').split()) == 6 for summary in summaries),
                )
                self.assertEqual(html.count('class="service-card-arrow"'), 4)
                self.assertEqual(html.count('class="service-icon"'), 4)

    def test_homepage_hero_has_no_action_buttons_in_either_language(self):
        for language in ('da', 'en'):
            self._switch_language(language)
            html = self.client.get('/').get_data(as_text=True)
            with self.subTest(language=language):
                self.assertNotIn('home-hero-actions', html)
                self.assertNotIn('home-hero-button', html)
                if language == 'da':
                    self.assertIn(
                        'Vi automatiserer arbejdsgange, analyserer data og '
                        'bygger digitale løsninger.',
                        html,
                    )
                    self.assertNotIn('der passer til jeres hverdag', html)
                else:
                    self.assertIn(
                        'We automate workflows, analyse data and build '
                        'digital tools.',
                        html,
                    )
                    self.assertNotIn('that fit the way you work', html)

    def test_homepage_contact_copy_uses_plain_punctuation(self):
        self._switch_language('da')
        html = self.client.get('/').get_data(as_text=True)
        self.assertIn(
            'Har I en opgave, vi skal se på, eller et spørgsmål? '
            'Ring, skriv eller find os på LinkedIn.',
            html,
        )
        self.assertNotIn(
            'Har I en opgave, vi skal se på – eller et spørgsmål?',
            html,
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

    def test_about_contact_connector_is_decorative_in_both_languages(self):
        for language in ('da', 'en'):
            self._switch_language(language)
            html = self.client.get('/').get_data(as_text=True)
            connector = re.search(
                r'<svg\b[^>]*class="about-contact-path"[^>]*>'
                r'[\s\S]*?</svg>',
                html,
            )
            with self.subTest(language=language):
                self.assertIsNotNone(connector)
                self.assertEqual(html.count('class="about-contact-path"'), 1)
                self.assertIn('role="presentation"', connector.group(0))
                self.assertIn('focusable="false"', connector.group(0))
                self.assertIn('aria-hidden="true"', connector.group(0))
                self.assertIn('about-contact-path__guide', connector.group(0))
                self.assertIn('about-contact-path__reveal', connector.group(0))
                self.assertIn('about-contact-path__ribbon', connector.group(0))
                self.assertIn('id="aboutContactRevealMask"', connector.group(0))
                self.assertIn('pathLength="1"', connector.group(0))
                self.assertIn(
                    'mask="url(#aboutContactRevealMask)"',
                    connector.group(0),
                )
                self.assertNotIn('about-contact-path__core', connector.group(0))
                self.assertIn('data-path-x="1056"', html)
                self.assertIn('data-path-width="105"', html)

    def test_about_contact_connector_uses_live_responsive_geometry(self):
        script_response = self.client.get(
            '/static/js/about-contact-path.js?v=20260728'
        )
        self.assertEqual(script_response.status_code, 200)
        script = script_response.get_data(as_text=True)
        script_response.close()

        self.assertIn("document.querySelector('.about-datara-media')", script)
        self.assertIn(
            "document.querySelector('#kontakt .contact-layout')",
            script,
        )
        self.assertIn('getBoundingClientRect()', script)
        self.assertIn("connector.setAttribute(", script)
        self.assertIn("'viewBox'", script)
        self.assertIn("guide.setAttribute('d', pathData)", script)
        self.assertIn("reveal.setAttribute('d', pathData)", script)
        self.assertIn('buildTaperedRibbon', script)
        self.assertIn('getTotalLength()', script)
        self.assertIn('getPointAtLength(', script)
        self.assertIn("ribbon.setAttribute(", script)
        self.assertIn("'--connector-roll-duration'", script)
        self.assertIn("revealMask.setAttribute(", script)
        self.assertIn("connector.dataset.routeSide = 'right'", script)
        self.assertNotIn("routeSide = 'left'", script)
        self.assertIn('const seamHoldDistance = clamp(', script)
        self.assertIn('const taperProgress = clamp(', script)
        self.assertIn('const imagePathSlope = 0.55', script)
        self.assertIn('const pathStartX =', script)
        self.assertIn('const seamJoinDistance = Math.hypot(', script)
        self.assertIn('seamPoint.distance', script)
        self.assertIn('`L ${round(startX)} ${connectorOverlap}`', script)
        self.assertIn('const polygonPoints = [', script)
        self.assertNotIn('curveThroughPoints', script)
        self.assertIn('const connectorOverlap = 2', script)
        self.assertIn("connector.classList.toggle('is-disabled'", script)
        self.assertIn('layoutRect.width / 2', script)
        self.assertIn('IntersectionObserver', script)
        self.assertIn('ResizeObserver', script)
        self.assertIn("image.addEventListener('load'", script)
        self.assertNotIn("document.createElement('canvas')", script)

    def test_about_contact_connector_remains_visible_and_non_interactive(self):
        refresh_response = self.client.get('/static/site-refresh.css')
        refresh_css = refresh_response.get_data(as_text=True)
        refresh_response.close()
        legacy_response = self.client.get('/static/style.css')
        legacy_css = legacy_response.get_data(as_text=True)
        legacy_response.close()

        connector_rule = re.search(
            r'\.about-contact-path \{[\s\S]*?\}',
            refresh_css,
        )
        self.assertIsNotNone(connector_rule)
        self.assertIn('pointer-events: none', connector_rule.group(0))
        self.assertIn('overflow: visible', connector_rule.group(0))
        self.assertIn('object-position: center bottom', refresh_css)
        self.assertIn('@media (prefers-reduced-motion: reduce)', refresh_css)
        self.assertIn('stroke-dasharray: 1', refresh_css)
        self.assertIn('stroke-dashoffset: 1', refresh_css)
        self.assertIn(
            'var(--connector-roll-duration, 3s)',
            refresh_css,
        )
        self.assertIn('@media (max-width: 860px)', refresh_css)
        self.assertRegex(
            refresh_css,
            r'@media \(max-width: 860px\) \{[\s\S]*?'
            r'\.about-contact-path \{[\s\S]*?display: none;',
        )
        self.assertRegex(
            refresh_css,
            r'\.about-contact-path\.animate-in '
            r'\.about-contact-path__reveal \{[\s\S]*?'
            r'stroke-dashoffset: 0;',
        )
        ribbon_rule = re.search(
            r'\.about-contact-path__ribbon \{[\s\S]*?\}',
            refresh_css,
        )
        self.assertIsNotNone(ribbon_rule)
        self.assertIn('opacity: 1', ribbon_rule.group(0))
        self.assertNotIn('transition:', ribbon_rule.group(0))
        self.assertNotIn('.about-contact-path__core', refresh_css)
        self.assertNotIn('.about-path-line', legacy_css)

    def test_heating_article_results_use_compact_responsive_maps(self):
        css_response = self.client.get('/static/style.css')
        css = css_response.get_data(as_text=True)
        css_response.close()

        layout_rule = re.search(
            r'\.project-article-layout \{([^}]*)\}',
            css,
        )
        self.assertIsNotNone(layout_rule)
        self.assertIn('width: min(100%, 960px)', layout_rule.group(1))
        self.assertIn('display: block', layout_rule.group(1))

        figure_rule = re.search(
            r'\.project-story-figure \{([^}]*)\}',
            css,
        )
        self.assertIsNotNone(figure_rule)
        self.assertIn('width: min(100%, 620px)', figure_rule.group(1))
        self.assertIn('border-radius: 14px', figure_rule.group(1))
        self.assertIn(
            'box-shadow: 0 8px 22px rgba(15, 23, 42, 0.06)',
            figure_rule.group(1),
        )
        self.assertRegex(
            css,
            r'\.project-story-figure img \{[\s\S]*?height: auto;',
        )
        self.assertRegex(
            css,
            r'@media \(min-width: 900px\)[\s\S]*?'
            r'\.project-story-section--with-figure \{[\s\S]*?'
            r'grid-template-columns: minmax\(250px, 0\.74fr\) '
            r'minmax\(380px, 1\.26fr\);',
        )
        self.assertRegex(
            css,
            r'\.project-story-section--with-figure '
            r'\.project-story-figure \{[\s\S]*?max-width: 520px;',
        )
        self.assertRegex(
            css,
            r'\.project-detail-page--lavtemperaturfjernvarme\s*'
            r'\.project-story-section:not\('
            r'\.project-story-section--with-figure\) \{\s*'
            r'width: 100%;',
        )
        self.assertRegex(
            css,
            r'\.project-detail-page--lavtemperaturfjernvarme\s*'
            r'\.project-story-section:not\('
            r'\.project-story-section--with-figure\)\s*p \{\s*'
            r'max-width: 76ch;',
        )

        section_divider_rule = re.search(
            r'\.project-story-section \+ \.project-story-section '
            r'\{([^}]*)\}',
            css,
        )
        self.assertIsNotNone(section_divider_rule)
        self.assertNotIn('border', section_divider_rule.group(1))
        self.assertRegex(
            css,
            r'\.project-story-section \{[\s\S]*?'
            r'width: min\(100%, 760px\);',
        )

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
