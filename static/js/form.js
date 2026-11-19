/**
 * SAT ALFA - Application Forms AJAX Submission & Phone Mask
 * Handles both the contact card form and the application popup modal form.
 */

document.addEventListener('DOMContentLoaded', () => {
  // Select all application forms (via data-apply-form or honeypot website field)
  const forms = document.querySelectorAll('form[data-apply-form], form:has(input[name="website"])');
  const targetForms = forms.length > 0
    ? forms
    : Array.from(document.querySelectorAll('form')).filter((f) => f.querySelector('input[name="website"]'));

  if (!targetForms.length) return;

  // Phone input mask formatter (+998 (XX) XXX-XX-XX)
  const formatPhoneValue = (raw) => {
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

  targetForms.forEach((form) => {
    const submitBtn = form.querySelector('button[type="submit"]');
    let messageBox = form.querySelector('.form-message');

    if (!messageBox) {
      messageBox = document.createElement('div');
      messageBox.className = 'form-message';
      if (submitBtn) {
        form.insertBefore(messageBox, submitBtn);
      } else {
        form.appendChild(messageBox);
      }
    }

    const successText = form.getAttribute('data-success') || 'Your application has been received!';
    const errorText = form.getAttribute('data-error') || 'An error occurred. Please check your information.';

    // Initialize phone mask for this form
    const phoneInput = form.querySelector('input[name="phone"], input[type="tel"]');
    if (phoneInput && !phoneInput.dataset.maskInitialized) {
      phoneInput.dataset.maskInitialized = 'true';

      phoneInput.addEventListener('focus', () => {
        if (!phoneInput.value) {
          phoneInput.value = '+998 (';
        }
      });

      phoneInput.addEventListener('blur', () => {
        if (phoneInput.value === '+998 (' || phoneInput.value === '+998') {
          phoneInput.value = '';
        }
      });

      phoneInput.addEventListener('input', () => {
        phoneInput.value = formatPhoneValue(phoneInput.value);
      });

      phoneInput.addEventListener('keydown', (e) => {
        if (e.key === 'Backspace' && phoneInput.value.length <= 6) {
          e.preventDefault();
          phoneInput.value = '';
        }
      });
    }

    // Helper to get CSRF token from this specific form
    const getCsrfToken = () => {
      const csrfInput = form.querySelector('[name=csrfmiddlewaretoken]');
      if (csrfInput && csrfInput.value) return csrfInput.value;

      const cookieMatch = document.cookie.match(/csrftoken=([^;]+)/);
      return cookieMatch ? cookieMatch[1] : '';
    };

    // Flag to prevent double submission if clicked quickly
    let isSubmitting = false;

    // Use capture phase to intercept submit before any bubble-phase listeners
    form.addEventListener(
      'submit',
      async (e) => {
        e.preventDefault();
        e.stopImmediatePropagation();

        if (isSubmitting) return;

        const nameInput = form.querySelector('input[name="name"]');
        const currentPhoneInput = form.querySelector('input[name="phone"], input[type="tel"]');

        if (!nameInput || !currentPhoneInput) return;

        isSubmitting = true;

        // Reset status message
        messageBox.style.display = 'none';
        messageBox.className = 'form-message';
        messageBox.textContent = '';

        // Disable button and add loading state
        if (submitBtn) {
          submitBtn.disabled = true;
          submitBtn.classList.add('loading');
        }

        try {
          const formData = new FormData(form);
          const actionUrl = form.getAttribute('action') || window.location.pathname;

          const response = await fetch(actionUrl, {
            method: 'POST',
            headers: {
              'X-CSRFToken': getCsrfToken(),
              'X-Requested-With': 'XMLHttpRequest',
            },
            body: formData,
          });

          const data = await response.json().catch(() => ({}));

          if (response.ok && data.ok) {
            messageBox.textContent = successText;
            messageBox.className = 'form-message form-message--success';
            messageBox.style.color = '#0D0C11';
            messageBox.style.background = '#F1FF0A';
            messageBox.style.padding = '12px 16px';
            messageBox.style.borderRadius = '30px';
            messageBox.style.fontSize = '14px';
            messageBox.style.fontWeight = '600';
            messageBox.style.textAlign = 'center';
            messageBox.style.marginBottom = '8px';
            messageBox.style.display = 'block';
            form.reset();

            // Check if this form is inside the modal
            const modal = form.closest('.apply-modal') || form.closest('[role="dialog"]');
            if (modal) {
              setTimeout(() => {
                const closeBtn = modal.querySelector('.apply-modal-close') || modal.querySelector('[aria-label*="Close" i]');
                if (closeBtn) {
                  closeBtn.click();
                } else {
                  modal.setAttribute('aria-hidden', 'true');
                  modal.classList.remove('open');
                  document.body.style.overflow = '';
                }
              }, 2500);
            }
          } else {
            messageBox.textContent = errorText;
            messageBox.className = 'form-message form-message--error';
            messageBox.style.color = '#FFFFFF';
            messageBox.style.background = '#E53935';
            messageBox.style.padding = '12px 16px';
            messageBox.style.borderRadius = '30px';
            messageBox.style.fontSize = '14px';
            messageBox.style.fontWeight = '600';
            messageBox.style.textAlign = 'center';
            messageBox.style.marginBottom = '8px';
            messageBox.style.display = 'block';
          }
        } catch (err) {
          messageBox.textContent = errorText;
          messageBox.className = 'form-message form-message--error';
          messageBox.style.color = '#FFFFFF';
          messageBox.style.background = '#E53935';
          messageBox.style.padding = '12px 16px';
          messageBox.style.borderRadius = '30px';
          messageBox.style.fontSize = '14px';
          messageBox.style.fontWeight = '600';
          messageBox.style.textAlign = 'center';
          messageBox.style.marginBottom = '8px';
          messageBox.style.display = 'block';
        } finally {
          isSubmitting = false;
          if (submitBtn) {
            submitBtn.disabled = false;
            submitBtn.classList.remove('loading');
          }
        }
      },
      true
    );
  });
});
