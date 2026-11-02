// PBC Marketing OS - service worker: kerangka aplikasi tersedia walau sinyal lemah. Data tidak disimpan di sini.
const CACHE = "pbc-app-v2";
const KERANGKA = ["./", "./index.html", "./manifest.webmanifest", "./ikon-192.png", "./ikon-512.png"];
self.addEventListener("install", e => { e.waitUntil(caches.open(CACHE).then(c => c.addAll(KERANGKA))); self.skipWaiting(); });
self.addEventListener("activate", e => {
  e.waitUntil(caches.keys().then(k => Promise.all(k.filter(x => x !== CACHE).map(x => caches.delete(x)))));
  self.clients.claim();
});
self.addEventListener("fetch", e => {
  const u = new URL(e.request.url);
  if (e.request.method !== "GET" || u.origin !== location.origin || u.pathname.endsWith("/data.json")) return;
  e.respondWith(fetch(e.request).then(r => {
    if (r.ok) { const s = r.clone(); caches.open(CACHE).then(c => c.put(e.request, s)); }
    return r;
  }).catch(() => caches.match(e.request).then(r => r || caches.match("./index.html"))));
});
