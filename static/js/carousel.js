/**
 * SAT ALFA - Reusable Carousel
 * Scroll-snap track, prev/next controls, and mouse-drag support.
 */

document.addEventListener('DOMContentLoaded', () => {
  const carousels = document.querySelectorAll('[data-carousel]');

  carousels.forEach((carousel) => {
    const track = carousel.querySelector('.carousel-track');
    const prevBtn = carousel.querySelector('.carousel-btn--prev');
    const nextBtn = carousel.querySelector('.carousel-btn--next');

    if (!track) return;

    // Helper to calculate scroll distance for one item
    const getScrollStep = () => {
      const firstItem = track.querySelector('.carousel-item');
      if (firstItem) {
        const style = window.getComputedStyle(track);
        const gap = parseFloat(style.gap) || 20;
        return firstItem.offsetWidth + gap;
      }
      return track.clientWidth * 0.75;
    };

    // Update disabled state of prev/next buttons
    const updateButtons = () => {
      const maxScroll = track.scrollWidth - track.clientWidth;
      if (prevBtn) {
        const atStart = track.scrollLeft <= 5;
        prevBtn.disabled = atStart;
        prevBtn.classList.toggle('disabled', atStart);
      }
      if (nextBtn) {
        const atEnd = track.scrollLeft >= maxScroll - 5;
        nextBtn.disabled = atEnd;
        nextBtn.classList.toggle('disabled', atEnd);
      }
    };

    if (prevBtn) {
      prevBtn.addEventListener('click', () => {
        const prefersReduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
        track.scrollBy({ left: -getScrollStep(), behavior: prefersReduced ? 'auto' : 'smooth' });
      });
    }

    if (nextBtn) {
      nextBtn.addEventListener('click', () => {
        const prefersReduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
        track.scrollBy({ left: getScrollStep(), behavior: prefersReduced ? 'auto' : 'smooth' });
      });
    }

    track.addEventListener('scroll', updateButtons, { passive: true });
    window.addEventListener('resize', updateButtons, { passive: true });
    setTimeout(updateButtons, 100);

    // Mouse drag scrolling
    let isDown = false;
    let startX = 0;
    let downPageX = 0;
    let scrollLeft = 0;
    let hasDragged = false;

    track.addEventListener('mousedown', (e) => {
      isDown = true;
      hasDragged = false;
      track.classList.add('is-dragging');
      startX = e.pageX - track.offsetLeft;
      downPageX = e.pageX;
      scrollLeft = track.scrollLeft;
    });

    const stopDragging = (e) => {
      if (!isDown) return;
      isDown = false;
      track.classList.remove('is-dragging');
      if (e && Math.abs(e.pageX - downPageX) > 6) {
        hasDragged = true;
      }
      updateButtons();
    };

    track.addEventListener('mouseleave', stopDragging);
    track.addEventListener('mouseup', stopDragging);

    track.addEventListener('mousemove', (e) => {
      if (!isDown) return;
      e.preventDefault();
      const x = e.pageX - track.offsetLeft;
      const walk = (x - startX) * 1.5;
      if (Math.abs(e.pageX - downPageX) > 6) {
        hasDragged = true;
      }
      track.scrollLeft = scrollLeft - walk;
    });

    // Prevent navigation/click if user was dragging
    track.addEventListener('click', (e) => {
      if (hasDragged) {
        e.preventDefault();
        e.stopPropagation();
      }
    }, true);
  });
});
