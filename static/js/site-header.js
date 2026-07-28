(() => {
  const navbar = document.querySelector('.site-navbar');
  const burger = navbar?.querySelector('#navbar-burger');
  const mobileMenu = navbar?.querySelector('#navbar-mobile-menu');
  const shouldAutoHide = navbar?.classList.contains('site-navbar--inner');
  const reducedMotionMedia = window.matchMedia('(prefers-reduced-motion: reduce)');
  const mobileViewportMedia = window.matchMedia('(max-width: 800px)');

  if (!navbar || !burger || !mobileMenu) {
    return;
  }

  const showNavbar = () => {
    navbar.classList.remove('navbar-hidden');
  };

  const syncMenuState = () => {
    const isOpen = mobileMenu.classList.contains('open');
    burger.classList.toggle('open', isOpen);
    burger.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
    burger.setAttribute(
      'aria-label',
      isOpen ? burger.dataset.labelClose : burger.dataset.labelOpen
    );
    navbar.classList.toggle('navbar-menu-open', isOpen);

    if (isOpen) {
      showNavbar();
    }
  };

  const closeMenu = (returnFocus = false) => {
    mobileMenu.classList.remove('open');
    syncMenuState();

    if (returnFocus) {
      burger.focus();
    }
  };

  burger.addEventListener('click', () => {
    mobileMenu.classList.toggle('open');
    syncMenuState();
  });

  mobileMenu.querySelectorAll('a').forEach((link) => {
    link.addEventListener('click', () => closeMenu());
  });

  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape' && mobileMenu.classList.contains('open')) {
      closeMenu(true);
    }
  });

  navbar.addEventListener('focusin', showNavbar);

  const handleViewportChange = (event) => {
    if (!event.matches && mobileMenu.classList.contains('open')) {
      closeMenu();
    }

    showNavbar();
  };

  if (typeof mobileViewportMedia.addEventListener === 'function') {
    mobileViewportMedia.addEventListener('change', handleViewportChange);
  } else {
    mobileViewportMedia.addListener(handleViewportChange);
  }

  if (shouldAutoHide) {
    let lastScrollY = Math.max(window.scrollY, 0);
    let scrollFramePending = false;

    const updateNavbarVisibility = () => {
      const currentScrollY = Math.max(window.scrollY, 0);
      const scrollingDown = currentScrollY > lastScrollY;
      const scrollingUp = currentScrollY < lastScrollY;
      const menuIsOpen = mobileMenu.classList.contains('open');
      const focusIsInNavbar = navbar.contains(document.activeElement);

      if (
        reducedMotionMedia.matches
        ||
        currentScrollY <= 72
        || scrollingUp
        || menuIsOpen
        || focusIsInNavbar
      ) {
        showNavbar();
      } else if (scrollingDown && currentScrollY > 120) {
        navbar.classList.add('navbar-hidden');
      }

      lastScrollY = currentScrollY;
      scrollFramePending = false;
    };

    window.addEventListener('scroll', () => {
      if (!scrollFramePending) {
        window.requestAnimationFrame(updateNavbarVisibility);
        scrollFramePending = true;
      }
    }, { passive: true });

    window.addEventListener('pageshow', () => {
      lastScrollY = Math.max(window.scrollY, 0);

      if (lastScrollY <= 72) {
        showNavbar();
      }
    });

    const handleReducedMotionChange = () => {
      showNavbar();
      lastScrollY = Math.max(window.scrollY, 0);
    };

    if (typeof reducedMotionMedia.addEventListener === 'function') {
      reducedMotionMedia.addEventListener('change', handleReducedMotionChange);
    } else {
      reducedMotionMedia.addListener(handleReducedMotionChange);
    }
  }

  syncMenuState();
})();
