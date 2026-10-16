#!/usr/bin/env python3
"""Build two outputs from src/app.html and data/temples.json:
  index.html      standalone installable web app (photos from img/, YouTube embedded)
  dist/artifact.html  single self-contained page for the claude.ai preview (photos inlined, links out to YouTube)
"""
import base64, json, os, pathlib, sys

ROOT = pathlib.Path(__file__).parent
SMALL_IMG = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / 'img'
src = (ROOT / 'src' / 'app.html').read_text()
temples = json.load(open(ROOT / 'data' / 'temples.json'))

def inject(cfg, data):
    return src.replace('/*__DATA__*/', 'window.CONFIG=' + json.dumps(cfg) + ';\nwindow.TEMPLES=' + json.dumps(data, ensure_ascii=False, separators=(',', ':')) + ';')

# standalone
head = ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
        '<meta name="theme-color" content="#b7322a">\n<link rel="manifest" href="manifest.json">\n'
        '<link rel="icon" href="icon.png">\n<link rel="apple-touch-icon" href="icon.png">\n')
body = inject({'name': 'Sujatha', 'nameTa': 'சுஜாதா', 'embed': True, 'thumbs': True, 'sw': True}, temples)
# move <title>, metas, links and style into head: simplest is to put everything in body, browsers handle it.
(ROOT / 'index.html').write_text(head + '</head>\n<body>\n' + body + '\n</body>\n</html>\n')

# artifact: inline small images
data2 = []
for t in temples:
    t = dict(t)
    p = SMALL_IMG / os.path.basename(t['img'])
    t['img'] = 'data:image/jpeg;base64,' + base64.b64encode(p.read_bytes()).decode()
    data2.append(t)
art = inject({'name': 'Sujatha', 'nameTa': 'சுஜாதா', 'embed': False, 'thumbs': False, 'sw': False}, data2)
(ROOT / 'dist').mkdir(exist_ok=True)
(ROOT / 'dist' / 'artifact.html').write_text(art)

# service worker: cache shell + photos on first visit
imgs = sorted(os.listdir(ROOT / 'img'))
import hashlib
ver = hashlib.md5((ROOT / 'index.html').read_bytes()).hexdigest()[:8]
(ROOT / 'sw.js').write_text("""const C='dd-%s';
const SHELL=['./','index.html','manifest.json','icon.png'].concat(%s.map(f=>'img/'+f));
self.addEventListener('install',e=>{e.waitUntil(caches.open(C).then(c=>c.addAll(SHELL)).then(()=>self.skipWaiting()))});
self.addEventListener('activate',e=>{e.waitUntil(caches.keys().then(k=>Promise.all(k.filter(x=>x!==C).map(x=>caches.delete(x)))).then(()=>self.clients.claim()))});
self.addEventListener('fetch',e=>{const u=new URL(e.request.url);if(u.origin!==location.origin)return;
const page=/\\/(index\\.html)?$/.test(u.pathname);
if(page){e.respondWith(fetch(e.request).then(res=>{const cp=res.clone();caches.open(C).then(c=>c.put(e.request,cp));return res;}).catch(()=>caches.match(e.request)));return;}
e.respondWith(caches.match(e.request).then(r=>r||fetch(e.request).then(res=>{const cp=res.clone();caches.open(C).then(c=>c.put(e.request,cp));return res;})))});
""" % (ver, json.dumps(imgs)))
(ROOT / 'manifest.json').write_text(json.dumps({
    'name': 'Divya Desam Yatra', 'short_name': 'Divya Desam', 'start_url': './index.html', 'display': 'standalone',
    'background_color': '#f6ecd8', 'theme_color': '#b7322a', 'icons': [{'src': 'icon.png', 'sizes': '512x512', 'type': 'image/png'}]}, indent=1))
print('index.html', os.path.getsize(ROOT / 'index.html') // 1024, 'KB; artifact', os.path.getsize(ROOT / 'dist' / 'artifact.html') // 1024 // 1024, 'MB')
