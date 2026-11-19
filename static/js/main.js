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

        const prefersReduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
        window.scrollTo({
          top: targetPosition,
          behavior: prefersReduced ? 'auto' : 'smooth',
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

  // 5. About Section Video Play Handler
  const aboutVideoWrap = document.getElementById('about-video-wrap');
  const aboutVideo = document.getElementById('about-video');
  const aboutPoster = document.getElementById('about-poster');
  const aboutPlayBtn = document.getElementById('about-play-btn');

  if (aboutVideo && aboutPlayBtn) {
    const playAboutVideo = () => {
      aboutPlayBtn.classList.add('hidden');
      if (aboutPoster) aboutPoster.classList.add('hidden');
      aboutVideo.classList.add('playing');
      aboutVideo.controls = true;
      aboutVideo.play().catch(() => {});
    };

    aboutPlayBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      playAboutVideo();
    });

    if (aboutVideoWrap) {
      aboutVideoWrap.addEventListener('click', () => {
        if (!aboutVideo.classList.contains('playing')) {
          playAboutVideo();
        }
      });
    }
  }

  // 6. FAQ Accordion (one open at a time, smooth transition)
  const faqAccordion = document.getElementById('faq-accordion');
  if (faqAccordion) {
    const faqItems = faqAccordion.querySelectorAll('.faq-item');

    faqItems.forEach((item) => {
      const btn = item.querySelector('.faq-question');
      const answer = item.querySelector('.faq-answer');

      if (!btn || !answer) return;

      btn.addEventListener('click', () => {
        const isOpen = item.classList.contains('open');

        // Close all items
        faqItems.forEach((other) => {
          if (other !== item && other.classList.contains('open')) {
            other.classList.remove('open');
            const otherBtn = other.querySelector('.faq-question');
            const otherAnswer = other.querySelector('.faq-answer');
            if (otherBtn) otherBtn.setAttribute('aria-expanded', 'false');
            if (otherAnswer) otherAnswer.style.maxHeight = null;
          }
        });

        // Toggle current item
        if (isOpen) {
          item.classList.remove('open');
          btn.setAttribute('aria-expanded', 'false');
          answer.style.maxHeight = null;
        } else {
          item.classList.add('open');
          btn.setAttribute('aria-expanded', 'true');
          answer.style.maxHeight = answer.scrollHeight + 'px';
        }
      });
    });
  }

  // 7. Phone Input Mask: +998 (XX) XXX-XX-XX
  const phoneInputs = document.querySelectorAll('#contact-phone, input[type="tel"]');
  phoneInputs.forEach((input) => {
    const formatValue = (raw) => {
      let digits = raw.replace(/\D/g, '');
      if (digits.startsWith('998')) {
        digits = digits.slice(3);
      }
      digits = digits.slice(0, 9);

      if (!digits.length) return '';

      let res = '+998';
      if (digits.length > 0) {
        res += ' (' + digits.slice(0, 2);
      }
      if (digits.length >= 2) {
        res += ') ';
      }
      if (digits.length > 2) {
        res += digits.slice(2, 5);
      }
      if (digits.length >= 5) {
        res += '-';
      }
      if (digits.length > 5) {
        res += digits.slice(5, 7);
      }
      if (digits.length >= 7) {
        res += '-';
      }
      if (digits.length > 7) {
        res += digits.slice(7, 9);
      }
      return res;
    };

    input.addEventListener('focus', () => {
      if (!input.value) {
        input.value = '+998 (';
      }
    });

    input.addEventListener('blur', () => {
      if (input.value === '+998 (' || input.value === '+998') {
        input.value = '';
      }
    });

    input.addEventListener('input', () => {
      input.value = formatValue(input.value);
    });

    input.addEventListener('keydown', (e) => {
      if (e.key === 'Backspace' && input.value.length <= 6) {
        e.preventDefault();
        input.value = '';
      }
    });
  });
});
