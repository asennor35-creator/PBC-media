import json, urllib.parse
SP = '/tmp/claude-0/-home-claude/d4f19151-37e9-53d0-8f8d-43cbfabd1301/scratchpad/np/'
B = '/home/claude/pbc-media/backup/2026-11-22/np/'
M = json.load(open(SP + 'media.json'))
WA = 'https://wa.me/6285745026574?text='

T = {
 'en': dict(eb='Design &amp; Construction Drawings', h='Café Nusa Penida',
   tag='Architectural design &amp; construction drawings',
   lead='A 105 m² café with 42 seats on a 10 × 20 m plot. Full design package: 3D renders, a 47-sheet construction drawing set, structural calculations and an itemised BOQ.',
   r='3D renders', d='Construction drawings',
   rc=['Front view – day', 'Front view – evening', 'Seating area', 'Indoor bar facing the road', 'Coffee &amp; pastry counter', 'Toilet lobby'],
   dc=['Furniture layout plan', 'Front elevation', 'Structural section with roof truss'],
   cta='Need a design before you build? We prepare 3D renders, construction drawings and a detailed BOQ.',
   btn='Ask about a design package', waq="Hello PBC, I'd like to ask about a design package (3D render, construction drawings and BOQ).",
   zoom='Tap an image to enlarge.', close='Close',
   side_eb='Design package', side_h='From idea to drawings, before we build',
   side_p='For a new café in Nusa Penida we prepared the full package: 3D renders, construction drawings, structural calculations and an itemised BOQ — so the owner knows exactly what will be built and what it costs.',
   side_a='See the design &amp; drawings →', side_url='/our-work/#desain'),
 'id': dict(eb='Desain &amp; Gambar Kerja', h='Kafe Nusa Penida',
   tag='Desain arsitektur &amp; gambar kerja',
   lead='Kafe 105 m² dengan 42 kursi di lahan 10 × 20 m. Paket desain lengkap: render 3D, 47 lembar gambar kerja, perhitungan struktur, dan RAB terperinci.',
   r='Render 3D', d='Gambar kerja',
   rc=['Tampak depan – siang', 'Tampak depan – malam', 'Area duduk', 'Meja bar menghadap jalan', 'Counter kopi &amp; pastry', 'Lobi toilet'],
   dc=['Denah tata letak furnitur', 'Tampak depan', 'Potongan struktur dengan rangka atap'],
   cta='Butuh desain sebelum membangun? Kami siapkan render 3D, gambar kerja, dan RAB terperinci.',
   btn='Tanya paket desain', waq='Halo PBC, saya ingin bertanya tentang paket desain (render 3D, gambar kerja, dan RAB).',
   zoom='Ketuk gambar untuk memperbesar.', close='Tutup',
   side_eb='Paket desain', side_h='Dari ide sampai gambar kerja, sebelum membangun',
   side_p='Untuk kafe baru di Nusa Penida kami siapkan paket lengkap: render 3D, gambar kerja, perhitungan struktur, dan RAB terperinci — pemilik tahu persis apa yang dibangun dan berapa biayanya.',
   side_a='Lihat desain &amp; gambar kerja →', side_url='/hasil-kerja-kami/#desain'),
}
R = ['render-08', 'render-09', 'render-11', 'render-12', 'render-13', 'render-14']
D = ['drawing-05', 'drawing-08', 'drawing-28']

