"""Freeze the Flask site into a static build for GitHub Pages.

Usage:
    python freeze.py                       Production build in docs/ (root-absolute URLs).
    python freeze.py --prefix /optimatix   Preview build for simnyborg.github.io/optimatix/.
    python freeze.py --cname datara.dk     Also write docs/CNAME (use for the final cutover build).

The Danish pages keep their exact live URLs (extensionless files, e.g.
docs/services/dataanalyse.html serves /services/dataanalyse). English pages
live under /en/. Unknown paths serve the Danish root 404.html; when the
requested path is under /en/ it redirects to the real English 404 page at
/en/404 (built as en/404.html).
"""
import argparse
import re
import shutil
from pathlib import Path

from app import app

ROOT = Path(__file__).resolve().parent
STATIC_SRC = ROOT / 'static'
DEST = ROOT / 'docs'
DEST_TMP = ROOT / 'docs.tmp'

DA_PAGES = [
    '/',
    '/services/dataanalyse',
    '/services/forretningsudvikling',
    '/services/automatisering',
    '/services/it-produktudvikling',
    '/projekter/1',
    '/projekter/2',
    '/privatliv',
    '/cookies',
    '/vilkar',
]
EN_PAGES = ['/en/' if p == '/' else '/en' + p for p in DA_PAGES]

# The parked "Indsigt" feature (vendor libs + insights.js) stays in the repo
# but is not referenced by any live page, so it is left out of the build.
EXCLUDED_STATIC_DIRS = {'vendor'}
EXCLUDED_STATIC_FILES = {('js', 'insights.js')}


def out_file(url: str) -> Path:
    if url == '/':
        return DEST_TMP / 'index.html'
    if url == '/en/':
        return DEST_TMP / 'en' / 'index.html'
    return DEST_TMP / Path(url.strip('/') + '.html')


def prefix_html(html: str, prefix: str) -> str:
    if not prefix:
        return html
    return re.sub(
        r'\b(href|src|action)="(/(?!/)[^"]*)"',
        lambda m: f'{m.group(1)}="{prefix}{m.group(2)}"',
        html,
    )


def prefix_css(css: str, prefix: str) -> str:
    if not prefix:
        return css
    return re.sub(
        r"url\((['\"]?)(/(?!/)[^)'\"]*)\1\)",
        lambda m: f'url({m.group(1)}{prefix}{m.group(2)}{m.group(1)})',
        css,
    )


def build(prefix: str = '', cname: str = '') -> None:
    if prefix and (not prefix.startswith('/') or ':' in prefix or prefix.endswith('/')):
        raise SystemExit(
            f'Ugyldigt prefix {prefix!r} - skal starte med "/" og ikke ende paa "/" '
            '(brug fx --prefix /optimatix; i Git Bash kraves MSYS_NO_PATHCONV=1)'
        )

    if DEST_TMP.exists():
        shutil.rmtree(DEST_TMP)
    DEST_TMP.mkdir()

    client = app.test_client()

    def fetch(url: str, expect: int = 200) -> bytes:
        response = client.get(url)
        if response.status_code != expect:
            raise SystemExit(f'{url} returned {response.status_code}, expected {expect}')
        data = response.get_data()
        response.close()
        return data

    for url in DA_PAGES + EN_PAGES:
        html = prefix_html(fetch(url).decode('utf-8'), prefix)
        path = out_file(url)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(html, encoding='utf-8', newline='')

    # Bilingual 404: GitHub Pages serves the root 404.html (Danish) for every
    # unknown path. The English 404 is a real page at /en/404; a tiny script
    # in the Danish document redirects there when the path is under /en/.
    # /404 is used as the frozen "current path" so the language toggles
    # become the tidy pair /en/404 <-> /404.
    da_404 = prefix_html(fetch('/404', expect=404).decode('utf-8'), prefix)
    en_404 = prefix_html(fetch('/en/404', expect=404).decode('utf-8'), prefix)
    redirect = (
        '<script>(function () {'
        f'var p = {prefix!r};'
        'var path = location.pathname;'
        "if (path !== p + '/en' && path.indexOf(p + '/en/') !== 0) return;"
        "if (path === p + '/en/404') return;"
        "location.replace(p + '/en/404');"
        '})();</script>'
    )
    (DEST_TMP / '404.html').write_text(
        da_404.replace('</head>', redirect + '\n</head>', 1), encoding='utf-8', newline=''
    )
    (DEST_TMP / 'en' / '404.html').write_text(en_404, encoding='utf-8', newline='')

    (DEST_TMP / 'robots.txt').write_bytes(fetch('/robots.txt'))
    (DEST_TMP / 'sitemap.xml').write_bytes(fetch('/sitemap.xml'))
    (DEST_TMP / 'favicon.ico').write_bytes(fetch('/favicon.ico'))

    for source in STATIC_SRC.rglob('*'):
        if not source.is_file():
            continue
        relative = source.relative_to(STATIC_SRC)
        if relative.parts[0] in EXCLUDED_STATIC_DIRS or relative.parts in EXCLUDED_STATIC_FILES:
            continue
        target = DEST_TMP / 'static' / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        if relative.suffix == '.css':
            target.write_text(
                prefix_css(source.read_text(encoding='utf-8'), prefix),
                encoding='utf-8',
                newline='',
            )
        elif relative.suffix == '.webmanifest' and prefix:
            target.write_text(
                source.read_text(encoding='utf-8').replace('"/static/', f'"{prefix}/static/'),
                encoding='utf-8',
                newline='',
            )
        else:
            shutil.copyfile(source, target)

    (DEST_TMP / '.nojekyll').write_text('', encoding='utf-8')
    if cname:
        (DEST_TMP / 'CNAME').write_text(cname + '\n', encoding='utf-8')

    # Atomic-ish swap: only replace docs/ once the new build is complete.
    if DEST.exists():
        shutil.rmtree(DEST)
    DEST_TMP.rename(DEST)

    pages = len(DA_PAGES + EN_PAGES)
    print(f'Built {pages} pages + 404/sitemap/robots into {DEST} '
          f'(prefix={prefix or "none"}, cname={cname or "none"})')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--prefix', default='', help='URL prefix, e.g. /optimatix for the Pages preview')
    parser.add_argument('--cname', default='', help='Custom domain to write into docs/CNAME')
    arguments = parser.parse_args()
    build(prefix=arguments.prefix, cname=arguments.cname)
