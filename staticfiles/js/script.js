// ОДИН главный обработчик, который запускается после загрузки страницы
document.addEventListener('DOMContentLoaded', function () {

    // --- Логика для смены вида меню при прокрутке ---
    const navbar = document.getElementById('navbar');
    if (navbar) {
        const logo = document.getElementById('logo-img');
        const logoWhite = logo.getAttribute('data-logo-white');
        const logoRgb = logo.getAttribute('data-logo-rgb');
        const navLinks = navbar.querySelectorAll('a');

        const updateNavbar = () => {
            if (window.scrollY > 50) {
                navbar.classList.add('bg-white', 'shadow-md');
                navbar.classList.remove('bg-digitalem-navy');
                logo.src = logoRgb;
                navLinks.forEach(link => {
                    link.classList.add('text-gray-800');
                    link.classList.remove('text-white');
                });
            } else {
                navbar.classList.remove('bg-white', 'shadow-md');
                navbar.classList.add('bg-digitalem-navy');
                logo.src = logoWhite;
                navLinks.forEach(link => {
                    link.classList.remove('text-gray-800');
                    link.classList.add('text-white');
                });
            }
        };
        updateNavbar();
        window.addEventListener('scroll', updateNavbar);
    }


    // --- Логика для отправки контактной формы ---
    const contactForm = document.getElementById('contact-form');
    if (contactForm) {
        contactForm.addEventListener('submit', async function (event) {
            event.preventDefault();
            const submitBtn = this.querySelector('button[type="submit"]');
            const submitText = submitBtn.querySelector('.submit-text');
            submitBtn.disabled = true;
            submitText.textContent = 'Отправка...';
            // ... остальная логика отправки ...
            console.log('Форма отправлена (симуляция)');
            await new Promise(resolve => setTimeout(resolve, 1000));
            showNotification('Сообщение успешно отправлено!', 'success');
            this.reset();
            submitBtn.disabled = false;
            submitText.textContent = 'Отправить сообщение';
        });
    }


    // --- Логика для анимации появления секций при прокрутке ---
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-fade-in-up');
            }
        });
    }, { threshold: 0.1 });
    document.querySelectorAll('section').forEach(section => {
        observer.observe(section);
    });


    // --- Логика для кнопки "Подробнее" ---
    const showBtn = document.getElementById('show-details-btn');
    const hideBtn = document.getElementById('hide-details-btn');
    const detailsBlock = document.getElementById('detailed-info-block');

    if (showBtn && detailsBlock) {
        showBtn.addEventListener('click', function() {
            detailsBlock.classList.remove('hidden');
            detailsBlock.scrollIntoView({ behavior: 'smooth', block: 'start' });
        });
    }

    if (hideBtn && detailsBlock) {
        hideBtn.addEventListener('click', function() {
            detailsBlock.classList.add('hidden');
        });
    }


    // --- Вспомогательная функция для уведомлений ---
    function showNotification(message, type = 'success') {
        const existingNotification = document.querySelector('.notification');
        if (existingNotification) {
            existingNotification.remove();
        }
        const notification = document.createElement('div');
        notification.className = `notification ${type}`;
        const icon = type === 'success' ? 'fas fa-check-circle' : 'fas fa-exclamation-triangle';
        notification.innerHTML = `<i class="${icon} icon"></i><span>${message}</span>`;
        document.body.appendChild(notification);
        setTimeout(() => {
            notification.classList.add('show');
        }, 100);
        setTimeout(() => {
            notification.classList.remove('show');
            setTimeout(() => {
                notification.remove();
            }, 500);
        }, 3000);
    }

}); // <-- Конец главного обработчика DOMContentLoaded