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

`python freeze.py --prefix /datara` bygger en version, der virker på
`https://simnyborg.github.io/datara/` (bruges kun til test/preview —
byg altid produktionsversionen med `--cname datara.dk` inden push).

## Affaldskortet (/affaldskort/)

Projektet om affaldsdebatten har to dele:

- Projektsiden `/projekter/affaldsdebatten` (tekst i `affaldskort_content.py`).
  Nøgletallene læses fra `apps/affaldskort/stats.json`.
- Det interaktive kort i `apps/affaldskort/`, som `freeze.py` kopierer til
  `docs/affaldskort/`. Filerne her er genereret: ret dem ikke i hånden.

Begge opdateres fra Affaldskort-pipelinen (OneDrive, `Affaldskort/pipeline`):

```powershell
python publish_datara.py            # byg offentlig udgave, kopiér, frys, test, commit og push
python publish_datara.py --no-push  # samme, men uden commit/push
```

Den offentlige udgave viser ikke nyhedsartiklernes egen tekst (kun titel,
kilde og link) og udelader de interne arbejdsnoter fra dashboardet.

## Parkeret

"Indsigt"-sektionen (Chart.js/Leaflet, `static/vendor/`, `static/js/insights.js`)
er midlertidigt deaktiveret via kommentarer i `templates/index.html` og
udelades af det statiske build, indtil den genaktiveres.

## SEO

Sitemap: `https://datara.dk/sitemap.xml` (genereres af `freeze.py`).
Google Search Console overvåger `https://datara.dk` og validerer sitemappet.
