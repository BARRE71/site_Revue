// JavaScript pour la page d'accueil RevueMaroc

document.addEventListener('DOMContentLoaded', function() {
    
    // Gestion de la bannière d'actualités importantes
    const breakingNewsBanner = document.querySelector('.breaking-news-banner');
    const breakingNewsText = document.querySelector('.breaking-news-text span');
    
    if (breakingNewsBanner && breakingNewsText) {
        // Messages d'actualités à faire défiler
        const newsMessages = [
            "RevueMaroc : Votre source d'information privilégiée sur le développement du Maroc",
            "Découvrez nos dernières analyses sur l'économie marocaine",
            "Nouveaux articles disponibles sur la politique et la société",
            "Abonnez-vous à notre newsletter pour rester informé"
        ];
        
        let currentMessageIndex = 0;
        
        // Fonction pour changer le message
        function changeNewsMessage() {
            breakingNewsText.style.opacity = '0';
            
            setTimeout(() => {
                currentMessageIndex = (currentMessageIndex + 1) % newsMessages.length;
                breakingNewsText.textContent = newsMessages[currentMessageIndex];
                breakingNewsText.style.opacity = '1';
            }, 500);
        }
        
        // Changer le message toutes les 5 secondes
        setInterval(changeNewsMessage, 5000);
        
        // Ajouter une transition CSS
        breakingNewsText.style.transition = 'opacity 0.5s ease-in-out';
    }
    
    // Animation des statistiques au scroll
    const statsCards = document.querySelectorAll('.stats-card');
    
    if (statsCards.length > 0) {
        const observerOptions = {
            threshold: 0.5,
            rootMargin: '0px 0px -50px 0px'
        };
        
        const statsObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.style.opacity = '1';
                    entry.target.style.transform = 'translateY(0)';
                }
            });
        }, observerOptions);
        
        statsCards.forEach(card => {
            card.style.opacity = '0';
            card.style.transform = 'translateY(30px)';
            card.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
            statsObserver.observe(card);
        });
    }
    
    // Effet de parallaxe léger pour l'image principale
    const mainArticleImage = document.querySelector('.main-article-image img');
    
    if (mainArticleImage) {
        window.addEventListener('scroll', () => {
            const scrolled = window.pageYOffset;
            const rate = scrolled * -0.3;
            mainArticleImage.style.transform = `translateY(${rate}px)`;
        });
    }
    
    // Animation des cartes d'articles au survol
    const articleCards = document.querySelectorAll('.article-card, .category-card');
    
    articleCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-8px)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });
    
    // Gestion des contrôles de carousel (pour future implémentation)
    const heroControls = document.querySelectorAll('.hero-controls .btn');
    
    heroControls.forEach(control => {
        control.addEventListener('click', function(e) {
            e.preventDefault();
            // Ici on pourrait implémenter la logique de carousel
            console.log('Contrôle de carousel cliqué:', this.querySelector('i').className);
        });
    });
    
    // Amélioration de l'accessibilité
    const allButtons = document.querySelectorAll('button, .btn');
    
    allButtons.forEach(button => {
        button.addEventListener('keydown', function(e) {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                this.click();
            }
        });
    });
    
    // Lazy loading des images (pour améliorer les performances)
    const images = document.querySelectorAll('img[data-src]');
    
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src;
                    img.classList.remove('lazy');
                    imageObserver.unobserve(img);
                }
            });
        });
        
        images.forEach(img => imageObserver.observe(img));
    }
    
    // Gestion du responsive pour les contrôles de bannière
    function handleResponsiveControls() {
        const breakingNewsContent = document.querySelector('.breaking-news-content');
        
        if (window.innerWidth <= 768) {
            breakingNewsContent.classList.add('mobile-layout');
        } else {
            breakingNewsContent.classList.remove('mobile-layout');
        }
    }
    
    // Appeler au chargement et au redimensionnement
    handleResponsiveControls();
    window.addEventListener('resize', handleResponsiveControls);
    
    // Ajout d'un indicateur de chargement
    const loadingIndicator = document.createElement('div');
    loadingIndicator.className = 'loading-indicator';
    loadingIndicator.innerHTML = '<div class="spinner"></div>';
    loadingIndicator.style.display = 'none';
    
    document.body.appendChild(loadingIndicator);
    
    // Fonction pour afficher/masquer l'indicateur de chargement
    window.showLoading = function() {
        loadingIndicator.style.display = 'flex';
    };
    
    window.hideLoading = function() {
        loadingIndicator.style.display = 'none';
    };
    
    // Gestion des erreurs d'images
    const allImages = document.querySelectorAll('img');
    
    allImages.forEach(img => {
        img.addEventListener('error', function() {
            this.style.display = 'none';
            const placeholder = document.createElement('div');
            placeholder.className = 'image-placeholder';
            placeholder.innerHTML = '<i class="fas fa-image"></i>';
            placeholder.style.cssText = `
                width: 100%;
                height: 100%;
                display: flex;
                align-items: center;
                justify-content: center;
                background: #f8f9fa;
                color: #6c757d;
                font-size: 2rem;
            `;
            this.parentNode.appendChild(placeholder);
        });
    });
    
    // Amélioration de la navigation au clavier
    document.addEventListener('keydown', function(e) {
        // Navigation avec les flèches
        if (e.key === 'ArrowRight') {
            const nextButton = document.querySelector('.hero-controls .btn:last-child');
            if (nextButton) nextButton.focus();
        }
        if (e.key === 'ArrowLeft') {
            const prevButton = document.querySelector('.hero-controls .btn:first-child');
            if (prevButton) prevButton.focus();
        }
    });
    
    console.log('Page d\'accueil RevueMaroc initialisée avec succès !');
});
