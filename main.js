
function translateDOM(lang) {
    const translations = window.i18n[lang];
    if (!translations) return;

    // 1. Translate elements with data-i18n attribute
    document.querySelectorAll('[data-i18n]').forEach(el => {
        const key = el.getAttribute('data-i18n');
        if (translations[key]) {
            if (el.tagName === 'INPUT' || el.tagName === 'TEXTAREA') {
                el.placeholder = translations[key];
            } else {
                el.textContent = translations[key];
            }
        }
    });

    // 2. Translate hardcoded text nodes using the global dictionary (one-way mapping for legacy support)
    // We'll build a reverse dictionary if it's 'en', but it's easier to just use the original text saved on the node
    const walk = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT, null, false);
    let n;
    while(n = walk.nextNode()) {
        const parent = n.parentElement;
        if(parent && parent.tagName !== 'SCRIPT' && parent.tagName !== 'STYLE' && !parent.hasAttribute('data-i18n')) {
            const trimmed = n.nodeValue.trim();
            if(trimmed.length > 1) {
                if(!n._ogText) {
                    n._ogText = trimmed;
                }
                const og = n._ogText;
                
                // Use a legacy mapping from window.i18n.ar (since keys are often English)
                if(lang === 'ar' && window.i18n.ar[og]) {
                   n.nodeValue = n.nodeValue.replace(trimmed, window.i18n.ar[og]);
                } else if(lang === 'en' && og) {
                   n.nodeValue = n.nodeValue.replace(trimmed, og);
                }
            }
        }
    }

    // 3. Update common attributes
    document.querySelectorAll('input[placeholder], textarea[placeholder]').forEach(el => {
        const ph = el.getAttribute('placeholder');
        if (lang === 'ar' && window.i18n.ar[ph]) {
            el.placeholder = window.i18n.ar[ph];
        }
    });
}

function updateLanguageUI(lang) {
    const isAr = lang === 'ar';
    document.documentElement.setAttribute('lang', lang);
    document.documentElement.setAttribute('dir', isAr ? 'rtl' : 'ltr');
    
    if (isAr) {
        document.body.classList.add('lang-ar');
    } else {
        document.body.classList.remove('lang-ar');
    }
    
    // Update all language select elements
    document.querySelectorAll('.custom-lang-select').forEach(select => {
        select.value = lang;
    });

    translateDOM(lang);
    
    // Re-initialize Lucide icons if needed
    if (window.lucide) {
        lucide.createIcons();
    }
}

window.switchLanguage = function (lang) {
    localStorage.setItem('shifa_lang', lang);
    // Update hash for consistency
    const url = new URL(window.location);
    url.hash = `lang=${lang}`;
    window.history.replaceState(null, '', url);
    updateLanguageUI(lang);
};

document.addEventListener('DOMContentLoaded', () => {
    const topBarContainer = document.querySelector('.top-bar-content');
    
    let currentLang = localStorage.getItem('shifa_lang') || 'en';
    if (window.location.hash.includes('lang=ar')) {
        currentLang = 'ar';
    }

    // Initial load
    updateLanguageUI(currentLang);

    // Sync with existing switcher or create one
    const existingPill = document.querySelector('.lang-pill-container');
    if (!existingPill && topBarContainer) {
        const langSwitcherWrapper = document.createElement('div');
        langSwitcherWrapper.className = 'custom-lang-wrapper';
        langSwitcherWrapper.innerHTML = `
            <div class="lang-pill-container" style="display: flex; align-items: center; gap: 8px;">
                <i data-lucide="globe" style="width: 14px; height: 14px; color: white;"></i>
                <select class="custom-lang-select" onchange="switchLanguage(this.value)">
                    <option value="en" ${currentLang === 'en' ? 'selected' : ''}>EN</option>
                    <option value="ar" ${currentLang === 'ar' ? 'selected' : ''}>العربية</option>
                </select>
            </div>
        `;

        const isMobile = window.innerWidth <= 1024;
        const target = isMobile ? document.querySelector('.nav-actions') : document.querySelector('.top-contact');
        if (target) {
            target.parentElement.insertBefore(langSwitcherWrapper, target);
        }
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
            navLinks.classList.toggle('active');
        });

        // Close menu when clicking a link
        navLinks.querySelectorAll('a').forEach(link => {
            link.addEventListener('click', () => {
                navLinks.classList.remove('active');
            });
        });

        // Close menu when clicking outside
        document.addEventListener('click', (e) => {
            if (!navbar.contains(e.target) && navLinks.classList.contains('active')) {
                navLinks.classList.remove('active');
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
