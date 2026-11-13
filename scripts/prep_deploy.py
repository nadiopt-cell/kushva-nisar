from pathlib import Path
R=Path(r"E:\ai_project\30days_challenge\day14_borges")
# workflow
wf=R/".github"/"workflows"; wf.mkdir(parents=True,exist_ok=True)
(wf/"pages.yml").write_text("""name: Deploy interactive map

on:
  push:
    branches: [main]
    paths:
      - 'web/**'
      - '.github/workflows/pages.yml'
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: pages
  cancel-in-progress: true

jobs:
  deploy:
    runs-on: ubuntu-latest
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    steps:
      - uses: actions/checkout@v4
      - name: Setup Pages
        uses: actions/configure-pages@v5
        with:
          enablement: true
      - name: Upload site
        uses: actions/upload-pages-artifact@v3
        with:
          path: web
      - name: Deploy
        id: deployment
        uses: actions/deploy-pages@v4
""",encoding="utf-8")
# readme
readme="""# Карта, которая почти стала территорией

**#30DayMapChallenge 2026 · Day 14 — Borgesian map**
Крупный ветровал + NISAR · Кушва, Свердловская область · 22 июня 2026

**Живая карта:** https://nadiopt-cell.github.io/kushva-nisar/

## Что это

22 июня 2026 года через Кушву прошёл смерч. Спутниковые снимки показали, что смерчей было два:
первый — у Малой Лаи (16,5 км, более 200 га леса), второй — через город (29 км, до 700 м в ширину,
≥510 га ветровала). Суммарно — более 710 га, рекорд для Свердловской области в XXI веке.

Интерактивная карта показывает след на двух языках данных:

- **NISAR L-band** — когерентность HH между 20.06.2026 и 02.07.2026 (один 12-дневный цикл,
  трек 93D). Поваленный лес теряет когерентность почти полностью и светится медной лентой.
- **Sentinel-2 L2A** — оптика до/после, синтез SWIR (B12/B8/B4): 21.05.2026 и 28.07.2026.
- **Контур ветровала** — порог когерентности + оптический dNBR.
- **Вода** — всегда сверху, чтобы низкая когерентность водоёмов не читалась как ветровал.
- **Рельеф** — Copernicus DEM 30 м, поверх растров.

## Файлы

| Путь | Что |
|---|---|
| `web/` | интерактивная карта MapLibre GL JS |
| `output/poster_radar_ru.jpg` / `_en.jpg` | постер NISAR, RU / EN |
| `output/poster_optical_ru.jpg` / `_en.jpg` | постер Sentinel-2, RU / EN |
| `output/posters_contact.jpg` | контактный лист 2×2 |
| `output/social_posts.md` | тексты для ВК и LinkedIn |
| `scripts/` | подготовка данных и сборка карты |
| `data/` | исходные срезы (не в репозитории) |

## Данные

- **NISAR:** NASA/ISRO, L2 GCOV + GUNW PROVISIONAL V1, frequency A (L-band, 24 см), HH/HV,
  20 м · 20.06.2026 15:44 UTC и 02.07.2026 15:44 UTC · трек 93D · ASF DAAC.
- **Sentinel-2:** Copernicus/ESA, L2A, 10 м · 21.05.2026 и 28.07.2026.
- **DEM:** Copernicus DEM 30 м. **OSM:** © OpenStreetMap contributors.

## Локальный запуск

```bash
python -m http.server 8000 --directory web
```

Открыть http://127.0.0.1:8000/

## Метод

Оба продукта NISAR приведены к сетке UTM 40N (20 м), GCOV пересчитан в дБ, GUNW — в поле
когерентности. Контур построен по устойчивому порогу когерентности (≤0,285) в коридоре следа,
с оптической поддержкой dNBR (SWIR2/NIR), очищен морфологией и упрощён. Площадь, длина и ширина
измерены в равновеликой проекции. Оценка площади согласуется с опубликованной: ≥510 га.

## Лицензии

Код — MIT. Данные — согласно условиям NASA/ISRO (ASF DAAC), Copernicus/ESA и OpenStreetMap.
"""
(R/"README.md").write_text(readme,encoding="utf-8")
# gitignore additions
gi=(R/".gitignore").read_text(encoding="utf-8")
if "/output/*.png" not in gi:
    gi += "/output/*.png\n/output/*.pdf\n"
(R/".gitignore").write_text(gi,encoding="utf-8")
print("ok")