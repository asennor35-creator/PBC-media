import re, json, sys, urllib.parse
SP = sys.argv[1]
css = open(SP + '/rubber_zip/pkg/halaman-EN.html').read()
css = css[css.find('<style'):css.find('</style>') + 8]
css = css.replace('</style>', """.pbk .ask{margin-top:22px;border:2px dashed var(--gold);background:#FFFBEF;padding:18px}
.pbk .ask b{display:block;font:700 18px 'Oswald';text-transform:uppercase;color:var(--navy);margin-bottom:4px}
.pbk .ask p{margin:0 0 10px;font-size:15px}
.pbk .mg a{font:700 14px 'Barlow';color:var(--gold2);text-decoration:none;display:inline-block;margin-top:8px}
.pbk .mg i{display:block;font-style:normal;font-size:13px;color:var(--muted);margin:2px 0 6px}
</style>""")
U = 'https://pratamabuild.id/wp-content/uploads/2026/11/pbc-akustik-m-'
WA = 'https://wa.me/6285745026574?text='

M = [  # key, img, en name, id name, en desc, id desc, size, depth, nrc, core_en, core_id, face_en, face_id, mount_en, mount_id, best_en, best_id
 ('fabric','kain','Fabric Panel','Panel Kain Kotak',
  'The workhorse of acoustic treatment. A deep 12 cm panel that absorbs speech and music evenly, placed at the first-reflection points.',
  'Panel andalan peredam gema. Tebal 12 cm, menyerap suara bicara dan musik secara merata, dipasang tepat di titik pantulan pertama.',
  '60 × 120 cm','12 cm','1.00','100 mm rockwool board, 60 kg/m³','Rockwool papan 10 cm, 60 kg/m³','Breathable acoustic fabric','Kain akustik tembus udara',
  'Centre at ear height, hidden Z-clips','Tengah panel setinggi telinga, Z-clip tersembunyi',
  'Music studio, band room, home cinema, recording room','Studio musik, ruang band, home theater, studio rekaman'),
 ('wide','wide','Wide Fabric Panel','Panel Kain Lebar',
  'A slim landscape panel that calms echo in everyday rooms without looking technical.',
  'Panel memanjang yang ramping, meredam gema di ruangan sehari-hari tanpa terlihat seperti studio.',
  '120 × 60 cm','7 cm','0.90','50 mm rockwool / glasswool, 60–80 kg/m³','Rockwool / glasswool 5 cm, 60–80 kg/m³','Acoustic fabric or PET felt','Kain akustik atau felt PET',
  'Centre at ear height, hidden Z-clips','Tengah panel setinggi telinga, Z-clip tersembunyi',
  'Meeting room, café, bedroom, villa','Ruang rapat, kafe, kamar tidur, villa'),
 ('hexagon','hex','Honeycomb Hexagons','Panel Heksagon',
  'Seven hexagons in two or three tones — a camera-friendly backdrop that also tames echo.',
  'Tujuh heksagon dua–tiga warna — latar yang cantik di kamera sekaligus meredam gema.',
  'Set 90 × 80 cm','5 cm','0.90','50 mm rockwool / glasswool, 60–80 kg/m³','Rockwool / glasswool 5 cm, 60–80 kg/m³','Acoustic fabric or PET felt','Kain akustik atau felt PET',
  'Centre at ear height, hidden Z-clips','Tengah panel setinggi telinga, Z-clip tersembunyi',
  'Podcast, content room, bedroom, café','Podcast, ruang konten, kamar tidur, kafe'),
 ('round','round','Round Panels','Panel Bulat',
  'Overlapping circles in soft tones for a relaxed, modern wall.',
  'Lingkaran bertumpuk dengan warna lembut untuk dinding yang santai dan modern.',
  'Ø 90 cm + smaller circle','5 cm','0.90','50 mm rockwool / glasswool, 60–80 kg/m³','Rockwool / glasswool 5 cm, 60–80 kg/m³','Acoustic fabric or PET felt','Kain akustik atau felt PET',
  'Centre at ear height, hidden Z-clips','Tengah panel setinggi telinga, Z-clip tersembunyi',
  'Café, meeting room, content room','Kafe, ruang rapat, ruang konten'),
 ('slat','slat','Timber Slat Panel','Panel Kisi Kayu (Slat)',
  'Warm timber slats over black felt and rockwool. Absorbs sound while the room stays lively and natural.',
  'Bilah kayu di atas felt hitam dan rockwool. Menyerap suara, tapi ruangan tetap hidup dan natural.',
  '60 cm × floor to ceiling','12 cm','0.75','Black felt + 50 mm rockwool + 50 mm air gap','Felt hitam + rockwool 5 cm + rongga 5 cm','Timber or veneered MDF slats','Bilah kayu atau MDF veneer',
  'Screwed to battens, floor to ceiling','Disekrup ke reng, dari lantai sampai plafon',
  'Villa, bedroom, meeting room, home cinema, recording room','Villa, kamar tidur, ruang rapat, home theater, studio rekaman'),
 ('printed','printed','Printed Art Panel','Panel Bergambar',
  'Any artwork, logo or photo printed on acoustic fabric. Looks like a canvas, works like an acoustic panel.',
  'Gambar, logo, atau foto apa saja dicetak di kain akustik. Tampil seperti lukisan, bekerja seperti panel peredam.',
  '120 × 80 cm','5 cm','0.90','50 mm rockwool / glasswool, 60–80 kg/m³','Rockwool / glasswool 5 cm, 60–80 kg/m³','Printed acoustic fabric','Kain akustik bercetak',
  'Centre at ear height, hidden Z-clips','Tengah panel setinggi telinga, Z-clip tersembunyi',
  'Café, restaurant, meeting room, bedroom','Kafe, restoran, ruang rapat, kamar tidur'),
]

