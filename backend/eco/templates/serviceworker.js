{% load static %}
self.addEventListener('install', (event) => {
    event.waitUntil(
        caches.open('admin-v1').then((cache) => {
            return cache.addAll([
                '/',
            ]);
        })
    );
});

self.addEventListener('fetch', (event) => {
    if (event.request.url.includes('/')) {
        event.respondWith(
            caches.match(event.request).then((response) => {
                return response || fetch(event.request);
            })
        );
    }
});

const urlBase64ToUint8Array = (base64String) => {
    const padding = '='.repeat((4 - (base64String.length % 4)) % 4);
    const base64 = (base64String + padding)
        .replace(/\-/g, '+')
        .replace(/_/g, '/');

    const rawData = atob(base64);
    const outputArray = new Uint8Array(rawData.length);

    for (let i = 0; i < rawData.length; ++i) {
        outputArray[i] = rawData.charCodeAt(i);
    }

    return outputArray;
};

const saveSubscription = async (subscription) => {
    const response = await fetch("{% url 'subscribe_info' %}", {
        method: 'post',
        headers: {'Content-type': "application/json"},
        body: JSON.stringify(subscription)
    });

    return response.json();
};

self.addEventListener("activate", async (e) => {
    const subscription = await self.registration.pushManager.subscribe({
            userVisibleOnly: true,
            applicationServerKey: urlBase64ToUint8Array('{{ vapid_public_key | safe }}')
        })
    ;

    const response = await saveSubscription(subscription);
    console.log(response);
});

self.addEventListener('push', (event) => {
    const data = event.data.json();
    const options = {
        body: data.message,
        data: {url: data.url},
    };

    event.waitUntil(
        self.registration.showNotification('Новое уведомление', options)
    );
});

self.addEventListener('notificationclick', (event) => {
    event.notification.close();
    const urlToOpen = new URL(event.notification.data.url || '/', self.location.origin);
    event.waitUntil(
        clients.matchAll({
            type: 'window',
            includeUncontrolled: true
        }).then((clientList) => {
            for (let client of clientList) {
                if (client.url === urlToOpen.href && 'focus' in client) {
                    return client.focus();
                }
            }
            if (clients.openWindow) {
                return clients.openWindow(urlToOpen.href);
            }
        })
    );
});

