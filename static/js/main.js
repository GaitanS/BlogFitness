/**
 * Fitness Blog - Main JavaScript
 */

document.addEventListener('DOMContentLoaded', function() {
    // Newsletter form submission
    const newsletterForm = document.getElementById('newsletter-form');
    if (newsletterForm) {
        newsletterForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const email = document.getElementById('email').value;
            const messageContainer = document.getElementById('newsletter-message');
            
            // Clear previous messages
            messageContainer.innerHTML = '';
            messageContainer.className = '';
            
            // Send AJAX request
            fetch('/subscribe/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: `email=${encodeURIComponent(email)}`
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    messageContainer.className = 'text-success';
                    messageContainer.innerText = data.message;
                    newsletterForm.reset();
                } else {
                    messageContainer.className = 'text-danger';
                    messageContainer.innerText = data.message;
                }
            })
            .catch(error => {
                messageContainer.className = 'text-danger';
                messageContainer.innerText = 'A apărut o eroare. Te rugăm să încerci din nou.';
                console.error('Error:', error);
            });
        });
    }
    
    // Hero Slider
    let currentSlide = 0;
    const heroSlides = [
        {
            title: 'Nutriție pentru performanță',
            subtitle: 'Alimentează-ți corpul pentru rezultate optime',
            backgroundImage: '/static/images/hero-bg.webp'
        },
        {
            title: 'Antrenamente eficiente',
            subtitle: 'Tehnici dovedite pentru rezultate maxime',
            backgroundImage: '/static/images/hero-bg-2.webp'
        },
        {
            title: 'Lifestyle sănătos',
            subtitle: 'Obiceiuri care îți transformă viața',
            backgroundImage: '/static/images/hero-bg-3.webp'
        }
    ];
    
    const heroSection = document.querySelector('.hero-section');
    const indicators = document.querySelectorAll('.hero-indicators span');
    const heroTitle = document.querySelector('.hero-title');
    const heroSubtitle = document.querySelector('.hero-subtitle');
    
    if (heroSection && indicators.length > 0) {
        // Set up indicators click events
        indicators.forEach((indicator, index) => {
            indicator.addEventListener('click', () => {
                changeSlide(index);
            });
        });
        
        // Auto change slides every 5 seconds
        setInterval(() => {
            currentSlide = (currentSlide + 1) % heroSlides.length;
            changeSlide(currentSlide);
        }, 5000);
        
        function changeSlide(index) {
            // Update current slide
            currentSlide = index;
            
            // Update indicators
            indicators.forEach((indicator, i) => {
                if (i === index) {
                    indicator.classList.add('active');
                } else {
                    indicator.classList.remove('active');
                }
            });
            
            // Update content with animation
            heroTitle.style.opacity = 0;
            heroSubtitle.style.opacity = 0;
            
            setTimeout(() => {
                // Update hero content
                heroTitle.innerText = heroSlides[index].title;
                heroSubtitle.innerText = heroSlides[index].subtitle;
                
                // Fade in the new content
                heroTitle.style.opacity = 1;
                heroSubtitle.style.opacity = 1;
            }, 300);
            
            // Update background with fade effect
            heroSection.style.backgroundImage = `url(${heroSlides[index].backgroundImage})`;
        }
    }
});