T = {
 'en': dict(
  waq=lambda x: WA + urllib.parse.quote("Hello PBC, I'd like advice on acoustic wall panels" + (f" ({x})" if x else '') + '.'),
  eb='Acoustic wall panels · Bali & all of Indonesia', h1='Acoustic wall panels that look like décor',
  lead='Six of our most-requested models. Every panel is made to your size and colour, filled with rockwool and installed by PBC — so the room sounds calm, not only looks good.',
  btn='Ask on WhatsApp', q='12 colour palettes or your own colour · Custom sizes · Hidden Z-clip mounting',
  s1eb='Step 1 · Your room', s1h='Which panel suits your room?',
  rooms=[('Café & restaurant','Round · Printed art · Wide fabric','Guests talk without shouting, and the wall still looks like décor.','/cafe-acoustic-panels-bali/','See café acoustics →'),
         ('Villa & bedroom','Wide fabric · Timber slat · Printed art','A softer, quieter room that keeps the villa style.','/villa-acoustic-panels-bali/','See villa acoustics →'),
         ('Podcast & content','Hexagons · Fabric panel','Clear voice on the mic and a backdrop that looks good on camera.','/podcast-room-acoustic-panels-bali/','See podcast rooms →'),
         ('Studio & home cinema','Fabric panel 12 cm · Timber slat','Accurate sound at the listening seat, with bass traps in the corners.','/music-studio-bali/','See music studios →')],
  s2eb='Step 2 · Choose a model', s2h='Six models, made to measure',
  nrc='NRC shows how much sound a panel absorbs: 0 = none, 1.00 = almost all.',
  size='Size', depth='Depth', abs='Absorption', full='Full specification', core='Core', face='Face', mount='Mounting', col='Colours', colv='12 colour palettes or your own colour',
  best='Best for', askm='Ask about this model →', typ='Sizes shown are standard. Every panel can be made to your size.',
  askb='Looking for another shape?', askp='We also make curved, fluted, perforated-timber, 3D and ceiling panels. Ask us for the full catalogue.', askbtn='Ask for the full catalogue',
  askq='full catalogue',
  s3eb='How we work', s3h='From echo to calm in 6 steps',
  steps=['Free site survey — we measure the room and its echo time','We calculate how many panels are needed and where they go','You choose the model, size and colours','Panels are made to measure: frame, rockwool, acoustic fabric','Installation with hidden Z-clips or battens','We measure the echo again, so you can hear and see the difference'],
  ctah='Send us a photo of your room', ctap='Tell us the size and what the room is for — we recommend the model, quantity and layout. Free survey in Bali.'),
 'id': dict(
  waq=lambda x: WA + urllib.parse.quote('Halo PBC, saya ingin konsultasi wall panel akustik' + (f' ({x})' if x else '') + '.'),
  eb='Wall panel akustik · Bali & seluruh Indonesia', h1='Wall panel akustik yang tampil seperti dekorasi',
  lead='Enam model yang paling sering dipesan. Setiap panel dibuat sesuai ukuran dan warna pilihan Anda, berisi rockwool, dan dipasang oleh PBC — ruangan bukan hanya cantik, tapi juga terdengar tenang.',
  btn='Tanya via WhatsApp', q='12 palet warna atau warna pilihan sendiri · Ukuran custom · Pemasangan Z-clip tersembunyi',
  s1eb='Langkah 1 · Ruangan Anda', s1h='Panel mana yang cocok untuk ruangan Anda?',
  rooms=[('Kafe & restoran','Bulat · Bergambar · Kain lebar','Tamu bisa mengobrol tanpa berteriak, dan dinding tetap tampil sebagai dekorasi.','/peredam-suara-kafe-bali/','Lihat akustik kafe →'),
         ('Villa & kamar tidur','Kain lebar · Kisi kayu · Bergambar','Ruangan lebih lembut dan tenang tanpa mengubah gaya villa.','/panel-akustik-villa-bali/','Lihat akustik villa →'),
         ('Podcast & konten','Heksagon · Panel kain kotak','Suara jernih di mikrofon dan latar yang cantik di kamera.','/panel-akustik-podcast-bali/','Lihat ruang podcast →'),
         ('Studio & home theater','Panel kain 12 cm · Kisi kayu','Suara akurat di posisi dengar, dengan bass trap di sudut ruangan.','/studio-musik-bali/','Lihat studio musik →')],
  s2eb='Langkah 2 · Pilih model', s2h='Enam model, dibuat sesuai ukuran',
  nrc='NRC menunjukkan seberapa banyak suara yang diserap panel: 0 = tidak menyerap, 1,00 = hampir semua terserap.',
  size='Ukuran', depth='Tebal', abs='Daya serap', full='Spesifikasi lengkap', core='Isi', face='Muka', mount='Pemasangan', col='Warna', colv='12 palet warna atau warna pilihan sendiri',
  best='Cocok untuk', askm='Tanya model ini →', typ='Ukuran di atas adalah ukuran standar. Setiap panel bisa dibuat sesuai ukuran ruangan Anda.',
  askb='Mencari bentuk lain?', askp='Kami juga membuat panel lengkung, fluted, kayu berlubang, 3D, dan panel plafon. Minta katalog lengkapnya ke kami.', askbtn='Minta katalog lengkap',
  askq='katalog lengkap',
  s3eb='Cara kerja kami', s3h='Dari bergema jadi tenang dalam 6 langkah',
  steps=['Survei lokasi gratis — kami ukur ruangan dan waktu gemanya','Kami hitung jumlah panel yang dibutuhkan dan posisinya','Anda pilih model, ukuran, dan warna','Panel dibuat sesuai ukuran: rangka, rockwool, kain akustik','Pemasangan dengan Z-clip tersembunyi atau reng','Kami ukur gema lagi, supaya Anda bisa mendengar dan melihat bedanya'],
  ctah='Kirim foto ruangan Anda', ctap='Beri tahu ukuran dan fungsi ruangannya — kami sarankan model, jumlah, dan tata letaknya. Survei gratis di Bali.'),
}

