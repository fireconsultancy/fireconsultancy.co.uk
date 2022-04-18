console.log('Hello from sw.js');

importScripts('https://storage.googleapis.com/workbox-cdn/releases/3.2.0/workbox-sw.js');

if (workbox) {
  console.log("Yay! Workbox is loaded 🎉");

  workbox.precaching.precacheAndRoute([
    {"url": "/", "revision": "1"},
    {"url": "/about", "revision": "1"},
    {"url": "/aerial-surveys", "revision": "1"},
    {"url": "/expert-witness", "revision": "1"},
    {"url": "/external-wall", "revision": "1"},
    {"url": "/fire-engineering", "revision": "1"},
    {"url": "/fire-safety-assessments", "revision": "1"},
    {"url": "/case-studies", "revision": "1"},
    {"url": "/ask", "revision": "1"},
    {"url": "/contact", "revision": "1"},
  ]);

  workbox.routing.registerRoute(
    /\.(?:js|css)$/,
    workbox.strategies.staleWhileRevalidate({
      cacheName: 'static-resources',
    }),
  );

  workbox.routing.registerRoute(
    /\.(?:webp|png|gif|jpg|jpeg|svg)$/,
    workbox.strategies.cacheFirst({
      cacheName: 'images',
      plugins: [
        new workbox.expiration.Plugin({
          maxEntries: 60,
          maxAgeSeconds: 30 * 24 * 60 * 60, // 30 Days
        }),
      ],
    }),
  );

  workbox.routing.registerRoute(
    new RegExp('^https://fireconsultancy-wordpress-assets.s3.eu-west-2.amazonaws.com/large/.*'),
    workbox.strategies.cacheFirst({
      cacheName: 'cdn-cache',
      cacheableResponse: {
        statuses: [0, 200], // Make sure 0 is included in this list.
      }
    })
  );

  
} else {
  console.log("Boo! Workbox didn't load 😬");
}