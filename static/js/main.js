/**
 * SAT ALFA - Main Client Scripts
 */

document.addEventListener('DOMContentLoaded', () => {
  const navbar = document.getElementById('main-navbar');
  const burgerBtn = document.getElementById('burger-btn');
  const mobileMenu = document.getElementById('mobile-menu');
  const mobileCloseBtn = document.getElementById('mobile-close-btn');
  const mobileLinks = document.querySelectorAll('.mobile-nav-item');

  // 1. Navbar scrolled state
  const updateNavbarState = () => {
    if (!navbar) return;
    const scrollThreshold = 50;
    if (window.scrollY > scrollThreshold) {
      navbar.classList.add('scrolled');
    } else {
      navbar.classList.remove('scrolled');
    }
  };

  window.addEventListener('scroll', updateNavbarState, { passive: true });
  updateNavbarState();

  // 2. Mobile Burger Menu
  const openMobileMenu = () => {
    if (!mobileMenu) return;
    mobileMenu.classList.add('open');
    mobileMenu.setAttribute('aria-hidden', 'false');
    if (burgerBtn) burgerBtn.setAttribute('aria-expanded', 'true');
    document.body.style.overflow = 'hidden';
  };

  const closeMobileMenu = () => {
    if (!mobileMenu) return;
    mobileMenu.classList.remove('open');
    mobileMenu.setAttribute('aria-hidden', 'true');
    if (burgerBtn) burgerBtn.setAttribute('aria-expanded', 'false');
    document.body.style.overflow = '';
  };

  if (burgerBtn) {
    burgerBtn.addEventListener('click', () => {
      const isOpen = mobileMenu && mobileMenu.classList.contains('open');
      if (isOpen) {
        closeMobileMenu();
      } else {
        openMobileMenu();
      }
    });
  }

  if (mobileCloseBtn) {
    mobileCloseBtn.addEventListener('click', closeMobileMenu);
  }

  mobileLinks.forEach((link) => {
    link.addEventListener('click', closeMobileMenu);
  });

  // 3. Smooth Anchor Scrolling with Navbar Offset
  const anchorLinks = document.querySelectorAll('a[href^="#"]');
  anchorLinks.forEach((anchor) => {
    anchor.addEventListener('click', (e) => {
      const href = anchor.getAttribute('href');
      if (!href || href === '#') return;

      const target = document.querySelector(href);
      if (target) {
        e.preventDefault();
        const navHeight = navbar ? navbar.offsetHeight : 64;
        const offset = 24; // extra breathing room
        const targetPosition = target.getBoundingClientRect().top + window.pageYOffset - (navHeight + offset);

        window.scrollTo({
          top: targetPosition,
          behavior: 'smooth',
        });

        if (window.history && window.history.pushState) {
          window.history.pushState(null, '', href);
        }
      }
    });
  });

  // 4. Subtle Fade-up on Scroll (IntersectionObserver)
  const fadeElements = document.querySelectorAll('.fade-up');
  const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  if (prefersReducedMotion || !('IntersectionObserver' in window)) {
    fadeElements.forEach((el) => el.classList.add('visible'));
  } else {
    const observer = new IntersectionObserver(
      (entries, obs) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add('visible');
            obs.unobserve(entry.target);
          }
        });
      },
      {
        threshold: 0.1,
        rootMargin: '0px 0px -40px 0px',
      }
    );

    fadeElements.forEach((el) => observer.observe(el));
  }
});