IDS={'Ø 90 cm + smaller circle':'Ø 90 cm + lingkaran kecil','60 cm × floor to ceiling':'60 cm × lantai sampai plafon'}
def page(lang):
    t = T[lang]; L = 0 if lang == 'en' else 1
    h = [css, '<div class="pbk">']
    h.append(f'<section class="pbk-hero"><div class="in"><div class="eb">{t["eb"]}</div><h1>{t["h1"]}</h1><p>{t["lead"]}</p><a class="btn" href="{t["waq"]("")}">{t["btn"]}</a><p class="q">{t["q"]}</p></div></section>')
    h.append(f'<section><div class="in"><div class="eb">{t["s1eb"]}</div><h2>{t["s1h"]}</h2><div class="mg">')
    for r in t['rooms']:
        h.append(f'<div><b>{r[0]}</b><i>{r[1]}</i><p>{r[2]}</p><a href="{r[3]}">{r[4]}</a></div>')
    h.append('</div></div></section>')
    h.append(f'<section class="alt"><div class="in"><div class="eb">{t["s2eb"]}</div><h2>{t["s2h"]}</h2><p class="note" style="margin:-6px 0 18px">{t["nrc"]}</p><div class="pfg">')
    for m in M:
        name = m[2 + L]; nrc = m[8] if lang == 'en' else m[8].replace('.', ',')
        alt = (f'{m[2]} – acoustic wall panel by PBC Bali' if lang == 'en' else f'{m[3]} – wall panel akustik PBC Bali')
        h.append(f'<div class="pfc"><img src="{U}{m[1]}.jpg" alt="{alt}" width="1531" height="895" loading="lazy" decoding="async"><h3>{name}</h3><p>{m[4 + L]}</p>'
                 f'<table><tr><td>{t["size"]}</td><td>{m[6] if lang=="en" else IDS.get(m[6],m[6])}</td></tr><tr><td>{t["depth"]}</td><td>{m[7]}</td></tr><tr><td>{t["abs"]}</td><td>NRC {nrc}</td></tr></table>'
                 f'<details><summary>{t["full"]}</summary><dl><dt>{t["core"]}</dt><dd>{m[9 + L]}</dd><dt>{t["face"]}</dt><dd>{m[11 + L]}</dd><dt>{t["mount"]}</dt><dd>{m[13 + L]}</dd>'
                 f'<dt>{t["col"]}</dt><dd>{t["colv"]}</dd><dt>{t["best"]}</dt><dd>{m[15 + L]}</dd></dl></details>'
                 f'<a class="pfl" href="{t["waq"](name)}">{t["askm"]}</a></div>')
    h.append(f'</div><p class="note" style="margin-top:14px">{t["typ"]}</p>')
    h.append(f'<div class="ask"><b>{t["askb"]}</b><p>{t["askp"]}</p><a class="btn" href="{t["waq"](t["askq"])}">{t["askbtn"]}</a></div></div></section>')
    h.append(f'<section><div class="in"><div class="eb">{t["s3eb"]}</div><h2>{t["s3h"]}</h2><div class="steps">' + ''.join(f'<div>{s}</div>' for s in t['steps']) + '</div></div></section>')
    h.append(f'<section class="cta"><div class="in"><h2>{t["ctah"]}</h2><p>{t["ctap"]}</p><a class="btn" href="{t["waq"]("")}">{t["btn"]}</a></div></section></div>')
    return ''.join(h)

for lang in ('en', 'id'):
    open(f'{SP}/wp6/wallpanel-{lang}.html', 'w').write(page(lang))
    print(lang, len(page(lang)))
