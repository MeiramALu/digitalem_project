document.addEventListener('DOMContentLoaded', function () {
    const navbar = document.getElementById('navbar');
    const logo = document.getElementById('logo-img');
    const mobileMenuIcon = document.getElementById('mobile-menu-icon');

    const gradientClasses = ['bg-gradient-to-r', 'from-digitalem-blue', 'via-digitalem-accent', 'to-digitalem-light'];

    if (navbar && logo) {
        const logoWhite = logo.getAttribute('data-logo-white');
        const logoRgb = logo.getAttribute('data-logo-rgb');

        const navLinks = navbar.querySelectorAll('.hidden.md\\:flex a');
        const langButtons = navbar.querySelectorAll('button[name="language"]');

        let activeLangBtn = null;
        langButtons.forEach(btn => {
            if (btn.classList.contains('bg-white')) {
                activeLangBtn = btn;
            }
        });

        const updateNavbar = () => {
            const isScrolled = window.scrollY > 20;

            if (isScrolled) {
                navbar.classList.remove(...gradientClasses);
                navbar.classList.add('bg-white', 'shadow-md');

                if (logoRgb) logo.src = logoRgb;

                navLinks.forEach(link => {
                    link.classList.remove('text-white', 'hover:text-blue-200');
                    link.classList.add('text-digitalem-navy', 'hover:text-digitalem-accent');
                });

                if (mobileMenuIcon) {
                    mobileMenuIcon.classList.remove('text-white');
                    mobileMenuIcon.classList.add('text-digitalem-navy');
                }

                langButtons.forEach(btn => {
                    if (btn === activeLangBtn) {
                        btn.classList.remove('bg-white', 'text-digitalem-blue', 'text-gray-600');
                        btn.classList.add('bg-digitalem-blue', 'text-white');
                    } else {
                        btn.classList.remove('text-white', 'hover:bg-white/20');
                        btn.classList.add('text-gray-600', 'hover:bg-gray-100');
                    }
                });

            } else {
                navbar.classList.remove('bg-white', 'shadow-md');
                navbar.classList.add(...gradientClasses);

                if (logoWhite) logo.src = logoWhite;

                navLinks.forEach(link => {
                    link.classList.remove('text-digitalem-navy', 'hover:text-digitalem-accent');
                    link.classList.add('text-white', 'hover:text-blue-200');
                });

                if (mobileMenuIcon) {
                    mobileMenuIcon.classList.remove('text-digitalem-navy');
                    mobileMenuIcon.classList.add('text-white');
                }

                langButtons.forEach(btn => {
                    if (btn === activeLangBtn) {
                        btn.classList.remove('bg-digitalem-blue', 'text-white', 'text-gray-600');
                        btn.classList.add('bg-white', 'text-digitalem-blue');
                    } else {
                        btn.classList.remove('text-gray-600', 'hover:bg-gray-100');
                        btn.classList.add('text-white', 'hover:bg-white/20');
                    }
                });
            }
        };

        updateNavbar();
        window.addEventListener('scroll', updateNavbar);
    }

    const mobileMenuButton = document.getElementById('mobile-menu-button');
    const mobileMenuPanel = document.getElementById('mobile-menu-panel');
    const mobileMenuOverlay = document.getElementById('mobile-menu-overlay');
    const mobileMenuCloseButton = document.getElementById('mobile-menu-close-button');

    const openMenu = () => {
        if (mobileMenuPanel && mobileMenuOverlay) {
            mobileMenuPanel.classList.remove('translate-x-full');
            mobileMenuOverlay.classList.remove('hidden');
            document.body.style.overflow = 'hidden';
        }
    };

    const closeMenu = () => {
        if (mobileMenuPanel && mobileMenuOverlay) {
            mobileMenuPanel.classList.add('translate-x-full');
            mobileMenuOverlay.classList.add('hidden');
            document.body.style.overflow = '';
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

    const showDetailsBtn = document.getElementById('show-details-btn');
    const hideDetailsBtn = document.getElementById('hide-details-btn');
    const detailedInfoBlock = document.getElementById('detailed-info-block');

    if (showDetailsBtn && detailedInfoBlock) {
        showDetailsBtn.addEventListener('click', function() {
            detailedInfoBlock.classList.remove('hidden');
            detailedInfoBlock.scrollIntoView({ behavior: 'smooth', block: 'start' });
        });
    }

    if (hideDetailsBtn && detailedInfoBlock) {
        hideDetailsBtn.addEventListener('click', function() {
            detailedInfoBlock.classList.add('hidden');
        });
    }

    const contactForm = document.getElementById('contact-form');
    if (contactForm) {
        contactForm.addEventListener('submit', async function (event) {
            event.preventDefault();
            console.log('Форма отправляется...');

            const submitBtn = this.querySelector('button[type="submit"]');
            const submitText = submitBtn.querySelector('.submit-text');
            const originalText = submitText ? submitText.textContent : 'Отправить';

            submitBtn.disabled = true;
            if (submitText) submitText.textContent = '...';

            const formData = new FormData(this);

            try {
                const response = await fetch('/send-telegram/', {
                    method: 'POST',
                    body: formData,
                    headers: { 'X-CSRFToken': getCookie('csrftoken') },
                });

                const result = await response.json();
                console.log('Ответ сервера:', result);

                if (result.success) {
                    showNotification('Сообщение успешно отправлено!', 'success');
                    this.reset();
                } else {
                    throw new Error(result.error || 'Ошибка отправки.');
                }
            } catch (error) {
                console.error('Ошибка:', error);
                showNotification('Ошибка связи с сервером', 'error');
            } finally {
                submitBtn.disabled = false;
                if (submitText) submitText.textContent = originalText;
            }
        });
    }

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-fade-in-up');
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.1 });

    document.querySelectorAll('section').forEach(section => {
        observer.observe(section);
    });

    function showNotification(message, type = 'success') {
        console.log('Попытка показать уведомление:', message);

        const existing = document.querySelector('.js-notification-custom');
        if (existing) existing.remove();

        const notification = document.createElement('div');
        notification.className = 'js-notification-custom';

        notification.style.position = 'fixed';
        notification.style.top = '100px';
        notification.style.right = '20px';
        notification.style.zIndex = '2147483647';
        notification.style.padding = '15px 25px';
        notification.style.borderRadius = '8px';
        notification.style.color = '#ffffff';
        notification.style.fontFamily = 'sans-serif';
        notification.style.fontWeight = '600';
        notification.style.boxShadow = '0 10px 15px -3px rgba(0, 0, 0, 0.1)';
        notification.style.transition = 'transform 0.3s ease-out, opacity 0.3s ease-out';
        notification.style.transform = 'translateX(120%)';
        notification.style.display = 'flex';
        notification.style.alignItems = 'center';
        notification.style.gap = '10px';

        if (type === 'success') {
            notification.style.backgroundColor = '#10B981';
            notification.innerHTML = `<span>✅</span> <span>${message}</span>`;
        } else {
            notification.style.backgroundColor = '#EF4444';
            notification.innerHTML = `<span>⚠️</span> <span>${message}</span>`;
        }

        document.body.appendChild(notification);

        setTimeout(() => {
            notification.style.transform = 'translateX(0)';
        }, 10);

        setTimeout(() => {
            notification.style.opacity = '0';
            notification.style.transform = 'translateX(120%)';
            setTimeout(() => notification.remove(), 300);
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
});