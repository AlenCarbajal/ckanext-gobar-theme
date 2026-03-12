/**
 * gobar-home.js
 * Counter animation + Organizations carousel + Custom pages nav
 */
document.addEventListener('DOMContentLoaded', function () {

  // ── Counter animation ──
  function animateCounters() {
    var counters = document.querySelectorAll('.gobar-counter-number[data-target]');
    counters.forEach(function (el) {
      var target = parseInt(el.getAttribute('data-target'), 10);
      if (isNaN(target)) return;
      var duration = 1800;
      var start = null;
      function step(timestamp) {
        if (!start) start = timestamp;
        var elapsed = timestamp - start;
        var progress = Math.min(elapsed / duration, 1);
        var eased = 1 - Math.pow(1 - progress, 3);
        var current = Math.floor(eased * target);
        el.textContent = current.toLocaleString('es-AR');
        if (progress < 1) {
          requestAnimationFrame(step);
        } else {
          el.innerHTML = target.toLocaleString('es-AR') + '<span class="plus">+</span>';
        }
      }
      requestAnimationFrame(step);
    });
  }

  var heroSection = document.querySelector('.gobar-counters');
  if (heroSection) {
    if ('IntersectionObserver' in window) {
      var observer = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            animateCounters();
            observer.unobserve(entry.target);
          }
        });
      }, { threshold: 0.3 });
      observer.observe(heroSection);
    } else {
      setTimeout(animateCounters, 500);
    }
  }

  // ── Organizations Carousel ──
  var track = document.querySelector('.gobar-carousel-track');
  var prevBtn = document.querySelector('.gobar-carousel-prev');
  var nextBtn = document.querySelector('.gobar-carousel-next');

  if (track && prevBtn && nextBtn) {
    var scrollAmount = 340; // ~2 cards

    prevBtn.addEventListener('click', function () {
      track.scrollBy({ left: -scrollAmount, behavior: 'smooth' });
    });

    nextBtn.addEventListener('click', function () {
      track.scrollBy({ left: scrollAmount, behavior: 'smooth' });
    });

    // Optional: auto-hide buttons at edges
    function updateButtons() {
      prevBtn.style.opacity = track.scrollLeft <= 10 ? '0.3' : '1';
      nextBtn.style.opacity =
        track.scrollLeft + track.clientWidth >= track.scrollWidth - 10 ? '0.3' : '1';
    }
    track.addEventListener('scroll', updateButtons);
    updateButtons();
  }

  // ── Custom pages nav active highlight ──
  var currentPath = window.location.pathname;
  document.querySelectorAll('.cp-nav-item a').forEach(function (link) {
    if (link.getAttribute('href') === currentPath) {
      link.parentElement.classList.add('active');
    }
  });
});
