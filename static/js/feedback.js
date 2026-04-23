(function() {
    var modal = document.getElementById('feedbackModal');
    var form = document.getElementById('feedbackForm');
    var closeBtn = document.getElementById('modalClose');
    var successBlock = document.getElementById('modalSuccess');
    var messageEl = document.getElementById('modalMessage');
    var phoneInput = document.getElementById('phoneInput');

    // Lazy load reCAPTCHA
    var recaptchaLoaded = false;
    function loadRecaptcha() {
        if (recaptchaLoaded) return;
        recaptchaLoaded = true;
        var script = document.createElement('script');
        script.src = 'https://www.google.com/recaptcha/api.js';
        document.head.appendChild(script);
    }

    // Open modal
    document.querySelectorAll('[data-modal="feedback"]').forEach(function(btn) {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            loadRecaptcha();
            modal.classList.add('active');
            document.body.style.overflow = 'hidden';
        });
    });

    // Close modal
    function closeModal() {
        modal.classList.remove('active');
        document.body.style.overflow = '';
        setTimeout(function() {
            form.reset();
            form.style.display = '';
            successBlock.style.display = 'none';
            messageEl.textContent = '';
            messageEl.className = 'modal-message';
            clearErrors();
        }, 300);
    }

    closeBtn.addEventListener('click', closeModal);
    modal.addEventListener('click', function(e) {
        if (e.target === modal) closeModal();
    });
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && modal.classList.contains('active')) closeModal();
    });

    // Phone mask: +7 (999) 999-99-99
    phoneInput.addEventListener('input', function(e) {
        var val = phoneInput.value.replace(/\D/g, '');
        if (val.length === 0) { phoneInput.value = ''; return; }
        if (val[0] === '8') val = '7' + val.slice(1);
        if (val[0] !== '7') val = '7' + val;
        var result = '+7';
        if (val.length > 1) result += ' (' + val.substring(1, 4);
        if (val.length >= 4) result += ') ' + val.substring(4, 7);
        if (val.length >= 7) result += '-' + val.substring(7, 9);
        if (val.length >= 9) result += '-' + val.substring(9, 11);
        phoneInput.value = result;
    });

    phoneInput.addEventListener('keydown', function(e) {
        if (!/[0-9+\-() Backspace Delete Tab ArrowLeft ArrowRight]/.test(e.key) && !e.ctrlKey && !e.metaKey) {
            e.preventDefault();
        }
    });

    // Clear errors on input
    form.querySelectorAll('input, textarea').forEach(function(el) {
        el.addEventListener('input', function() {
            el.classList.remove('modal-input-error');
            var err = el.closest('.modal-form-group').querySelector('.modal-field-error');
            if (err) err.textContent = '';
        });
    });

    function clearErrors() {
        form.querySelectorAll('.modal-field-error').forEach(function(el) { el.textContent = ''; });
        form.querySelectorAll('.modal-input-error').forEach(function(el) { el.classList.remove('modal-input-error'); });
        document.getElementById('captchaError').textContent = '';
    }

    function showError(field, msg) {
        var input = form.querySelector('[name="' + field + '"]');
        if (input) {
            input.classList.add('modal-input-error');
            var err = input.closest('.modal-form-group').querySelector('.modal-field-error');
            if (err) err.textContent = msg;
        }
    }

    function validateEmail(email) {
        return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
    }

    function validateForm() {
        clearErrors();
        var valid = true;
        var firstName = form.querySelector('[name="first_name"]').value.trim();
        var lastName = form.querySelector('[name="last_name"]').value.trim();
        var phone = form.querySelector('[name="phone"]').value.trim();
        var email = form.querySelector('[name="email"]').value.trim();
        var message = form.querySelector('[name="message"]').value.trim();

        if (!firstName) { showError('first_name', 'Введите имя'); valid = false; }
        if (!lastName) { showError('last_name', 'Введите фамилию'); valid = false; }

        var digits = phone.replace(/\D/g, '');
        if (!phone || digits.length < 11) { showError('phone', 'Введите корректный номер телефона'); valid = false; }

        if (!email) { showError('email', 'Введите e-mail'); valid = false; }
        else if (!validateEmail(email)) { showError('email', 'Введите корректный e-mail'); valid = false; }

        if (!message) { showError('message', 'Введите сообщение'); valid = false; }

        var captcha = (typeof grecaptcha !== 'undefined') ? grecaptcha.getResponse() : '';
        if (!captcha) {
            document.getElementById('captchaError').textContent = 'Подтвердите, что вы не робот';
            valid = false;
        }

        return valid;
    }

    // Submit
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        if (!validateForm()) return;

        var submitBtn = form.querySelector('.btn-modal-submit');
        submitBtn.disabled = true;
        submitBtn.textContent = 'Отправка...';

        var formData = new FormData(form);

        fetch('/feedback/', {
            method: 'POST',
            body: formData
        })
        .then(function(r) { return r.json(); })
        .then(function(data) {
            submitBtn.disabled = false;
            submitBtn.textContent = 'Отправить';
            if (data.status) {
                form.style.display = 'none';
                successBlock.style.display = 'flex';
                setTimeout(closeModal, 3000);
            } else {
                if (data.error_captcha) {
                    document.getElementById('captchaError').textContent = data.error_captcha;
                }
                if (data.errors) {
                    for (var key in data.errors) {
                        showError(key, data.errors[key]);
                    }
                }
                if (typeof grecaptcha !== 'undefined') grecaptcha.reset();
            }
        })
        .catch(function() {
            submitBtn.disabled = false;
            submitBtn.textContent = 'Отправить';
            messageEl.textContent = 'Ошибка сети. Попробуйте позже.';
            messageEl.classList.add('modal-message-error');
        });
    });
})();
