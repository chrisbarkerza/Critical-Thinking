// ADVANCED ANIMATION SYSTEM - NEXT LEVEL
// Using GSAP for professional-grade animations

document.addEventListener('DOMContentLoaded', () => {
    initializeAdvancedAnimations();
    initializeCursorSystem();
    initializeParticleSystem();
    initializeNavigation();
    initializeScrollTriggers();
    initializeInteractiveElements();
    initializeTimelineAnimations();
    initializeFacilitatorCarousel();
    initializeCounterAnimations();
    console.log('🚀 FutureForesight - Advanced Animation System Loaded');
});

// Advanced Cursor System
function initializeCursorSystem() {
    const cursor = document.querySelector('.cursor-trail');
    if (!cursor) return;

    let mouseX = 0, mouseY = 0;
    let cursorX = 0, cursorY = 0;

    document.addEventListener('mousemove', (e) => {
        mouseX = e.clientX;
        mouseY = e.clientY;
    });

    // Smooth cursor following
    function updateCursor() {
        const dx = mouseX - cursorX;
        const dy = mouseY - cursorY;
        
        cursorX += dx * 0.1;
        cursorY += dy * 0.1;
        
        gsap.set(cursor, {
            x: cursorX - 20,
            y: cursorY - 20,
            duration: 0.1
        });
        
        requestAnimationFrame(updateCursor);
    }
    updateCursor();

    // Cursor interactions
    const interactiveElements = document.querySelectorAll('a, button, .nav-link, .challenge-card, .diff-card-3d, .skill-item');
    
    interactiveElements.forEach(el => {
        el.addEventListener('mouseenter', () => {
            gsap.to(cursor, {
                scale: 1.5,
                borderColor: '#60a5fa',
                duration: 0.3
            });
        });
        
        el.addEventListener('mouseleave', () => {
            gsap.to(cursor, {
                scale: 1,
                borderColor: '#3b82f6',
                duration: 0.3
            });
        });
    });
}

// Advanced Particle System
function initializeParticleSystem() {
    const particlesContainer = document.getElementById('particles-bg');
    if (!particlesContainer) return;

    // Create floating particles
    for (let i = 0; i < 50; i++) {
        const particle = document.createElement('div');
        particle.style.cssText = `
            position: absolute;
            width: ${Math.random() * 4 + 2}px;
            height: ${Math.random() * 4 + 2}px;
            background: radial-gradient(circle, rgba(59, 130, 246, 0.6) 0%, transparent 70%);
            border-radius: 50%;
            pointer-events: none;
        `;
        
        particlesContainer.appendChild(particle);
        
        // Animate particles
        gsap.set(particle, {
            x: Math.random() * window.innerWidth,
            y: Math.random() * window.innerHeight,
        });
        
        gsap.to(particle, {
            x: `+=${Math.random() * 200 - 100}`,
            y: `+=${Math.random() * 200 - 100}`,
            duration: Math.random() * 20 + 10,
            repeat: -1,
            yoyo: true,
            ease: 'sine.inOut'
        });
        
        gsap.to(particle, {
            opacity: Math.random() * 0.5 + 0.2,
            duration: Math.random() * 3 + 2,
            repeat: -1,
            yoyo: true,
            ease: 'power2.inOut'
        });
    }
}

