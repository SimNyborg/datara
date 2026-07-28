(() => {
    'use strict';

    const initAboutContactPath = () => {
        const main = document.querySelector('#main-content');
        const media = document.querySelector('.about-datara-media');
        const image = media ? media.querySelector('img') : null;
        const aboutText = document.querySelector('.about-datara-text');
        const contactLayout = document.querySelector('#kontakt .contact-layout');
        const connector = document.querySelector('.about-contact-path');

        if (!main || !media || !image || !aboutText || !contactLayout || !connector) {
            return;
        }

        const guide = connector.querySelector('.about-contact-path__guide');
        const reveal = connector.querySelector('.about-contact-path__reveal');
        const ribbon = connector.querySelector('.about-contact-path__ribbon');
        const revealMask = connector.querySelector('#aboutContactRevealMask');
        const ribbonGradient = connector.querySelector(
            '#aboutContactRibbonFade'
        );

        if (!guide || !reveal || !ribbon || !revealMask) {
            return;
        }

        let animationFrame = 0;
        let revealPrepared = false;

        const clamp = (value, minimum, maximum) =>
            Math.min(Math.max(value, minimum), maximum);
        const round = (value) => Number(value.toFixed(2));

        const buildTaperedRibbon = (
            startWidth,
            endWidth,
            seamPoint
        ) => {
            const totalLength = guide.getTotalLength();

            if (!Number.isFinite(totalLength) || totalLength <= 0) {
                return '';
            }

            const sampleCount = Math.round(
                clamp(totalLength / 2.5, 72, 220)
            );
            const seamHoldDistance = clamp(
                startWidth * 0.45,
                12,
                20
            );
            const leftSide = [];
            const rightSide = [];
            const samples = Array.from(
                { length: sampleCount + 1 },
                (_, index) => ({
                    distance: totalLength * (index / sampleCount)
                })
            );

            if (
                seamPoint &&
                seamPoint.distance > 0 &&
                seamPoint.distance < totalLength
            ) {
                samples.push(seamPoint);
                samples.sort(
                    (first, second) =>
                        first.distance - second.distance
                );
            }

            samples.forEach((sample) => {
                const distance = sample.distance;
                const point =
                    sample.x === undefined
                        ? guide.getPointAtLength(distance)
                        : sample;
                const taperProgress = clamp(
                    (distance - seamHoldDistance) /
                        Math.max(
                            1,
                            totalLength - seamHoldDistance
                        ),
                    0,
                    1
                );
                const width =
                    endWidth +
                    (startWidth - endWidth) *
                        Math.pow(1 - taperProgress, 1.55);
                const halfWidth = width / 2;

                leftSide.push({
                    x: point.x - halfWidth,
                    y: point.y
                });
                rightSide.push({
                    x: point.x + halfWidth,
                    y: point.y
                });
            });

            const polygonPoints = [
                ...leftSide,
                ...rightSide.reverse()
            ];

            return [
                ...polygonPoints.map(
                    (point, index) =>
                        `${index === 0 ? 'M' : 'L'} ` +
                        `${round(point.x)} ${round(point.y)}`
                ),
                'Z'
            ].join(' ');
        };

        const prepareReveal = () => {
            if (revealPrepared) {
                return;
            }

            revealPrepared = true;
            const reduceMotion =
                window.matchMedia &&
                window.matchMedia('(prefers-reduced-motion: reduce)').matches;
            const revealConnector = () =>
                connector.classList.add('animate-in');

            if (reduceMotion || !('IntersectionObserver' in window)) {
                revealConnector();
                return;
            }

            const revealObserver = new IntersectionObserver(
                (entries) => {
                    entries.forEach((entry) => {
                        if (!entry.isIntersecting) {
                            return;
                        }

                        revealConnector();
                        revealObserver.unobserve(entry.target);
                    });
                },
                {
                    rootMargin: '0px 0px -10% 0px',
                    threshold: 0.01
                }
            );

            revealObserver.observe(connector);
        };

        const drawConnector = () => {
            animationFrame = 0;

            const mainRect = main.getBoundingClientRect();
            const mediaRect = media.getBoundingClientRect();
            const textRect = aboutText.getBoundingClientRect();
            const layoutRect = contactLayout.getBoundingClientRect();
            const sourceWidth =
                image.naturalWidth || Number(image.getAttribute('width')) || 1920;
            const sourceHeight =
                image.naturalHeight || Number(image.getAttribute('height')) || 1280;
            const sourcePathX =
                Number(image.dataset.pathX) || sourceWidth * 0.55;
            const sourcePathWidth =
                Number(image.dataset.pathWidth) || sourceWidth * 0.055;
            const imageScale = Math.max(
                mediaRect.width / sourceWidth,
                mediaRect.height / sourceHeight
            );
            const renderedImageWidth = sourceWidth * imageScale;
            const imageOffsetX = (mediaRect.width - renderedImageWidth) / 2;
            const startX =
                mediaRect.left -
                mainRect.left +
                imageOffsetX +
                sourcePathX * imageScale;
            const startWidth = clamp(sourcePathWidth * imageScale, 16, 44);
            const narrowLayout = window.innerWidth <= 860;
            connector.classList.toggle('is-disabled', narrowLayout);

            if (narrowLayout) {
                connector.classList.remove('is-ready');
                return;
            }

            const connectorOverlap = 2;
            const imagePathSlope = 0.55;
            const pathStartX =
                startX - imagePathSlope * connectorOverlap;
            const seamJoinDistance = Math.hypot(
                startX - pathStartX,
                connectorOverlap
            );
            const layoutTopY =
                layoutRect.top - mediaRect.bottom + connectorOverlap;
            const layoutCenterX =
                layoutRect.left -
                mainRect.left +
                layoutRect.width / 2;
            const layoutRightX = layoutRect.right - mainRect.left;
            const targetX = clamp(
                layoutCenterX,
                startX + 110,
                layoutRightX - 84
            );
            const entryY = layoutTopY + 8;
            const endY =
                layoutTopY +
                clamp(layoutRect.height * 0.46, 116, 210);
            const pathData = [
                `M ${round(pathStartX)} 0`,
                `L ${round(startX)} ${connectorOverlap}`,
                `C ${round(startX + 13)} ${connectorOverlap + 24} ${round(targetX)} ${round(layoutTopY - 48)} ${round(targetX)} ${round(entryY)}`,
                `L ${round(targetX)} ${round(endY)}`
            ].join(' ');
            const svgHeight = Math.max(1, endY + 24);

            connector.style.top = `${
                round(
                    mediaRect.bottom -
                        mainRect.top -
                        connectorOverlap
                )
            }px`;
            connector.style.width = `${round(mainRect.width)}px`;
            connector.style.height = `${round(svgHeight)}px`;
            connector.style.setProperty(
                '--connector-start-width',
                `${round(startWidth)}px`
            );
            connector.setAttribute(
                'viewBox',
                `0 0 ${round(mainRect.width)} ${round(svgHeight)}`
            );
            connector.dataset.routeSide = 'right';
            guide.setAttribute('d', pathData);
            reveal.setAttribute('d', pathData);
            ribbon.setAttribute(
                'd',
                buildTaperedRibbon(startWidth, 0.4, {
                    distance: seamJoinDistance,
                    x: startX,
                    y: connectorOverlap
                })
            );
            revealMask.setAttribute('x', '-64');
            revealMask.setAttribute('y', '-64');
            revealMask.setAttribute(
                'width',
                String(round(mainRect.width + 128))
            );
            revealMask.setAttribute(
                'height',
                String(round(svgHeight + 128))
            );
            connector.style.setProperty(
                '--connector-reveal-width',
                `${round(startWidth + 16)}px`
            );
            connector.style.setProperty(
                '--connector-roll-duration',
                `${round(clamp(guide.getTotalLength() / 160, 2.8, 3.4))}s`
            );

            if (ribbonGradient) {
                ribbonGradient.setAttribute('y2', String(round(endY)));
            }

            connector.classList.add('is-ready');
            prepareReveal();
        };

        const scheduleConnectorDraw = () => {
            if (animationFrame) {
                window.cancelAnimationFrame(animationFrame);
            }

            animationFrame = window.requestAnimationFrame(drawConnector);
        };

        scheduleConnectorDraw();
        image.addEventListener('load', scheduleConnectorDraw, { once: true });

        if ('ResizeObserver' in window) {
            const connectorResizeObserver = new ResizeObserver(
                scheduleConnectorDraw
            );
            [main, media, aboutText, contactLayout].forEach((element) =>
                connectorResizeObserver.observe(element)
            );
        } else {
            window.addEventListener('resize', scheduleConnectorDraw);
        }

        if (document.fonts && document.fonts.ready) {
            document.fonts.ready.then(scheduleConnectorDraw);
        }
    };

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initAboutContactPath, {
            once: true
        });
    } else {
        initAboutContactPath();
    }
})();
