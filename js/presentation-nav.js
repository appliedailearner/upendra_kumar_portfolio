document.addEventListener('DOMContentLoaded', () => {
    const slides = document.querySelectorAll('.slide');
    const container = document.querySelector('.deck-container');
    let currentSlideIndex = 0;

    // Find current slide on load (in case of refresh)
    const updateCurrentIndex = () => {
        let minDistance = Infinity;
        slides.forEach((slide, index) => {
            const rect = slide.getBoundingClientRect();
            const distance = Math.abs(rect.top); // Distance from top of viewport
            if (distance < minDistance) {
                minDistance = distance;
                currentSlideIndex = index;
            }
        });
    };

    // Initial check
    updateCurrentIndex();
    container.addEventListener('scroll', () => {
        // debounce or specific check could be added here
        updateCurrentIndex();
    });

    window.scrollToSlide = (index) => {
        if (index < 0 || index >= slides.length) return;
        currentSlideIndex = index;
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

    // Keyboard Navigation
    document.addEventListener('keydown', (e) => {
        if (e.key === 'ArrowDown' || e.key === 'PageDown') {
            e.preventDefault();
            nextSlide();
        } else if (e.key === 'ArrowUp' || e.key === 'PageUp') {
            e.preventDefault();
            prevSlide();
        }
    });
});