// Advanced Navigation System
function initializeNavigation() {
    const hamburger = document.querySelector('.hamburger');
    const navMenu = document.querySelector('.nav-menu');
    const navLinks = document.querySelectorAll('.nav-link');

    hamburger?.addEventListener('click', () => {
        navMenu.classList.toggle('active');
        
        // Animate hamburger
        gsap.to(hamburger.children, {
            rotation: navMenu.classList.contains('active') ? 45 : 0,
            transformOrigin: 'center',
            duration: 0.3,
            stagger: 0.1
        });
    });

    // Smooth scroll navigation
    navLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            const href = link.getAttribute('href');
            if (href.startsWith('#')) {
                e.preventDefault();
                const target = document.querySelector(href);
                if (target) {
                    gsap.to(window, {
                        scrollTo: {
                            y: target,
                            offsetY: 80
                        },
                        duration: 1.5,
                        ease: 'power3.inOut'
                    });
                }
            }
        });
    });

    // Active navigation highlighting
    function updateActiveNav() {
        const sections = document.querySelectorAll('section[id]');
        const scrollPos = window.scrollY + 100;

        sections.forEach(section => {
            const top = section.offsetTop;
            const bottom = top + section.offsetHeight;
            const id = section.getAttribute('id');
            const navLink = document.querySelector(`a[href=\"#${id}\"]`);

            if (scrollPos >= top && scrollPos <= bottom) {
                navLinks.forEach(link => link.classList.remove('active'));
                navLink?.classList.add('active');
            }
        });
    }

    window.addEventListener('scroll', updateActiveNav);
}

// Advanced Scroll Triggers
function initializeScrollTriggers() {
    gsap.registerPlugin(ScrollTrigger);

    // Hero parallax layers
    const heroLayers = document.querySelectorAll('.hero-layer');
    heroLayers.forEach((layer, index) => {
        const speed = layer.dataset.speed || 0.5;
        gsap.to(layer, {
            yPercent: -50 * speed,
            ease: 'none',
            scrollTrigger: {
                trigger: '.hero-section',
                start: 'top bottom',
                end: 'bottom top',
                scrub: true
            }
        });
    });

    // Stats cards reveal
    gsap.fromTo('.stat-card', {
        y: 100,
        opacity: 0,
        scale: 0.8
    }, {
        y: 0,
        opacity: 1,
        scale: 1,
        duration: 1,
        stagger: 0.2,
        ease: 'back.out(1.7)',
        scrollTrigger: {
            trigger: '.stats-grid-enhanced',
            start: 'top 80%',
            toggleActions: 'play none none reverse'
        }
    });

    // Challenge cards animation
    gsap.fromTo('.challenge-card', {
        rotationY: -90,
        opacity: 0
    }, {
        rotationY: 0,
        opacity: 1,
        duration: 1.2,
        stagger: 0.3,
        ease: 'power3.out',
        scrollTrigger: {
            trigger: '.challenge-grid',
            start: 'top 80%',
            toggleActions: 'play none none reverse'
        }
    });

    // Timeline items
    gsap.fromTo('.timeline-item', {
        x: (index) => index % 2 === 0 ? -100 : 100,
        opacity: 0
    }, {
        x: 0,
        opacity: 1,
        duration: 1,
        stagger: 0.3,
        ease: 'power3.out',
        scrollTrigger: {
            trigger: '.value-timeline',
            start: 'top 70%',
            toggleActions: 'play none none reverse'
        }
    });

    // 3D Cards entrance
    gsap.fromTo('.diff-card-3d', {
        rotationX: -90,
        y: 100,
        opacity: 0
    }, {
        rotationX: 0,
        y: 0,
        opacity: 1,
        duration: 1.5,
        stagger: 0.2,
        ease: 'power3.out',
        scrollTrigger: {
            trigger: '.diff-grid-3d',
            start: 'top 80%',
            toggleActions: 'play none none reverse'
        }
    });

    // Skills items slide in
    gsap.fromTo('.skill-item', {
        x: -50,
        opacity: 0
    }, {
        x: 0,
        opacity: 1,
        duration: 0.8,
        stagger: 0.1,
        ease: 'power2.out',
        scrollTrigger: {
            trigger: '.skills-interactive',
            start: 'top 80%',
            toggleActions: 'play none none reverse'
        }
    });

    // Floating professional animation
    gsap.to('.floating-professional', {
        y: -20,
        rotation: 2,
        duration: 3,
        repeat: -1,
        yoyo: true,
        ease: 'sine.inOut'
    });

    // Morphing background animation
    gsap.to('.morphing-bg', {
        rotation: 360,
        duration: 60,
        repeat: -1,
        ease: 'none'
    });
}