CSS = """<style>
.pbc .dsg-tag{font:600 15px 'Barlow',sans-serif;color:var(--muted);margin:-6px 0 10px}
.pbc .dsg-lead{max-width:760px;margin:0 0 22px}
.pbc .dsg-r{display:grid;grid-template-columns:1fr;gap:10px;margin-bottom:26px}
@media(min-width:560px){.pbc .dsg-r{grid-template-columns:1fr 1fr}}
@media(min-width:900px){.pbc .dsg-r{grid-template-columns:repeat(3,1fr);gap:14px}}
.pbc .dsg-r img{aspect-ratio:16/10;object-fit:cover;cursor:zoom-in}
.pbc .dsg-d{display:grid;grid-template-columns:1fr;gap:10px;margin-bottom:22px}
@media(min-width:760px){.pbc .dsg-d{grid-template-columns:repeat(3,1fr);gap:14px}}
.pbc .dsg-d figure{border:1px solid #DDE1EA}
.pbc .dsg-d img{aspect-ratio:4/3;object-fit:contain;background:#fff;padding:8px;cursor:zoom-in}
.pbc .dsg-note{font-size:13px;color:var(--muted);margin:-12px 0 20px}
.pbc .dsg-cta{background:var(--navy);color:#fff;padding:20px;border-top:3px solid var(--gold)}
.pbc .dsg-cta p{margin:0 0 12px;color:#fff}
.pbc .dsg-cta a{display:inline-block;background:var(--gold);color:var(--navy);font:700 15px 'Barlow',sans-serif;padding:12px 18px;text-decoration:none;border-radius:2px}
</style>"""

def fig(k, cap, alt_sfx):
    m = M[k]
    return f'<figure><img src="{m["url"]}" alt="{cap} – {alt_sfx}" width="{m["w"]}" height="{m["h"]}" loading="lazy" decoding="async"><figcaption>{cap}</figcaption></figure>'

def section(lang):
    t = T[lang]; sfx = 'Café Nusa Penida, PBC Bali' if lang == 'en' else 'Kafe Nusa Penida, PBC Bali'
    h = [CSS, '<section class="pbc-sec" id="desain"><div class="in">',
         f'<div class="eyebrow">{t["eb"]}</div><h2>{t["h"]}</h2><p class="dsg-tag">{t["tag"]}</p><p class="dsg-lead">{t["lead"]}</p>',
         f'<h3 class="sub">{t["r"]}</h3><div class="dsg-r">' + ''.join(fig(k, c, sfx) for k, c in zip(R, t['rc'])) + '</div>',
         f'<h3 class="sub">{t["d"]}</h3><div class="dsg-d">' + ''.join(fig(k, c, sfx) for k, c in zip(D, t['dc'])) + '</div>',
         f'<p class="dsg-note">{t["zoom"]}</p>',
         f'<div class="dsg-cta"><p>{t["cta"]}</p><a href="{WA + urllib.parse.quote(t["waq"])}">{t["btn"]}</a></div>',
         '</div></section>']
    return ''.join(h)

def side(lang):
    t = T[lang]; m = M['render-08']
    return (f'<section class="pbc-sec"><div class="in narrow"><div class="eyebrow">{t["side_eb"]}</div><h2>{t["side_h"]}</h2>'
            f'<a href="{t["side_url"]}"><img src="{m["url"]}" alt="{t["rc"][0]} – {t["h"]}" width="{m["w"]}" height="{m["h"]}" loading="lazy" decoding="async" style="width:100%;height:auto;aspect-ratio:16/10;object-fit:cover;display:block;margin:6px 0 14px"></a>'
            f'<p>{t["side_p"]}</p><p><a href="{t["side_url"]}">{t["side_a"]}</a></p></div></section>')

out = {}
for p, lang in [(739, 'en'), (741, 'id')]:
    r = json.load(open(B + f'page{p}.json'))['content']['raw']
    a = '<section class="pbc-sec pbc-cs" id="studi-kasus">'
    assert r.count(a) == 1 and 'id="desain"' not in r
    out[p] = r.replace(a, section(lang) + a)
for p, lang, anchor in [(474, 'en', '<section class="pbc-sec" id="faq">'), (473, 'id', '<section class="pbc-sec" id="faq">'),
                        (654, 'en', None), (653, 'id', None)]:
    r = json.load(open(B + f'page{p}.json'))['content']['raw']
    if anchor is None:
        # sebelum bagian "pertanyaan umum"
        i = r.find('Common questions' if lang == 'en' else 'Pertanyaan umum'); anchor = r[r.rfind('<section', 0, i):r.find('>', r.rfind('<section', 0, i)) + 1]
    assert r.count(anchor) == 1, (p, anchor)
    out[p] = r.replace(anchor, side(lang) + anchor)
for p, c in out.items():
    json.dump({'content': c}, open(SP + f'_p{p}.json', 'w'), ensure_ascii=False)
    print(p, len(c))
