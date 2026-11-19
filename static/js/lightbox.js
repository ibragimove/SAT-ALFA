/**
 * SAT ALFA - Official Result Image Lightbox
 */

document.addEventListener('DOMContentLoaded', () => {
  const lightbox = document.getElementById('result-lightbox');
  if (!lightbox) return;

  const backdrop = document.getElementById('lightbox-backdrop');
  const card = document.getElementById('lightbox-card');
  const closeBtn = document.getElementById('lightbox-close-btn');
  const studentNameEl = document.getElementById('lightbox-student-name');
  const scoreValEl = document.getElementById('lightbox-score-val');
  const imgEl = document.getElementById('lightbox-img');
  const loaderEl = document.getElementById('lightbox-loader');
  const origLink = document.getElementById('lightbox-orig-link');

  let triggerElement = null;

  const getFocusableElements = () => {
    return card.querySelectorAll(
      'a[href], button:not([disabled]), input:not([tabindex="-1"]), textarea, select, [tabindex]:not([tabindex="-1"])'
    );
  };

  const openLightbox = (trigger) => {
    triggerElement = trigger;

    const src = trigger.getAttribute('data-src') || '';
    const name = trigger.getAttribute('data-name') || '';
    const score = trigger.getAttribute('data-score') || '';

    if (studentNameEl) studentNameEl.textContent = name;
    if (scoreValEl) scoreValEl.textContent = score;
    if (origLink) origLink.setAttribute('href', src);
    lightbox.setAttribute('aria-label', name ? `${name} - Official Result` : 'Official Result');

    // Show gradient loader, hide image until loaded
    if (imgEl && loaderEl) {
      imgEl.style.display = 'none';
      loaderEl.style.display = 'block';

      imgEl.onload = () => {
        loaderEl.style.display = 'none';
        imgEl.style.display = 'block';
      };
      imgEl.onerror = () => {
        loaderEl.style.display = 'none';
        imgEl.style.display = 'block';
      };
      imgEl.src = src;
    }

    lightbox.setAttribute('aria-hidden', 'false');
    lightbox.classList.add('open');
    document.body.style.overflow = 'hidden';

    // Move focus into dialog
    if (closeBtn) {
      const prefersReduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
      setTimeout(() => closeBtn.focus(), prefersReduced ? 0 : 100);
    }
  };

  const closeLightbox = () => {
    lightbox.setAttribute('aria-hidden', 'true');
    lightbox.classList.remove('open');

    // If apply-modal is not open, restore scroll
    const applyModal = document.getElementById('apply-modal');
    if (!applyModal || !applyModal.classList.contains('open')) {
      document.body.style.overflow = '';
    }

    if (triggerElement && typeof triggerElement.focus === 'function') {
      triggerElement.focus();
    }
    triggerElement = null;

    // Reset image
    if (imgEl) {
      imgEl.src = '';
      imgEl.style.display = 'none';
    }
  };

  // Open triggers
  document.querySelectorAll('[data-lightbox]').forEach((el) => {
    el.addEventListener('click', (e) => {
      e.preventDefault();
      openLightbox(el);
    });
    el.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault();
        openLightbox(el);
      }
    });
  });

  // Close triggers
  if (closeBtn) closeBtn.addEventListener('click', closeLightbox);
  if (backdrop) backdrop.addEventListener('click', closeLightbox);

  // Escape key handler: use capture phase so if lightbox is on top,
  // it stops immediate propagation and closes only itself
  document.addEventListener(
    'keydown',
    (e) => {
      if (e.key === 'Escape' && lightbox.classList.contains('open')) {
        e.stopImmediatePropagation();
        e.preventDefault();
        closeLightbox();
      }
    },
    true
  );

  // Focus trap
  lightbox.addEventListener('keydown', (e) => {
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
});
