/**
 * SAT ALFA - Contact Form AJAX Submission
 */

document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('contact-form');
  if (!form) return;

  const submitBtn = document.getElementById('contact-submit-btn') || form.querySelector('button[type="submit"]');
  const messageBox = document.getElementById('form-message') || document.createElement('div');

  if (!document.getElementById('form-message')) {
    messageBox.id = 'form-message';
    messageBox.className = 'form-message';
    form.insertBefore(messageBox, submitBtn);
  }

  const successText = form.getAttribute('data-success') || 'Your application has been received!';
  const errorText = form.getAttribute('data-error') || 'An error occurred. Please check your information.';

  // Helper to extract CSRF token
  const getCsrfToken = () => {
    const csrfInput = form.querySelector('[name=csrfmiddlewaretoken]');
    if (csrfInput && csrfInput.value) return csrfInput.value;

    const cookieMatch = document.cookie.match(/csrftoken=([^;]+)/);
    return cookieMatch ? cookieMatch[1] : '';
  };

  form.addEventListener('submit', async (e) => {
    e.preventDefault();

    const nameInput = document.getElementById('contact-name');
    const phoneInput = document.getElementById('contact-phone');

    if (!nameInput || !phoneInput) return;

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
      if (submitBtn) {
        submitBtn.disabled = false;
        submitBtn.classList.remove('loading');
      }
    }
  });
});
