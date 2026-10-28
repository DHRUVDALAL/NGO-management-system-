// Form Interactions & Validation
document.addEventListener('DOMContentLoaded', () => {
  // 1. Donation Amount Preset Selector
  const presetChips = document.querySelectorAll('.preset-chip');
  const customAmountInput = document.getElementById('custom_amount');

  if (presetChips.length > 0 && customAmountInput) {
    presetChips.forEach(chip => {
      chip.addEventListener('click', () => {
        presetChips.forEach(c => c.classList.remove('active'));
        chip.classList.add('active');
        const amount = chip.getAttribute('data-amount');
        customAmountInput.value = amount;
      });
    });

    customAmountInput.addEventListener('input', () => {
      presetChips.forEach(chip => {
        if (chip.getAttribute('data-amount') === customAmountInput.value.trim()) {
          chip.classList.add('active');
        } else {
          chip.classList.remove('active');
        }
      });
    });
  }

  // 2. Payment Method Card Selector
  const paymentCards = document.querySelectorAll('.payment-method-card');
  paymentCards.forEach(card => {
    card.addEventListener('click', () => {
      paymentCards.forEach(c => c.classList.remove('selected'));
      card.classList.add('selected');
      const radio = card.querySelector('input[type="radio"]');
      if (radio) radio.checked = true;
    });
  });

  // 3. Form Validation Enhancements
  const forms = document.querySelectorAll('form[data-validate="true"]');
  forms.forEach(form => {
    form.addEventListener('submit', (e) => {
      let isValid = true;
      const requiredInputs = form.querySelectorAll('[required]');

      requiredInputs.forEach(input => {
        if (!input.value.trim()) {
          isValid = false;
          input.classList.add('is-invalid');
          input.style.borderColor = 'var(--rose-500)';
        } else {
          input.classList.remove('is-invalid');
          input.style.borderColor = '';
        }
      });

      if (!isValid) {
        e.preventDefault();
        alert('Please fill in all required fields marked with *');
      }
    });
  });
});
