// Init Swipers after CSS is ready
function initSwipers() {
    // Rent Swiper
    if (document.querySelector('.rent-swiper')) {
        new Swiper('.rent-swiper', {
            slidesPerView: 1.5,
            spaceBetween: 24,
            loop: false,
            watchOverflow: true,
            allowTouchMove: false,
            navigation: {
                prevEl: '.rent-prev',
                nextEl: '.rent-next'
            },
            breakpoints: {
                0: { slidesPerView: 1 },
                768: { slidesPerView: 1.5 }
            }
        });
    }

    // Rent card inner galleries
    document.querySelectorAll('.rent-card-gallery').forEach(function(el) {
        new Swiper(el, {
            slidesPerView: 1,
            spaceBetween: 0,
            loop: false,
            pagination: {
                el: el.querySelector('.rent-card-pagination'),
                clickable: true
            }
        });
    });
}

// Wait for swiper CSS to load before initializing
var swiperLink = document.getElementById('swiperCss');
if (!swiperLink || swiperLink.media === 'all') {
    initSwipers();
} else {
    swiperLink.addEventListener('load', initSwipers);
}

// Yandex Map — lazy load when contacts section is near viewport
(function() {
    var mapEl = document.getElementById('contacts-map');
    if (!mapEl) return;
    var loaded = false;
    var observer = new IntersectionObserver(function(entries) {
        if (entries[0].isIntersecting && !loaded) {
            loaded = true;
            observer.disconnect();
            var apiKey = mapEl.getAttribute('data-api-key') || '';
            var script = document.createElement('script');
            var mapUrl = 'https://api-maps.yandex.ru/2.1/?lang=ru_RU';
            if (apiKey) mapUrl += '&apikey=' + apiKey;
            script.src = mapUrl;
            script.onload = function() {
                ymaps.ready(function() {
                    var map = new ymaps.Map('contacts-map', {
                        center: [56.7688, 60.6336],
                        zoom: 16,
                        controls: ['zoomControl', 'fullscreenControl']
                    });
                    map.geoObjects.add(new ymaps.Placemark([56.7688, 60.6336], {
                        balloonContent: '620000, г. Екатеринбург, ул. Новостроя 1Б'
                    }, {
                        preset: 'islands#redDotIcon'
                    }));
                    map.behaviors.disable('scrollZoom');
                });
            };
            document.body.appendChild(script);
        }
    }, { rootMargin: '300px' });
    observer.observe(mapEl);
})();
