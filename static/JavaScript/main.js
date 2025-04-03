document.addEventListener("DOMContentLoaded", function () {
    const menuToggle = document.getElementById("menuToggle");
    const mobileMenu = document.getElementById("mobileMenu");

    menuToggle.addEventListener("click", () => {
        mobileMenu.classList.toggle("hidden");
    });

    // Close menu when clicking outside
    document.addEventListener("click", (event) => {
        if (!menuToggle.contains(event.target) && !mobileMenu.contains(event.target)) {
            mobileMenu.classList.add("hidden");
        }
    });
});

let currentIndex = 0;
const carousel = document.getElementById("carousel");
const slides = carousel ? carousel.children : [];
const dots = document.querySelectorAll(".dot");

function goToSlide(index) {
  if (!carousel || slides.length === 0) return; // Prevent errors if elements are missing
  
  currentIndex = index;
  const offset = -index * 100; // Move slide by 100% per index
  carousel.style.transition = "transform 0.5s ease-in-out";
  carousel.style.transform = `translateX(${offset}%)`;
  updateDots();
}

function updateDots() {
  dots.forEach((dot, index) => {
    dot.classList.toggle("bg-yellow-500", index === currentIndex);
    dot.classList.toggle("w-[30px]", index === currentIndex);
    dot.classList.toggle("bg-gray", index !== currentIndex);
  });
}

// Auto-Slide Functionality
const autoSlide = setInterval(() => {
  currentIndex = (currentIndex + 1) % slides.length;
  goToSlide(currentIndex);
}, 5000); // Change every 5 seconds

// Allow manual navigation through dots
dots.forEach((dot, index) => {
  dot.addEventListener("click", () => {
    clearInterval(autoSlide); // Stop auto-slide when user interacts
    goToSlide(index);
  });
});

// Initialize
if (carousel) updateDots();


function toggleHover(isHovered, cardName) {
    const hoverContent = document.getElementById(`hover-content-${cardName}`);
    const title = document.getElementById(`title-${cardName}`);
  
    if (isHovered) {
      hoverContent.classList.remove("invisible");
      hoverContent.classList.add("opacity-100");
      title.classList.add("opacity-0");
    } else {
      hoverContent.classList.remove("opacity-100");
      hoverContent.classList.add("invisible");
      title.classList.remove("opacity-0");
      title.classList.add("opacity-100");
    }
  }
  