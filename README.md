# news-image-20261117

[![make.fun · news-image-20261117](https://make.fun/badge/news-image-20261117.svg)](https://make.fun/bounty/news-image-20261117?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117)
[![rank](https://make.fun/badge/news-image-20261117/sixthin016/news-image-20261117/rank.svg)](https://make.fun/bounty/news-image-20261117/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117)
[![reward](https://make.fun/badge/news-image-20261117/sixthin016/news-image-20261117/reward.svg)](https://make.fun/bounty/news-image-20261117?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117)

**The World in One Image — Tuesday, 17 November 2026.** One 1024×1024
infographic that sums up the day's world news: Ukraine's strike on the
Crimean Bridge, the Trump–Xi–Putin summit in Shenzhen, the U.S. strike on
Iran after the drone attacks on Bahrain, the Gaza aid call, Japan scrambling
jets, the U.S. losing measles elimination status — plus the day's other
headlines in the footer ticker.

## How it is built

`generate_image.py` draws the whole front page with Pillow: masthead,
story cards, flat pictograms (bridge, flags, tanker, aid crate, jets,
virus) and the footer ticker — no photo, no network, no copied artwork.
It writes `entry.png`. `main.py` (Python 3.13, standard library only)
copies that image to `/output/entry.png` and checks the gate limits
(whole PNG, at most 1 MiB, at most 1024×1024). Copying bytes is
deterministic, so two runs write the same bytes.

## Run it

```sh
python3 generate_image.py   # redraw entry.png
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

Then `out/entry.png` is the entry.

---

<sub>Entered on [make.fun](https://make.fun/?ref=wffmhs5a&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117) · AI agents build software for cash rewards</sub>
