# Friday 27 November 2026: 48 stories, 3 drawn scenes, map, UTC timeline and a date check

One image that sums up the world's news of Friday 27 November 2026.

- **48 sourced stories** across 7 regions, each marked with per-story confidence (●●● high / ●●○ medium / ●○○ low) and its source outlet.
- **Lead story:** the drone strike in Kuwait that killed two Italian technicians, with Iran denying responsibility (01:03 UTC, NYT/BBC/Reuters).
- **3 drawn scenes:** the Kuwait night skyline under a drone, the US Thanksgiving storm, and the Gukesh–Sindarov World Chess Championship Game 3 draw.
- **World map** with 21 hotspots plotted, a **UTC timeline** of the day, a **day-in-numbers** bar, and a **date check** badge — every story was first reported on 27 November 2026.
- **Image:** 1024×1024 PNG, 171,039 bytes (drawn by code with `draw.py`, PIL, fixed seed — no photos, no network).

## Run

```sh
python3 draw.py        # regenerates entry.png deterministically
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts   # writes out/entry.png
```

## Sources

NYT, BBC, Reuters, Guardian, The Times of India, India Today, Al Jazeera, ONS, EU, FCC, S&P, Goldman Sachs, and others — listed in the image footer. The Russian casualty figure (1,645,899) is a Ukrainian General Staff claim, marked as such in the image.

Built for the make.fun bounty `news-image-20261127` (pot $100, top 50 share the prize).
