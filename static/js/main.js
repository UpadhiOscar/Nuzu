"use strict";

/* =========================================
   NUZU — MOBILE NAVIGATION
   ========================================= */

const menuToggle = document.getElementById("menu-toggle");
const mainNav = document.getElementById("main-nav");

if (menuToggle && mainNav) {
    menuToggle.addEventListener("click", () => {
        const isOpen = mainNav.classList.toggle("is-open");

        menuToggle.setAttribute("aria-expanded", String(isOpen));
        menuToggle.setAttribute(
            "aria-label",
            isOpen ? "Close navigation menu" : "Open navigation menu"
        );
    });

    mainNav.querySelectorAll("a").forEach((link) => {
        link.addEventListener("click", () => {
            mainNav.classList.remove("is-open");
            menuToggle.setAttribute("aria-expanded", "false");
            menuToggle.setAttribute("aria-label", "Open navigation menu");
        });
    });
}

/* =========================================
   NUZU — IMAGE FALLBACKS
   ========================================= */

document.querySelectorAll(".musician-photo img").forEach((image) => {
    image.addEventListener("error", () => {
        image.style.display = "none";
    });
});

/*
  The hero image has an inline fallback in home.html.
  The musician-card fallbacks use their CSS background colors.
*/

/* =========================================
   NUZU — PREVENT PAST EVENT DATES
   ========================================= */

const dateInput = document.querySelector('input[name="date"]');

if (dateInput) {
    const today = new Date();
    const localToday = [
        today.getFullYear(),
        String(today.getMonth() + 1).padStart(2, "0"),
        String(today.getDate()).padStart(2, "0")
    ].join("-");

    dateInput.min = localToday;
}