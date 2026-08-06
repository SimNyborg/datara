# Datara – Hjemmeside

Datara.dk er et statisk site, der hostes gratis på GitHub Pages. Indholdet
vedligeholdes stadig som en lille Flask-app (templates + `site_content.py` +
`app.py`), og `freeze.py` "fryser" appen til færdige HTML-filer i `docs/`,
som GitHub Pages serverer.

## Sådan retter du indhold

1. Redigér teksterne i `site_content.py` / `app.py` (PROJECTS) eller
   templates i `templates/`.
2. Byg det statiske site:

   ```powershell
   python freeze.py --cname datara.dk
   ```

3. Kør testene: `python -m pytest tests -q`
4. Commit og push til `main` – GitHub Pages deployer automatisk `docs/`.

## Sprog

Dansk ligger på rod-URL'erne (`/`, `/services/...`), engelsk under `/en/...`.
Sproget styres af URL'en – sprogknappen i menuen linker til søstersiden.
`404.html` indeholder begge sprog og viser engelsk for stier under `/en/`.

## Preview uden domæne

`python freeze.py --prefix /optimatix` bygger en version, der virker på
`https://simnyborg.github.io/optimatix/` (bruges kun til test/preview —
byg altid produktionsversionen med `--cname datara.dk` inden push).

## Parkeret

"Indsigt"-sektionen (Chart.js/Leaflet, `static/vendor/`, `static/js/insights.js`)
er midlertidigt deaktiveret via kommentarer i `templates/index.html` og
udelades af det statiske build, indtil den genaktiveres.

## SEO

Sitemap: `https://datara.dk/sitemap.xml` (genereres af `freeze.py`).
Google Search Console overvåger `https://datara.dk` og validerer sitemappet.
