/**
 * SAT ALFA - Main Client Scripts
 */

document.addEventListener('DOMContentLoaded', () => {
  const navbar = document.getElementById('main-navbar');
  const burgerBtn = document.getElementById('burger-btn');
  const mobileMenu = document.getElementById('mobile-menu');
  const mobileCloseBtn = document.getElementById('mobile-close-btn');
  const mobileLinks = document.querySelectorAll('.mobile-nav-item');

  // 1. Navbar scrolled state (via IntersectionObserver on hero section)
  const heroSection = document.getElementById('hero');
  if (navbar && heroSection && 'IntersectionObserver' in window) {
    const heroObserver = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          navbar.classList.toggle('is-scrolled', !entry.isIntersecting);
        });
      },
      {
        rootMargin: '-90px 0px 0px 0px',
        threshold: 0,
      }
    );
    heroObserver.observe(heroSection);
  }

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

  // 8. Application Modal
  const modal = document.getElementById('apply-modal');
  if (modal) {
    const backdrop = document.getElementById('modal-backdrop');
    const card = document.getElementById('modal-card');
    const closeBtn = document.getElementById('modal-close-btn');
    const prefersReduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    let triggerElement = null;

    const getFocusableElements = () => {
      return card.querySelectorAll(
        'a[href], button:not([disabled]), input:not([tabindex="-1"]), textarea, select, [tabindex]:not([tabindex="-1"])'
      );
    };

    const openModal = (trigger) => {
      triggerElement = trigger;
      modal.setAttribute('aria-hidden', 'false');
      modal.classList.add('open');
      document.body.style.overflow = 'hidden';

      // Focus the name input inside the modal
      const nameInput = document.getElementById('modal-name');
      if (nameInput) {
        setTimeout(() => nameInput.focus(), prefersReduced ? 0 : 150);
      }
    };

    const closeModal = () => {
      modal.setAttribute('aria-hidden', 'true');
      modal.classList.remove('open');
      document.body.style.overflow = '';

      if (triggerElement && typeof triggerElement.focus === 'function') {
        triggerElement.focus();
      }
      triggerElement = null;
    };

    // Open triggers
    document.querySelectorAll('[data-open-form]').forEach((el) => {
      el.addEventListener('click', (e) => {
        e.preventDefault();
        openModal(el);
      });
    });

    // Close triggers
    if (closeBtn) closeBtn.addEventListener('click', closeModal);
    if (backdrop) backdrop.addEventListener('click', closeModal);

    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && modal.classList.contains('open')) {
        closeModal();
      }
    });

    // Focus trap
    modal.addEventListener('keydown', (e) => {
      if (e.key !== 'Tab') return;
      const focusable = getFocusableElements();
      if (focusable.length === 0) return;

      const first = focusable[0];
      const last = focusable[focusable.length - 1];

      if (e.shiftKey) {
        if (document.activeElement === first) {
          e.preventDefault();
          last.focus();
        }
      } else {
        if (document.activeElement === last) {
          e.preventDefault();
          first.focus();
        }
      }
    });

    // Modal form AJAX submission (mirrors form.js for the modal form)
    const modalForm = document.getElementById('modal-form');
    if (modalForm) {
      const modalSubmitBtn = document.getElementById('modal-submit-btn') || modalForm.querySelector('button[type="submit"]');
      const modalMessage = document.getElementById('modal-message');

      const getCsrfToken = () => {
        const csrfInput = modalForm.querySelector('[name=csrfmiddlewaretoken]');
        if (csrfInput && csrfInput.value) return csrfInput.value;
        const cookieMatch = document.cookie.match(/csrftoken=([^;]+)/);
        return cookieMatch ? cookieMatch[1] : '';
      };

      const showMessage = (el, text, isSuccess) => {
        if (!el) return;
        el.textContent = text;
        el.style.color = isSuccess ? '#0D0C11' : '#FFFFFF';
        el.style.background = isSuccess ? '#F1FF0A' : '#E53935';
        el.style.padding = '12px 16px';
        el.style.borderRadius = '30px';
        el.style.fontSize = '14px';
        el.style.fontWeight = '600';
        el.style.textAlign = 'center';
        el.style.marginBottom = '8px';
        el.style.display = 'block';
      };

      modalForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        if (modalMessage) { modalMessage.style.display = 'none'; }
        if (modalSubmitBtn) { modalSubmitBtn.disabled = true; modalSubmitBtn.classList.add('loading'); }

        const successText = modalForm.getAttribute('data-success') || 'Your application has been received!';
        const errorText = modalForm.getAttribute('data-error') || 'An error occurred.';

        try {
          const formData = new FormData(modalForm);
          const actionUrl = modalForm.getAttribute('action') || window.location.pathname;
          const response = await fetch(actionUrl, {
            method: 'POST',
            headers: { 'X-CSRFToken': getCsrfToken(), 'X-Requested-With': 'XMLHttpRequest' },
            body: formData,
          });
          const data = await response.json().catch(() => ({}));

          if (response.ok && data.ok) {
            showMessage(modalMessage, successText, true);
            modalForm.reset();
          } else {
            showMessage(modalMessage, errorText, false);
          }
        } catch (err) {
          showMessage(modalMessage, errorText, false);
        } finally {
          if (modalSubmitBtn) { modalSubmitBtn.disabled = false; modalSubmitBtn.classList.remove('loading'); }
        }
      });
    }
  }
});
