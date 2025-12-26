/**
 * Interactive Particle Network Animation
 * Spawns a constellation of connected particles that react to mouse movement.
 * Optimized for performance: Disabled on mobile/reduced motion.
 */

const canvas = document.getElementById('particles-canvas');
const ctx = canvas ? canvas.getContext('2d') : null;

if (canvas && ctx) {
    let particlesArray;
    let animationId;

    // Configuration
    const config = {
        particleCount: 60,
        connectionDistance: 150,
        mouseRadius: 150,
        baseColor: 'rgba(56, 189, 248, 0.5)', // Sky blue
        lineColor: 'rgba(56, 189, 248, 0.15)',
        particleSpeed: 0.3 // Very slow, subtle
    };

    // Handle Resize
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;

    window.addEventListener('resize', () => {
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
        init();
    });

    // Mouse Interaction
    const mouse = {
        x: null,
        y: null,
        radius: config.mouseRadius
    };

    window.addEventListener('mousemove', (event) => {
        mouse.x = event.x;
        mouse.y = event.y;
    });

    window.addEventListener('mouseout', () => {
        mouse.x = undefined;
        mouse.y = undefined;
    });

    // Particle Class
    class Particle {
        constructor() {
            this.x = Math.random() * (canvas.width - 20) + 10; // Padding
            this.y = Math.random() * (canvas.height - 20) + 10;
            this.directionX = (Math.random() * 2) - 1; // -1 to 1
            this.directionY = (Math.random() * 2) - 1;
            this.size = Math.random() * 2 + 1; // 1 to 3px
            this.speedX = this.directionX * config.particleSpeed;
            this.speedY = this.directionY * config.particleSpeed;
        }

        update() {
            // Boundary Check
            if (this.x > canvas.width || this.x < 0) {
                this.directionX = -this.directionX;
                this.speedX = this.directionX * config.particleSpeed;
            }
            if (this.y > canvas.height || this.y < 0) {
                this.directionY = -this.directionY;
                this.speedY = this.directionY * config.particleSpeed;
            }

            // Mouse Interaction (Run away or attract - let's do slight attraction)
            let dx = mouse.x - this.x;
            let dy = mouse.y - this.y;
            let distance = Math.sqrt(dx * dx + dy * dy);

            // Move particle
            this.x += this.speedX;
            this.y += this.speedY;
        }

        draw() {
            ctx.beginPath();
            ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2, false);
            ctx.fillStyle = config.baseColor;
            ctx.fill();
        }
    }

    // Init Logic
    function init() {
        particlesArray = [];
        // Reduce count on smaller screens
        const count = window.innerWidth < 768 ? config.particleCount / 2 : config.particleCount;

        for (let i = 0; i < count; i++) {
            particlesArray.push(new Particle());
        }
    }

    // Animation Loop
    function animate() {
        requestAnimationFrame(animate);
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        for (let i = 0; i < particlesArray.length; i++) {
            particlesArray[i].update();
            particlesArray[i].draw();
        }
        connect();
    }

    // Draw lines between nearby particles
    function connect() {
        for (let a = 0; a < particlesArray.length; a++) {
            for (let b = a; b < particlesArray.length; b++) {
                let distance = ((particlesArray[a].x - particlesArray[b].x) * (particlesArray[a].x - particlesArray[b].x)) +
                    ((particlesArray[a].y - particlesArray[b].y) * (particlesArray[a].y - particlesArray[b].y));

                if (distance < (config.connectionDistance * config.connectionDistance)) {
                    let opacity = 1 - (distance / (config.connectionDistance * config.connectionDistance));
                    ctx.strokeStyle = `rgba(56, 189, 248, ${opacity * 0.15})`; // Low opacity lines
                    ctx.lineWidth = 1;
                    ctx.beginPath();
                    ctx.moveTo(particlesArray[a].x, particlesArray[a].y);
                    ctx.lineTo(particlesArray[b].x, particlesArray[b].y);
                    ctx.stroke();
                }
            }
        }
    }

    // Start only if not reduced motion and not mobile (optimization)
    const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    const isMobile = window.innerWidth < 768;

    if (!prefersReducedMotion && !isMobile) {
        init();
        animate();
    } else {
        console.log('Particles disabled for performance/accessibility');
    }
}
