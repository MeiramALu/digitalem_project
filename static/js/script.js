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
                    if (!btn.classList.contains('bg-white')) {
                        btn.classList.remove('text-white', 'hover:bg-white/20');
                        btn.classList.add('text-gray-600', 'hover:bg-gray-100');
                    } else {
                        btn.classList.remove('bg-white', 'text-digitalem-blue');
                        btn.classList.add('bg-digitalem-blue', 'text-white');
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
                    if (btn.classList.contains('text-gray-600')) {
                        btn.classList.remove('text-gray-600', 'hover:bg-gray-100');
                        btn.classList.add('text-white', 'hover:bg-white/20');
                    }
                    if (btn.classList.contains('bg-digitalem-blue')) {
                        btn.classList.remove('bg-digitalem-blue', 'text-white');
                        btn.classList.add('bg-white', 'text-digitalem-blue');
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
            showDetailsBtn.scrollIntoView({ behavior: 'smooth', block: 'center' });
        });
    }

    const contactForm = document.getElementById('contact-form');
    if (contactForm) {
        contactForm.addEventListener('submit', async function (event) {
            event.preventDefault();

            const submitBtn = this.querySelector('button[type="submit"]');
            const submitText = submitBtn.querySelector('.submit-text');
            const originalText = submitText.textContent;
            
            submitBtn.disabled = true;
            submitText.textContent = '...';

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
                    throw new Error(result.error || 'Ошибка отправки.');
                }
            } catch (error) {
                console.error(error);
                showNotification('Ошибка связи с сервером', 'error');
            } finally {
                submitBtn.disabled = false;
                submitText.textContent = originalText;
            }
        });
    }

    console.log("Ищу кнопку 'Подробнее' и связанный с ней блок...");

    const showBtn = document.getElementById('show-details-btn');
    console.log("Результат поиска кнопки 'Подробнее':", showBtn);

    const hideBtn = document.getElementById('hide-details-btn');
    console.log("Результат поиска кнопки 'Скрыть':", hideBtn);

    const detailsBlock = document.getElementById('detailed-info-block');
    console.log("Результат поиска блока с деталями:", detailsBlock);

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
        const existing = document.querySelector('.notification');
        if (existing) existing.remove();

        const notification = document.createElement('div');
        notification.className = `notification ${type} fixed top-24 right-5 p-4 rounded-xl text-white font-medium z-50 transform translate-x-full transition-all duration-300 shadow-2xl flex items-center max-w-sm`;

        if (type === 'success') {
            notification.classList.add('bg-emerald-500', 'border', 'border-emerald-400');
        } else {
            notification.classList.add('bg-red-500', 'border', 'border-red-400');
        }

        const icon = type === 'success' ? 'fa-check-circle' : 'fa-exclamation-circle';
        notification.innerHTML = `<i class="fas ${icon} mr-3 text-xl"></i><span>${message}</span>`;
        
        document.body.appendChild(notification);

        requestAnimationFrame(() => {
            notification.classList.remove('translate-x-full');
        });

        setTimeout(() => {
            notification.classList.add('translate-x-full', 'opacity-0');
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
