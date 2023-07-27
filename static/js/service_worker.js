let g_permanent = [
	'/static/css/bootstrap530a1.min.css',
	'/static/js/popper.min.js',
	'/static/js/bootstrap530a1.min.js',
	'/static/fontawesome/css/fontawesome.min.css',
	'/static/fontawesome/css/solid.min.css',
	'/static/fontawesome/css/regular.min.css',
	'/static/fontawesome/css/brands.min.css',
	'/static/fontawesome/webfonts/fa-solid-900.woff2'
];

let g_temp = [
	'/static/css/common.css',
	'/static/css/friends.css',
	'/static/css/index.css',
	'/static/js/common.js',
	'/',
	'/friends/',
	'/settings/',
]

self.addEventListener('install', function (e) {
	/*
	e.waitUntil(
		caches.open('friends42').then(function (cache) {
			return cache.addAll([...g_temp, ...g_permanent]);
		})
	);
	 */
});

self.addEventListener('fetch', function (event) {
	/*
	event.respondWith(
		caches.match(event.request).then(async function (response) {
			if (event.request.url in g_temp)
			{
				let r = await fetch(event.request);
				if (r.status === 200)
					return r;
				return response;
			}
			return response || fetch(event.request);
		})
	);
	 */
});

self.addEventListener("activate", (event) => {
	event.waitUntil(
		caches.keys().then((cacheNames) => {
			return Promise.all(
				cacheNames.map((cacheName) => {
					return caches.delete(cacheName);
				})
			);
		})
	);
});
