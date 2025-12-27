document.addEventListener('DOMContentLoaded', () => {
    const slides = document.querySelectorAll('.slide');
    const container = document.querySelector('.deck-container');

    // Inject Progress Bar
    const progressBar = document.createElement('div');
    progressBar.id = 'deck-progress';
    document.body.prepend(progressBar);

    // --- State ---
    let currentSlideIndex = 0;

    // --- 1. Animation Trigger (Intersection Observer) ---
    const observerOptions = {
        root: container,
        threshold: 0.5 // Trigger when 50% visible
    };

    const slideObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                // Add visible class to trigger CSS transitions
                entry.target.classList.add('visible');

                // Update current index based on observation
                const index = Array.from(slides).indexOf(entry.target);
                if (index !== -1) {
                    currentSlideIndex = index;
                    updateProgress();
                    updateURL();
                }
            }
        });
    }, observerOptions);

    slides.forEach(slide => slideObserver.observe(slide));

    // --- 2. Progress Bar Logic ---
    function updateProgress() {
        const progress = ((currentSlideIndex + 1) / slides.length) * 100;
        progressBar.style.width = `${progress}%`;
    }

    // --- 3. Navigation Helpers ---
    function updateURL() {
        // Optional: Update #slide-X in URL without reloading
        history.replaceState(null, null, `#slide-${currentSlideIndex + 1}`);
    }

    window.scrollToSlide = (index) => {
        if (index < 0 || index >= slides.length) return;
        currentSlideIndex = index; // Optimistic update
        slides[index].scrollIntoView({ behavior: 'smooth' });
    };

    window.nextSlide = () => {
        if (currentSlideIndex < slides.length - 1) {
            scrollToSlide(currentSlideIndex + 1);
        }
    };

    window.prevSlide = () => {
        if (currentSlideIndex > 0) {
            scrollToSlide(currentSlideIndex - 1);
        }
    };

    // --- 4. Input Handling (Keyboard) ---
    document.addEventListener('keydown', (e) => {
        // Prevent default scrolling for keys to let our logic handle it smoothly
        if (['ArrowDown', 'ArrowUp', 'PageDown', 'PageUp', 'Space'].includes(e.code)) {
            e.preventDefault();
        }

        if (e.key === 'ArrowDown' || e.key === 'PageDown' || e.code === 'Space') {
            nextSlide();
        } else if (e.key === 'ArrowUp' || e.key === 'PageUp') {
            prevSlide();
        }
    });

    // --- 5. Mobile Swipe Handling ---
    let touchStartY = 0;
    let touchEndY = 0;

    container.addEventListener('touchstart', (e) => {
        touchStartY = e.changedTouches[0].screenY;
    }, { passive: true });

    container.addEventListener('touchend', (e) => {
        touchEndY = e.changedTouches[0].screenY;
        handleSwipe();
    }, { passive: true });

    function handleSwipe() {
        const threshold = 50; // Min distance to be considered a swipe
        const distance = touchStartY - touchEndY;

        if (Math.abs(distance) > threshold) {
            if (distance > 0) {
                // Swiped Up -> Next Slide
                nextSlide();
            } else {
                // Swiped Down -> Prev Slide
                prevSlide();
            }
        }
    }

    // Initial Trigger
    updateProgress();
});
