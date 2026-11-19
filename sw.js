/* GM Early Years App iPhone guide: keeps a copy of the guide on the phone so it opens without a signal.
   The guide itself is fetched fresh whenever there is a connection; the saved copy is used only when there is not.
   Change CACHE with every release so old copies are cleared. */
var CACHE = 'ey-guide-v3.00';
var FILES = ['./', './manifest.webmanifest', './icons/icon-180.png', './icons/icon-192.png', './icons/icon-512.png', './icons/icon-maskable-512.png'];

self.addEventListener('install', function (e) {
  e.waitUntil(caches.open(CACHE).then(function (c) { return c.addAll(FILES); }).then(function () { return self.skipWaiting(); }));
});

self.addEventListener('activate', function (e) {
  e.waitUntil(caches.keys().then(function (keys) {
    return Promise.all(keys.filter(function (k) { return k.indexOf('ey-guide-') === 0 && k !== CACHE; }).map(function (k) { return caches.delete(k); }));
  }).then(function () { return self.clients.claim(); }));
});

self.addEventListener('fetch', function (e) {
  var r = e.request;
  if (r.method !== 'GET') return;
  var u = new URL(r.url), scope = new URL(self.registration.scope);
  if (u.origin !== scope.origin) return;                       /* maps and other sites: straight to the network */
  var isGuide = u.pathname === scope.pathname || u.pathname === scope.pathname + 'index.html';
  if (r.mode === 'navigate' || isGuide) {
    if (!isGuide) return;                                      /* other pages, such as /preview/: not kept */
    e.respondWith(fetch(r).then(function (res) {
      if (res && res.ok) { var copy = res.clone(); caches.open(CACHE).then(function (c) { c.put('./', copy); }); }
      return res;
    }).catch(function () { return caches.match('./'); }));
    return;
  }
  e.respondWith(caches.match(r).then(function (hit) { return hit || fetch(r); }));
});