// Interactive Elements
function initializeInteractiveElements() {
    // 3D tilt effect for cards
    const tiltElements = document.querySelectorAll('[data-tilt]');
    
    tiltElements.forEach(el => {
        el.addEventListener('mousemove', (e) => {
            const rect = el.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            
            const centerX = rect.width / 2;
            const centerY = rect.height / 2;
            
            const rotateX = (y - centerY) / centerY * -10;
            const rotateY = (x - centerX) / centerX * 10;
            
            gsap.to(el, {
                rotationX: rotateX,
                rotationY: rotateY,
                transformPerspective: 1000,
                duration: 0.3,
                ease: 'power2.out'
            });
        });
        
        el.addEventListener('mouseleave', () => {
            gsap.to(el, {
                rotationX: 0,
                rotationY: 0,
                duration: 0.5,
                ease: 'power2.out'
            });
        });
    });

    // Skill items hover effect
    const skillItems = document.querySelectorAll('.skill-item');
    skillItems.forEach(item => {
        item.addEventListener('mouseenter', () => {
            gsap.to(item, {
                x: 15,
                scale: 1.02,
                duration: 0.3,
                ease: 'power2.out'
            });
            
            gsap.to(item.querySelector('.skill-icon'), {
                rotation: 5,
                scale: 1.1,
                duration: 0.3,
                ease: 'back.out(1.7)'
            });
        });
        
        item.addEventListener('mouseleave', () => {
            gsap.to(item, {
                x: 0,
                scale: 1,
                duration: 0.3,
                ease: 'power2.out'
            });
            
            gsap.to(item.querySelector('.skill-icon'), {
                rotation: 0,
                scale: 1,
                duration: 0.3,
                ease: 'power2.out'
            });
        });
    });

    // Challenge cards glow effect
    const challengeCards = document.querySelectorAll('.challenge-card');
    challengeCards.forEach(card => {
        card.addEventListener('mouseenter', () => {
            gsap.to(card, {
                scale: 1.05,
                boxShadow: '0 20px 40px rgba(59, 130, 246, 0.3)',
                duration: 0.3,
                ease: 'power2.out'
            });
        });
        
        card.addEventListener('mouseleave', () => {
            gsap.to(card, {
                scale: 1,
                boxShadow: '0 25px 50px -12px rgba(0, 0, 0, 0.25)',
                duration: 0.3,
                ease: 'power2.out'
            });
        });
    });
}

// Timeline Animations
function initializeTimelineAnimations() {
    const timelineItems = document.querySelectorAll('.timeline-item');
    
    timelineItems.forEach((item, index) => {
        const isEven = index % 2 === 0;
        
        ScrollTrigger.create({
            trigger: item,
            start: 'top 80%',
            onEnter: () => {
                item.classList.add('aos-animate');
                
                // Animate the marker
                gsap.fromTo(item.querySelector('.timeline-marker'), {
                    scale: 0,
                    rotation: -180
                }, {
                    scale: 1,
                    rotation: 0,
                    duration: 0.8,
                    ease: 'back.out(1.7)',
                    delay: 0.3
                });
                
                // Animate the content
                gsap.fromTo(item.querySelector('.timeline-content'), {
                    x: isEven ? -100 : 100,
                    opacity: 0,
                    rotationY: isEven ? -30 : 30
                }, {
                    x: 0,
                    opacity: 1,
                    rotationY: 0,
                    duration: 1,
                    ease: 'power3.out',
                    delay: 0.5
                });
            }
        });
    });
}

// Facilitator Carousel
function initializeFacilitatorCarousel() {
    const tabs = document.querySelectorAll('.tab');
    const categories = document.querySelectorAll('.achievement-category');
    
    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            const target = tab.dataset.target;
            
            // Update active tab
            tabs.forEach(t => t.classList.remove('active'));
            tab.classList.add('active');
            
            // Animate category switch
            categories.forEach(category => {
                if (category.dataset.category === target) {
                    gsap.set(category, { x: 50, opacity: 0 });
                    category.classList.add('active');
                    
                    gsap.to(category, {
                        x: 0,
                        opacity: 1,
                        duration: 0.6,
                        ease: 'power3.out'
                    });
                    
                    // Animate achievements
                    gsap.fromTo(category.querySelectorAll('.achievement'), {
                        x: 30,
                        opacity: 0
                    }, {
                        x: 0,
                        opacity: 1,
                        duration: 0.4,
                        stagger: 0.1,
                        ease: 'power2.out',
                        delay: 0.3
                    });
                } else {
                    category.classList.remove('active');
                }
            });
        });
    });
}

