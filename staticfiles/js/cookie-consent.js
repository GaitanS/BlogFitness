class CookieConsent {
    constructor() {
        this.cookieModal = new bootstrap.Modal(document.getElementById('cookieModal'));
        this.bindEvents();
        this.checkCookieConsent();
    }

    bindEvents() {
        document.getElementById('acceptAllCookies').addEventListener('click', () => this.acceptAll());
        document.getElementById('acceptSelectedCookies').addEventListener('click', () => this.acceptSelected());
        document.getElementById('cookieSettingsBtn').addEventListener('click', () => this.showSettings());
    }

    checkCookieConsent() {
        if (!this.getCookie('cookieConsent')) {
            this.cookieModal.show();
        }
    }

    acceptAll() {
        const cookieOptions = {
            necessary: true,
            analytics: true,
            marketing: true
        };
        this.setCookieConsent(cookieOptions);
        this.cookieModal.hide();
    }

    acceptSelected() {
        const cookieOptions = {
            necessary: true,
            analytics: document.getElementById('analyticsCookies').checked,
            marketing: document.getElementById('marketingCookies').checked
        };
        this.setCookieConsent(cookieOptions);
        this.cookieModal.hide();
    }

    showSettings() {
        const currentConsent = this.getCookie('cookieConsent');
        if (currentConsent) {
            const options = JSON.parse(currentConsent);
            document.getElementById('analyticsCookies').checked = options.analytics;
            document.getElementById('marketingCookies').checked = options.marketing;
        }
        this.cookieModal.show();
    }

    setCookieConsent(options) {
        // Set cookie for 1 year
        const expires = new Date(Date.now() + 365 * 24 * 60 * 60 * 1000).toUTCString();
        document.cookie = `cookieConsent=${JSON.stringify(options)}; expires=${expires}; path=/; SameSite=Strict`;
        
        // Apply cookie settings
        if (options.analytics) {
            this.enableAnalytics();
        }
        if (options.marketing) {
            this.enableMarketing();
        }
    }

    getCookie(name) {
        const value = `; ${document.cookie}`;
        const parts = value.split(`; ${name}=`);
        if (parts.length === 2) return parts.pop().split(';').shift();
    }

    enableAnalytics() {
        // Implementează logica pentru activarea Google Analytics
        console.log('Analytics cookies enabled');
    }

    enableMarketing() {
        // Activează AdSense
        if (window.adsbygoogle === undefined) {
            // Încarcă scriptul AdSense
            const script = document.createElement('script');
            script.src = 'https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-5227061222218296';
            script.async = true;
            script.crossOrigin = 'anonymous';
            document.head.appendChild(script);
        }

        // Activează toate reclamele existente
        document.querySelectorAll('.adsbygoogle').forEach((ad) => {
            try {
                (adsbygoogle = window.adsbygoogle || []).push({});
            } catch (e) {
                console.error('Error loading AdSense ad:', e);
            }
        });

        // Afișează containerele de reclame
        document.querySelectorAll('.adsense-container').forEach((container) => {
            container.style.display = 'block';
        });
    }

    disableMarketing() {
        // Ascunde toate containerele de reclame
        document.querySelectorAll('.adsense-container').forEach((container) => {
            container.style.display = 'none';
        });
    }

    applySettings() {
        const consent = this.getCookie('cookieConsent');
        if (consent) {
            const options = JSON.parse(consent);
            if (options.marketing) {
                this.enableMarketing();
            } else {
                this.disableMarketing();
            }
        }
    }
}

// Inițializează când DOM-ul este încărcat
document.addEventListener('DOMContentLoaded', () => {
    const cookieConsent = new CookieConsent();
    cookieConsent.applySettings();
});
