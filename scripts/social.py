# -*- coding: utf-8 -*-
from pathlib import Path
R=Path(r"E:\ai_project\30days_challenge\day14_borges")
(R/"output").mkdir(exist_ok=True)
text = """# Посты для соцсетей · «Карта, которая почти стала территорией»

## 1. ВКонтакте (основной пост)

**Карта, которая почти стала территорией**

22 июня 2026 года через Кушву прошёл смерч. Спутниковые снимки показали: смерчей было два. Первый — у Малой Лаи: 16,5 км и более 200 га леса. Второй — через город: 29 км, до 700 м в ширину и ≥510 га ветровала. Суммарно — более 710 га. Рекорд для Свердловской области в XXI веке.

Для #30DayMapChallenge (день 14 — Borgesian map) я собрал интерактивную карту этого следа. В основе — не оптика, а **NISAR L-band**: радар с длиной волны 24 см, который видит структуру леса сквозь облака.

Как это работает:
— NISAR снял Кушву 20 июня и 2 июля 2026 года — ровно один 12-дневный цикл, один и тот же трек 93D.
— Когерентность — мера того, насколько поверхность «согласна сама с собой» между двумя проходами радара. Поваленный лес теряет её почти полностью.
— На карте след светится медной лентой: лес перестал быть тем же лесом.
— Контур по L-band: 606 га, 29,8 км, до 760 м в ширину. Независимая оценка исследователей — ≥510 га (часть следа была под облаками), цифры сходятся.
— Оптика: Sentinel-2 до/после, синтез SWIR (B12/B8/B4). Облака не мешают радару — в этом и смысл.

Название — от Борхеса: карта, которая почти совпала с территорией. Здесь она совпала настолько, что виден каждый повреждённый участок леса.

🗺 Интерактивная карта: [ссылка]
🖼 Постер и GIF: [ссылка]

Данные: NASA/ISRO NISAR L2 GCOV + GUNW (ASF DAAC), Sentinel-2 L2A (Copernicus/ESA), Copernicus DEM, OpenStreetMap.

#30DayMapChallenge #BorgesianMap #NISAR #Sentinel2 #Кушва #ветровал #смерч #ГИС #дистанционноеЗондирование #Урал #карты

---

## 2. ВКонтакте (короткая версия для репоста)

**Карта, которая почти стала территорией**

Смерч 22 июня 2026 года оставил в лесах под Кушвой след длиной 29 км и площадью ≥510 га. На снимках NISAR L-band он светится медной лентой: радар видит, как лес теряет когерентность — «перестаёт быть собой» между двумя проходами.

Интерактивная карта: оптика до/после (Sentinel-2, SWIR), NISAR L-band, контур ветровала и сравнение «до/после».

🗺 [ссылка]

#30DayMapChallenge #NISAR #Кушва #ветровал #ГИС

---

## 3. LinkedIn (English, основной)

**A map that almost became the territory**

On 22 June 2026, a tornado cut through Kushva in the Middle Urals. Satellite imagery revealed that there were two tornadoes: one near Malaya Laya (16.5 km, >200 ha of forest), and one through Kushva itself — 29 km long, up to 700 m wide, ≥510 ha of windthrow. In total, >710 ha: a record for Sverdlovsk Oblast in the 21st century.

For Day 14 of #30DayMapChallenge (Borgesian map), I built an interactive map of the scar using **NISAR L-band** — a 24 cm radar that sees forest structure through clouds.

Method:
• NISAR GCOV + GUNW, 20 June and 2 July 2026 — exactly one 12-day repeat cycle, the same track 93D.
• Interferometric coherence measures how much the surface "agrees with itself" between passes. Windthrown forest loses it almost completely.
• The track appears as a bright copper band: the forest is no longer the same forest.
• L-band contour: 606 ha, 29.8 km, up to 760 m wide. The independent published estimate is ≥510 ha (part of the track was cloud-covered) — consistent.
• Optical context: Sentinel-2 before/after, SWIR composite (B12/B8/B4).

The title comes from Borges: a map that almost coincided with the territory. Here it coincides closely enough to show every damaged forest stand.

Why it matters: L-band coherence provides an all-weather, day/night damage map — useful for rapid post-storm assessment in remote boreal forest, where optical imagery is often blocked by clouds.

Interactive map: [link]
Poster and GIF: [link]

Data: NASA/ISRO NISAR L2 GCOV + GUNW (ASF DAAC), Sentinel-2 L2A (Copernicus/ESA), Copernicus DEM, OpenStreetMap.

#RemoteSensing #SAR #NISAR #Sentinel2 #GIS #Windthrow #Tornado #BorealForest #30DayMapChallenge #BorgesianMap #ClimateResilience

---

## 4. LinkedIn (короткая версия)

**A map that almost became the territory**

A tornado through Kushva (Middle Urals) on 22 June 2026 left a 29 km scar and ≥510 ha of windthrow. Using NISAR L-band coherence (20 June → 2 July 2026), the damaged forest appears as a bright copper band — the canopy literally stops agreeing with itself between two radar passes.

Interactive map with Sentinel-2 before/after (SWIR), NISAR L-band, contour and swipe comparison: [link]

#30DayMapChallenge #NISAR #SAR #RemoteSensing #BorealForest

---

## 5. Факты и источники (для проверки)

- Событие: 22.06.2026, Кушва, Свердловская область. Два смерча, связанных с одним мезоциклоном.
- Первый: у Малой Лаи, 16,5 км, >200 га, ширина до 570 м.
- Второй: через Кушву, 29 км, ≥510 га, ширина до 700 м; предварительно EF3/F3, скорость в воронке по оценкам >250 км/ч; на метеостанции порывы >33 м/с.
- Суммарно: >710 га; рекорд для Свердловской области в XXI веке (оценка ГИС-Центра ПГНИУ / А. Шихов).
- NISAR: L2 GCOV PROVISIONAL V1 (HH+HV, 20 м) и L2 GUNW PROVISIONAL V1 (HH coherence, 20 м), 20.06.2026 15:44 UTC и 02.07.2026 15:44 UTC, нисходящий трек 93D, frame 059.
- Sentinel-2 L2A: 21.05.2026 (0,6 % облачности) и 28.07.2026 (0,6–4,6 %), синтез SWIR B12/B8/B4.
- Наш контур: 606 га, 29,8 км, макс. ширина 761 м, средняя когерентность 0,29.
- Источники: Росгидромет (22.06.2026), КП-Урал (26.06.2026), Российская газета (26.06.2026), uralweb (28.06.2026), NASA Earthdata «Tracing a Tornado's Path of Destruction» (07.08.2026).
"""
(R/"output/social_posts.md").write_text(text,encoding="utf-8")
print("saved", (R/"output/social_posts.md").stat().st_size)