// Counter Animations
function initializeCounterAnimations() {
    const counters = document.querySelectorAll('.achievement-number');
    
    counters.forEach(counter => {
        const target = counter.dataset.count || counter.textContent.replace(/[^0-9]/g, '');
        const isPlus = counter.textContent.includes('+');
        
        ScrollTrigger.create({
            trigger: counter,
            start: 'top 80%',
            onEnter: () => {
                gsap.fromTo(counter, {
                    textContent: 0
                }, {
                    textContent: target,
                    duration: 2,
                    ease: 'power2.out',
                    snap: { textContent: 1 },
                    onUpdate: function() {
                        const current = Math.floor(this.targets()[0].textContent);
                        counter.textContent = (isPlus ? current + '+' : current);
                    }
                });
            }
        });
    });
}

// Advanced Initialization
function initializeAdvancedAnimations() {
    // Preload animations
    gsap.set('.hero-section', { opacity: 0 });
    gsap.set('.quote-intro, .cinematic-quote, .quote-author', { opacity: 0, y: 30 });
    gsap.set('.stats-title', { opacity: 0, y: 50 });
    gsap.set('.challenge-title', { opacity: 0, y: 30 });
    
    // Hero entrance animation
    const tl = gsap.timeline();
    
    tl.to('.hero-section', { opacity: 1, duration: 0.5 })
      .to('.quote-intro', { opacity: 1, y: 0, duration: 0.8, ease: 'power3.out' }, '+=0.5')
      .to('.cinematic-quote', { opacity: 1, y: 0, duration: 1, ease: 'power3.out' }, '+=0.3')
      .to('.quote-author', { opacity: 1, y: 0, duration: 0.8, ease: 'power3.out' }, '+=0.2')
      .to('.stats-title', { opacity: 1, y: 0, duration: 1, ease: 'power3.out' }, '+=0.5')
      .to('.challenge-title', { opacity: 1, y: 0, duration: 0.8, ease: 'power3.out' }, '+=1');

    // Floating book animation
    gsap.to('.floating-book', {
        rotationY: -5,
        rotationX: 10,
        y: -5,
        duration: 4,
        repeat: -1,
        yoyo: true,
        ease: 'sine.inOut'
    });

    // Book glow animation
    gsap.to('.book-glow', {
        scale: 1.1,
        opacity: 0.6,
        duration: 3,
        repeat: -1,
        yoyo: true,
        ease: 'sine.inOut'
    });

    // Logo glow animation
    gsap.to('.logo-icon', {
        textShadow: '0 0 20px rgba(59, 130, 246, 0.8)',
        duration: 2,
        repeat: -1,
        yoyo: true,
        ease: 'sine.inOut'
    });

    // Scroll indicator animation
    gsap.to('.scroll-indicator', {
        y: 10,
        duration: 1.5,
        repeat: -1,
        yoyo: true,
        ease: 'sine.inOut'
    });

    // Clients carousel setup
    gsap.to('.clients-track', {
        x: '-50%',
        duration: 30,
        repeat: -1,
        ease: 'none'
    });

    // Advanced stat card interactions
    document.querySelectorAll('.stat-card').forEach(card => {
        card.addEventListener('mouseenter', () => {
            gsap.to(card, {
                y: -10,
                scale: 1.03,
                boxShadow: '0 25px 50px rgba(59, 130, 246, 0.25)',
                duration: 0.4,
                ease: 'power3.out'
            });
            
            gsap.to(card.querySelector('.stat-visual img'), {
                scale: 1.1,
                rotation: 5,
                duration: 0.4,
                ease: 'back.out(1.7)'
            });
        });
        
        card.addEventListener('mouseleave', () => {
            gsap.to(card, {
                y: 0,
                scale: 1,
                boxShadow: '0 10px 15px -3px rgba(0, 0, 0, 0.1)',
                duration: 0.4,
                ease: 'power3.out'
            });
            
            gsap.to(card.querySelector('.stat-visual img'), {
                scale: 1,
                rotation: 0,
                duration: 0.4,
                ease: 'power2.out'
            });
        });
    });

    // Contact items hover animation
    document.querySelectorAll('.contact-item').forEach(item => {
        item.addEventListener('mouseenter', () => {
            gsap.to(item, {
                y: -8,
                scale: 1.02,
                boxShadow: '0 20px 40px rgba(59, 130, 246, 0.2)',
                duration: 0.3,
                ease: 'power2.out'
            });
        });
        
        item.addEventListener('mouseleave', () => {
            gsap.to(item, {
                y: 0,
                scale: 1,
                boxShadow: 'none',
                duration: 0.3,
                ease: 'power2.out'
            });
        });
    });
}

