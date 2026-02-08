import { useEffect, useRef } from 'react';

function createParticle(canvasWidth, canvasHeight) {
  return {
    x: Math.random() * canvasWidth,
    y: Math.random() * canvasHeight,
    size: Math.random() * 3 + 1,
    speedX: (Math.random() - 0.5) * 0.5,
    speedY: (Math.random() - 0.5) * 0.5,
    opacity: Math.random() * 0.5 + 0.2,
    color: Math.random() > 0.5 ? '#F7931A' : '#FFD700',
  };
}

function updateParticle(p, canvasWidth, canvasHeight) {
  p.x += p.speedX;
  p.y += p.speedY;
  if (p.x > canvasWidth) p.x = 0;
  if (p.x < 0) p.x = canvasWidth;
  if (p.y > canvasHeight) p.y = 0;
  if (p.y < 0) p.y = canvasHeight;
}

function drawParticle(ctx, p) {
  ctx.beginPath();
  ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
  ctx.fillStyle = p.color;
  ctx.globalAlpha = p.opacity;
  ctx.fill();
  ctx.globalAlpha = 1;
}

const ParticleBackground = () => {
  const canvasRef = useRef(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    const ctx = canvas.getContext('2d');
    let animationFrameId;
    let particles = [];

    const resizeCanvas = () => {
      canvas.width = window.innerWidth;
      canvas.height = window.innerHeight;
    };

    resizeCanvas();
    window.addEventListener('resize', resizeCanvas);

    const initParticles = () => {
      particles = [];
      const particleCount = Math.floor((canvas.width * canvas.height) / 15000);
      for (let i = 0; i < Math.min(particleCount, 100); i++) {
        particles.push(createParticle(canvas.width, canvas.height));
      }
    };

    initParticles();

    const drawConnections = () => {
      for (let i = 0; i < particles.length; i++) {
        for (let j = i + 1; j < particles.length; j++) {
          const dx = particles[i].x - particles[j].x;
          const dy = particles[i].y - particles[j].y;
          const distance = Math.sqrt(dx * dx + dy * dy);

          if (distance < 150) {
            ctx.beginPath();
            ctx.strokeStyle = '#F7931A';
            ctx.globalAlpha = 0.1 * (1 - distance / 150);
            ctx.lineWidth = 0.5;
            ctx.moveTo(particles[i].x, particles[i].y);
            ctx.lineTo(particles[j].x, particles[j].y);
            ctx.stroke();
            ctx.globalAlpha = 1;
          }
        }
      }
    };

    const animate = () => {
      ctx.clearRect(0, 0, canvas.width, canvas.height);

      particles.forEach(particle => {
        updateParticle(particle, canvas.width, canvas.height);
        drawParticle(ctx, particle);
      });

      drawConnections();

      animationFrameId = requestAnimationFrame(animate);
    };

    animate();

    return () => {
      window.removeEventListener('resize', resizeCanvas);
      cancelAnimationFrame(animationFrameId);
    };
  }, []);

  return (
    <canvas
      ref={canvasRef}
      className="absolute inset-0 pointer-events-none"
      style={{ zIndex: 1 }}
    />
  );
};

export default ParticleBackground;
