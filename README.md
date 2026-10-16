# Divya Desam Yatra

A visual tour of the 108 Divya Desams, built as a gift for Sujatha.
Live at **https://sproutdev.github.io/divya-desam/**

## Putting it on her Pixel 6a

1. Open **Chrome** on the phone and go to `sproutdev.github.io/divya-desam`
   (or send her the link on WhatsApp and tap it).
2. Let the page load fully once while on Wi-Fi. It saves all 111 photos for offline use.
3. Tap the **three dots** (top right) and choose **Add to Home screen**, then **Install**.
4. An icon called **Divya Desam** appears on her home screen. It opens full screen, like an app.

Optional, so she only sees this one app:
- Settings > Digital Wellbeing or Settings > Accessibility has no kiosk mode on Pixel,
  but you can move the icon to the first home screen page and remove other clutter.
- Chrome > Settings > Accessibility > **Text scaling** can go to 125% if she wants bigger type.

## Updating the app

Edit `src/app.html` or `data/temples.json`, then:

```bash
python3 build.py
git add -A && git commit -m "Update" && git push
```

The site updates within a minute or two. Her phone picks up the new version the next
time she opens the app while online.

## Layout

- `src/app.html` — the page template (styles, markup, script)
- `data/temples.json` — the 111 shrines: names, deities, descriptions, photo paths, video IDs
- `img/` — one photo per shrine, from Wikimedia Commons contributors
- `build.py` — generates `index.html`, `sw.js` and `manifest.json`
- `dist/artifact.html` — self-contained preview build (not deployed)

## Swapping a video

Find the shrine in `data/temples.json` by its `n` number, put the YouTube video ID first in
its `videos` list, rebuild, commit and push.
