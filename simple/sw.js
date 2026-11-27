/* GM Early Years App Simple guide: keeps a copy on the phone so it opens without a signal.
   The guide is fetched fresh whenever there is a connection; the saved copy is used only when there is not.
   Change CACHE with every release so old copies are cleared. Only touches caches named ey-simple-. */
var CACHE = 'ey-simple-v1.5';
var FILES = ['./', './manifest.webmanifest'];

self.addEventListener('install', function (e) {
  e.waitUntil(caches.open(CACHE).then(function (c) { return c.addAll(FILES); }).then(function () { return self.skipWaiting(); }));
});

self.addEventListener('activate', function (e) {
  e.waitUntil(caches.keys().then(function (keys) {
    return Promise.all(keys.filter(function (k) { return k.indexOf('ey-simple-') === 0 && k !== CACHE; }).map(function (k) { return caches.delete(k); }));
  }).then(function () { return self.clients.claim(); }));
});

self.addEventListener('fetch', function (e) {
  var r = e.request;
  if (r.method !== 'GET') return;
  var u = new URL(r.url), scope = new URL(self.registration.scope);
  if (u.origin !== scope.origin) return;                       /* NHS login, maps and other sites: straight to the network */
  var isGuide = u.pathname === scope.pathname || u.pathname === scope.pathname + 'index.html';
  if (r.mode === 'navigate' || isGuide) {
    if (!isGuide) return;                                      /* other pages, such as /simple/preview/: not kept */
    e.respondWith(fetch(u.href, { cache: 'no-cache', credentials: 'same-origin' }).then(function (res) {
      if (res && res.ok) { var copy = res.clone(); caches.open(CACHE).then(function (c) { c.put('./', copy); }); }
      return res;
    }).catch(function () { return caches.match('./'); }));
    return;
  }
  if (u.pathname.indexOf(scope.pathname) !== 0) return;         /* icons and files outside this folder: network */
  e.respondWith(caches.match(r).then(function (hit) { return hit || fetch(r); }));
});
