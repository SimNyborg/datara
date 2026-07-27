(() => {
  const navbar = document.querySelector('.site-navbar--inner');
  const burger = navbar?.querySelector('#navbar-burger');
  const mobileMenu = navbar?.querySelector('#navbar-mobile-menu');
  const shouldAutoHide = document.body.classList.contains('project-detail-page');

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

  const closeMenu = () => {
    mobileMenu.classList.remove('open');
    syncMenuState();
  };

  burger.addEventListener('click', () => {
    mobileMenu.classList.toggle('open');
    syncMenuState();
  });

  mobileMenu.querySelectorAll('a').forEach((link) => {
    link.addEventListener('click', closeMenu);
  });

  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape' && mobileMenu.classList.contains('open')) {
      closeMenu();
      burger.focus();
    }
  });

  navbar.addEventListener('focusin', showNavbar);

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
  }
})();
