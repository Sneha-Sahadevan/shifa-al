window.googleTranslateElementInit = function () {
    new google.translate.TranslateElement({
        pageLanguage: 'en',
        includedLanguages: 'ar,en', // Provide English and Arabic
        autoDisplay: false
    }, 'google_translate_element');
};

window.switchLanguage = function (lang) {
    document.cookie = `googtrans=/en/${lang}; path=/`;
    if (window.location.hostname !== '') {
        document.cookie = `googtrans=/en/${lang}; domain=${window.location.hostname}; path=/`;
    }
    window.location.reload();
};

document.addEventListener('DOMContentLoaded', () => {
    // --- Inject Custom Language Switcher ---
    const topBarContainer = document.querySelector('.top-bar-content');
    if (topBarContainer) {
        let currentLang = 'en';
        if (document.cookie.includes('googtrans=/en/ar') || document.cookie.includes('googtrans=%2Fen%2Far')) {
            currentLang = 'ar';
        }

        // Set attributes for CSS-based language switching
        if (currentLang === 'ar') {
            document.documentElement.setAttribute('lang', 'ar');
            document.body.classList.add('lang-ar');
        } else {
            document.documentElement.setAttribute('lang', 'en');
            document.body.classList.remove('lang-ar');
        }

        const langSwitcherWrapper = document.createElement('div');
        langSwitcherWrapper.className = 'custom-lang-wrapper';
        langSwitcherWrapper.innerHTML = `
            <div style="display: flex; align-items: center; gap: 5px; margin: 0 15px;">
                <i data-lucide="globe" style="width: 14px; height: 14px; color: white;"></i>
                <select class="custom-lang-select" onchange="switchLanguage(this.value)" style="background: transparent; border: none; color: white; font-family: 'Open Sans', sans-serif; font-size: 0.85rem; outline: none; cursor: pointer; padding: 2px 5px; border-radius: 4px;">
                    <option value="en" style="color: #333;" ${currentLang === 'en' ? 'selected' : ''}>English</option>
                    <option value="ar" style="color: #333;" ${currentLang === 'ar' ? 'selected' : ''}>Arabic (العربية)</option>
                </select>
            </div>
            <div id="google_translate_element" style="display:none;"></div>
        `;

        // Insert it before the contact info
        const topContactElement = document.querySelector('.top-contact');
        if (topContactElement) {
            topBarContainer.insertBefore(langSwitcherWrapper, topContactElement);
        }

        const gtScript = document.createElement('script');
        gtScript.src = 'https://translate.google.com/translate_a/element.js?cb=googleTranslateElementInit';
        document.body.appendChild(gtScript);
    }

    // Initialize Lucide icons
    lucide.createIcons();

    // Sticky Navbar on Scroll
    const navbar = document.getElementById('navbar');
    if (navbar) {
        window.addEventListener('scroll', () => {
            if (window.scrollY > 50) {
                navbar.classList.add('scrolled');
            } else {
                navbar.classList.remove('scrolled');
            }
        });
    }

    // Mobile Navigation Toggle
    const mobileToggle = document.getElementById('mobile-toggle');
    const navLinks = document.getElementById('nav-links');

    if (mobileToggle) {
        mobileToggle.addEventListener('click', () => {
            navLinks.style.display = navLinks.style.display === 'flex' ? 'none' : 'flex';
            if (navLinks.style.display === 'flex') {
                navLinks.style.flexDirection = 'column';
                navLinks.style.position = 'absolute';
                navLinks.style.top = '80px';
                navLinks.style.left = '0';
                navLinks.style.width = '100%';
                navLinks.style.background = 'white';
                navLinks.style.padding = '20px';
                navLinks.style.textAlign = 'center';
            }
        });
    }

    // Smooth Scrolling for Navigation Links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth'
                });

                // Update active link
                document.querySelectorAll('.nav-links a').forEach(link => {
                    link.classList.remove('active');
                });
                this.classList.add('active');

                // Close mobile menu if open
                if (window.innerWidth <= 768) {
                    navLinks.style.display = 'none';
                }
            }
        });
    });

    // Intersection Observer for scroll animations
    const observerOptions = {
        threshold: 0.1
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in-up');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    document.querySelectorAll('.service-card, .glass-card, .doctor-card, .info-card').forEach(el => {
        el.classList.add('opacity-0'); // Initial state
        observer.observe(el);
    });

    // Form Submission Handling
    const contactForm = document.querySelector('.contact-form');
    if (contactForm) {
        contactForm.addEventListener('submit', (e) => {
            e.preventDefault();
            alert('Thank you for your message! Our team will get back to you shortly.');
            contactForm.reset();
        });
    }
    // Doctor Modal Logic
    const doctorCards = document.querySelectorAll('.practitioner-card');
    const modalOverlay = document.getElementById('doctor-modal');

    if (doctorCards.length > 0 && modalOverlay) {
        const modalClose = document.getElementById('modal-close');
        const modalImg = document.getElementById('modal-img');
        const modalName = document.getElementById('modal-name');
        const modalSpec = document.getElementById('modal-spec');
        const modalTime = document.getElementById('modal-time');
        const modalDesc = document.getElementById('modal-desc');

        doctorCards.forEach(card => {
            card.addEventListener('click', () => {
                // Populate data from elements instead of attributes
                const img = card.querySelector('.practitioner-img');
                const name = card.querySelector('.practitioner-name');
                const spec = card.querySelector('.practitioner-spec');
                const time = card.querySelector('.practitioner-schedule');
                const desc = card.querySelector('.practitioner-hover-info p');

                if (img) {
                    // Show the FULL image (non-standardized version if available)
                    let fullImgSrc = img.src;
                    if (fullImgSrc.includes('_standard.png')) {
                        fullImgSrc = fullImgSrc.replace('_standard.png', '.png');
                    }
                    modalImg.src = fullImgSrc;

                    // Fallback to .jpg if the high-res .png original is missing
                    modalImg.onerror = function() {
                        if (this.src.endsWith('.png')) {
                           this.src = this.src.replace('.png', '.jpg');
                           this.onerror = null; // Prevent infinite loop
                        }
                    };
                }
                if (name) modalName.textContent = name.textContent;
                if (spec) modalSpec.textContent = spec.textContent;
                if (time) modalTime.textContent = time.textContent;
                if (desc) modalDesc.textContent = desc.textContent;

                // Open modal
                modalOverlay.classList.add('active');
            });
        });

        // Close on X button
        modalClose.addEventListener('click', () => {
            modalOverlay.classList.remove('active');
        });

        // Close on clicking outside the modal content
        modalOverlay.addEventListener('click', (e) => {
            if (e.target === modalOverlay) {
                modalOverlay.classList.remove('active');
            }
        });
    }

    // Trigger backend API call on Book Now interactions
    document.querySelectorAll('.offer-card a.btn-primary').forEach(btn => {
        if (btn.textContent.trim() === 'Book Now') {
            btn.addEventListener('click', () => {
                const card = btn.closest('.offer-card');
                const deptName = card && card.querySelector('h3') ? card.querySelector('h3').textContent.trim() : 'Unknown Service';
                
                fetch('/api/notify-booking', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        message: `User clicked Book Now for ${deptName} on the website.`,
                        department: deptName
                    })
                }).catch(err => console.error('Backend notification failed:', err));
            });
        }
    });

});

// Helper for mobile styles
const style = document.createElement('style');
style.innerHTML = `
    .opacity-0 {
        opacity: 0;
    }
`;
document.head.appendChild(style);
