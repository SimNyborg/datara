/* De vandrette skillestreger paa forsiden tegnes fra venstre kantstreg mod hoejre,
 * naar man scroller hen til dem.
 *
 * CSS viser altid den faerdige side. En streg 'spaendes' (.ln-armed) foerst, lige foer den kommer
 * ind nedefra, og tegnes, naar den er kommet 12 % op paa skaermen. En streg, der allerede staar paa
 * skaermen eller over den, fx efter et menulink til en sektion eller en genindlaesning midt paa
 * siden, forbliver faerdig. Hver streg tegnes hoejst een gang pr. sidevisning.
 * Uden JavaScript, uden IntersectionObserver og ved reduceret bevaegelse sker der intet.
 */
(function () {
    'use strict';

    if (!('IntersectionObserver' in window)) return;
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;

    var lines = document.querySelectorAll('main section + section');
    if (!lines.length) return;
    document.documentElement.classList.add('ln');

    /* Lange streger tager laengere tid, men ikke proportionalt: 384 px ~ 590 ms, 1300 px ~ 920 ms. */
    var duration = function (px) {
        return Math.round(Math.min(950, Math.max(340, 200 + 20 * Math.sqrt(px))));
    };

    var arming, drawing;
    var done = function (el) {
        el.classList.remove('ln-armed');
        arming.unobserve(el);
        drawing.unobserve(el);
    };

    /* 1. Spaend en streg, lige foer den kommer ind nedefra. Staar den allerede paa skaermen
          eller over den, forbliver den faerdig. */
    arming = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
            var el = entry.target;
            if (entry.boundingClientRect.top > window.innerHeight) {
                if (entry.isIntersecting && !el.classList.contains('ln-armed')) {
                    el.classList.add('ln-armed');
                    drawing.observe(el);
                }
                return;
            }
            if (!el.classList.contains('ln-go')) done(el);
        });
    }, { rootMargin: '0px 0px 40% 0px' });

    /* 2. Tegn den, naar den er kommet 12 % op paa skaermen. Er man scrollet forbi i eet hop,
          staar den faerdig. */
    drawing = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
            var el = entry.target;
            if (entry.isIntersecting) {
                el.style.setProperty('--ln-d', duration(entry.boundingClientRect.width) + 'ms');
                el.classList.add('ln-go');
                arming.unobserve(el);
                drawing.unobserve(el);
            } else if (entry.boundingClientRect.bottom < 0) {
                done(el);
            }
        });
    }, { rootMargin: '0px 0px -12% 0px' });

    /* Start efter load, naar browseren har genskabt scrollpositionen ved en genindlaesning. */
    var start = function () {
        window.requestAnimationFrame(function () {
            window.requestAnimationFrame(function () {
                Array.prototype.forEach.call(lines, function (el) { arming.observe(el); });
            });
        });
    };
    if (document.readyState === 'complete') start();
    else window.addEventListener('load', start, { once: true });
})();
