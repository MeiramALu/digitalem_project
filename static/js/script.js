// /static/js/script.js

document.addEventListener('DOMContentLoaded', function () {

    const navbar = document.getElementById('navbar');
    const mobileMenuButton = document.getElementById('mobile-menu-button');
    const mobileMenuPanel = document.getElementById('mobile-menu-panel');
    const mobileMenuOverlay = document.getElementById('mobile-menu-overlay');
    const mobileMenuCloseButton = document.getElementById('mobile-menu-close-button');
    const mobileMenuIcon = document.getElementById('mobile-menu-icon');

    if (navbar) {
        const logo = document.getElementById('logo-img');
        const logoWhite = logo.getAttribute('data-logo-white');
        const logoRgb = logo.getAttribute('data-logo-rgb');
        const navLinks = navbar.querySelectorAll('.nav-link');
        const mobileNavLinks = mobileMenuPanel.querySelectorAll('.mobile-nav-link');
        const mobileMenuLogo = mobileMenuPanel.querySelector('.logo-text');

        const updateNavbar = () => {
            const isScrolled = window.scrollY > 50;

            navbar.classList.toggle('bg-white', isScrolled);
            navbar.classList.toggle('shadow-md', isScrolled);
            navbar.classList.toggle('gradient-bg', !isScrolled);
            logo.src = isScrolled ? logoRgb : logoWhite;

            navLinks.forEach(link => {
                link.classList.toggle('text-gray-800', isScrolled);
                link.classList.toggle('text-white', !isScrolled);
            });

            if (mobileMenuIcon) {
                mobileMenuIcon.classList.toggle('text-gray-800', isScrolled);
                mobileMenuIcon.classList.toggle('text-white', !isScrolled);
            }

            if (mobileMenuPanel) {
                mobileMenuPanel.classList.toggle('gradient-bg', isScrolled);
                mobileMenuPanel.classList.toggle('text-white', isScrolled);
                mobileMenuPanel.classList.toggle('bg-white', !isScrolled);
                mobileMenuPanel.classList.toggle('text-digitalem-navy', !isScrolled);

                if (mobileMenuLogo) {
                    mobileMenuLogo.classList.toggle('logo-text-inverted', isScrolled);
                }

                mobileNavLinks.forEach(link => {
                    link.classList.toggle('text-white', isScrolled);
                    link.classList.toggle('hover:text-blue-200', isScrolled);
                    link.classList.toggle('hover:text-digitalem-blue', !isScrolled);
                });
            }
        };

        updateNavbar();
        window.addEventListener('scroll', updateNavbar);
    }

    const openMenu = () => {
        if (mobileMenuPanel && mobileMenuOverlay) {
            mobileMenuPanel.classList.remove('translate-x-full');
            mobileMenuOverlay.classList.remove('hidden');
        }
    };

    const closeMenu = () => {
        if (mobileMenuPanel && mobileMenuOverlay) {
            mobileMenuPanel.classList.add('translate-x-full');
            mobileMenuOverlay.classList.add('hidden');
        }
    };

    if (mobileMenuButton) mobileMenuButton.addEventListener('click', openMenu);
    if (mobileMenuCloseButton) mobileMenuCloseButton.addEventListener('click', closeMenu);
    if (mobileMenuOverlay) mobileMenuOverlay.addEventListener('click', closeMenu);

    if (mobileMenuPanel) {
        mobileMenuPanel.querySelectorAll('a').forEach(link => {
            link.addEventListener('click', closeMenu);
        });
    }

    const contactForm = document.getElementById('contact-form');
    if (contactForm) {
        contactForm.addEventListener('submit', async function (event) {
            event.preventDefault();

            const submitBtn = this.querySelector('button[type="submit"]');
            const submitText = submitBtn.querySelector('.submit-text');
            submitBtn.disabled = true;
            submitText.textContent = 'Отправка...';

            const formData = new FormData(this);

            try {
                const response = await fetch('/send-telegram/', {
                    method: 'POST',
                    body: formData,
                    headers: { 'X-CSRFToken': getCookie('csrftoken') },
                });

                const result = await response.json();

                if (result.success) {
                    showNotification('Сообщение успешно отправлено!', 'success');
                    this.reset();
                } else {
                    throw new Error(result.error || 'Произошла ошибка на сервере.');
                }
            } catch (error) {
                console.error(error);
                showNotification(error.message, 'error');
            } finally {
                submitBtn.disabled = false;
                submitText.textContent = 'Отправить сообщение';
            }
        });
    }

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
        setTimeout(() => { notification.classList.add('show'); }, 100);
        setTimeout(() => {
            notification.classList.remove('show');
            setTimeout(() => { notification.remove(); }, 500);
        }, 3000);
    }

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

}); // <-- Конец ЕДИНОГО главного обработчика