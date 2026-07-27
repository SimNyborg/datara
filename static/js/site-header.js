(() => {
  const navbar = document.querySelector('.site-navbar--inner');
  const burger = navbar?.querySelector('#navbar-burger');
  const mobileMenu = navbar?.querySelector('#navbar-mobile-menu');

  if (!navbar || !burger || !mobileMenu) {
    return;
  }

  const syncMenuState = () => {
    const isOpen = mobileMenu.classList.contains('open');
    burger.classList.toggle('open', isOpen);
    burger.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
    burger.setAttribute(
      'aria-label',
      isOpen ? burger.dataset.labelClose : burger.dataset.labelOpen
    );
    navbar.classList.toggle('navbar-menu-open', isOpen);
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
})();
