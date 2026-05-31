document.addEventListener("DOMContentLoaded", function () {
    
console.log("Secure Smart Home Dashboard Loaded");

// =========================
// Animated Statistics
// =========================

const counters = document.querySelectorAll(".stat-number");

counters.forEach(counter => {

    const text = counter.innerText.trim();

    if (!isNaN(text)) {

        const target = parseInt(text);

        let count = 0;

        const speed = 20;

        const updateCounter = () => {

            if (count < target) {

                count++;

                counter.innerText = count;

                setTimeout(updateCounter, speed);

            }

        };

        updateCounter();

    }

});

// =========================
// Card Hover Animation
// =========================

const cards = document.querySelectorAll(".dashboard-card");

cards.forEach(card => {

    card.addEventListener("mouseenter", () => {

        card.style.transform = "translateY(-5px)";

    });

    card.addEventListener("mouseleave", () => {

        card.style.transform = "translateY(0px)";

    });

});

// =========================
// Notification
// =========================

const alertBox = document.querySelector(".alert-danger");

if (alertBox) {

    console.log("Motion Alert Active");

}
});
