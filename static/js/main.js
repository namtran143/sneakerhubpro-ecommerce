document.addEventListener('DOMContentLoaded', function () {
    const paymentRadios = document.querySelectorAll('.payment-options input[type="radio"]');
    paymentRadios.forEach((radio) => {
        radio.classList.add('form-check-input', 'me-2');
    });
});