// Scroll progress indicator
function createScrollProgress() {
    const progressBar = document.createElement('div');
    progressBar.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 0%;
        height: 3px;
        background: linear-gradient(90deg, #3b82f6, #60a5fa);
        z-index: 10000;
        transition: width 0.1s ease;
    `;
    document.body.appendChild(progressBar);
    
    window.addEventListener('scroll', () => {
        const scrolled = (window.scrollY / (document.documentElement.scrollHeight - window.innerHeight)) * 100;
        progressBar.style.width = scrolled + '%';
    });
}

// Header scroll effects
window.addEventListener('scroll', () => {
    const header = document.querySelector('.header');
    const scrolled = window.scrollY > 50;
    
    if (scrolled) {
        header.style.background = 'rgba(255, 255, 255, 0.95)';
        header.style.backdropFilter = 'blur(20px) saturate(180%)';
        header.style.borderBottom = '1px solid rgba(59, 130, 246, 0.1)';
    } else {
        header.style.background = 'rgba(255, 255, 255, 0.85)';
        header.style.backdropFilter = 'blur(20px) saturate(180%)';
        header.style.borderBottom = '1px solid rgba(255, 255, 255, 0.2)';
    }
});

// Initialize everything
createScrollProgress();

// Performance optimization
let ticking = false;

function updateAnimations() {
    // Update any frame-based animations here
    ticking = false;
}

window.addEventListener('scroll', () => {
    if (!ticking) {
        requestAnimationFrame(updateAnimations);
        ticking = true;
    }
});

// Resize handler
window.addEventListener('resize', debounce(() => {
    ScrollTrigger.refresh();
}, 250));

// Utility functions
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Advanced error handling
window.addEventListener('error', (e) => {
    console.error('Animation error:', e);
});

// Accessibility support
const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
if (prefersReducedMotion.matches) {
    gsap.globalTimeline.timeScale(0.1);
}

// Easter egg - Konami code
let konamiCode = [];
const correctCode = [38, 38, 40, 40, 37, 39, 37, 39, 66, 65];

document.addEventListener('keydown', (e) => {
    konamiCode.push(e.keyCode);
    if (konamiCode.length > correctCode.length) {
        konamiCode.shift();
    }
    
    if (JSON.stringify(konamiCode) === JSON.stringify(correctCode)) {
        // Trigger special animation
        gsap.to('body', {
            filter: 'hue-rotate(360deg)',
            duration: 2,
            repeat: 3,
            yoyo: true
        });
        
        gsap.to('.logo-icon', {
            rotation: 720,
            scale: 1.5,
            duration: 2,
            ease: 'power2.out'
        });
        
        console.log('🎉 Easter egg activated! Claude Code is incredible!');
    }
});

console.log('🎯 Pro tip: Try the Konami code (↑↑↓↓←→←→BA) for a surprise!');