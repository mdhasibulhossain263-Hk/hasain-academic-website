/* ==========================================================================
   Md Hasibul Hossain — Academic Website
   assets/js/main.js
   --------------------------------------------------------------------------
   Plain JavaScript, no libraries, no build step.
   Handles: theme toggle, mobile navigation, sticky-header state,
            scroll reveal, back-to-top button, footer year.
   Every browser-storage call is wrapped in try/catch so the site still
   works in private windows or when cookies/site data are blocked.
   ========================================================================== */

(function () {
  "use strict";

  var STORAGE_KEY = "mhh-theme";

  /* ----------------------------------------------------------------------
     THEME  (light / dark)
     The inline script in each page's <head> applies the saved theme before
     first paint to avoid a flash. This section only wires up the button.
     ---------------------------------------------------------------------- */

  function readStoredTheme() {
    try { return window.localStorage.getItem(STORAGE_KEY); }
    catch (e) { return null; }
  }

  function storeTheme(value) {
    try { window.localStorage.setItem(STORAGE_KEY, value); }
    catch (e) { /* storage unavailable — theme simply won't persist */ }
  }

  function currentTheme() {
    var explicit = document.documentElement.getAttribute("data-theme");
    if (explicit) return explicit;
    return window.matchMedia &&
           window.matchMedia("(prefers-color-scheme: dark)").matches
             ? "dark" : "light";
  }

  function initTheme() {
    var button = document.querySelector("[data-theme-toggle]");
    if (!button) return;

    function syncLabel() {
      var next = currentTheme() === "dark" ? "light" : "dark";
      button.setAttribute("aria-label", "Switch to " + next + " appearance");
      button.setAttribute("title", "Switch to " + next + " appearance");
    }

    button.addEventListener("click", function () {
      var next = currentTheme() === "dark" ? "light" : "dark";
      document.documentElement.setAttribute("data-theme", next);
      storeTheme(next);
      syncLabel();
    });

    syncLabel();
  }

  /* ----------------------------------------------------------------------
     MOBILE NAVIGATION
     ---------------------------------------------------------------------- */

  function initNav() {
    var toggle = document.querySelector("[data-nav-toggle]");
    var menu   = document.getElementById("primary-navigation");
    if (!toggle || !menu) return;

    function close() {
      menu.classList.remove("is-open");
      toggle.setAttribute("aria-expanded", "false");
    }

    toggle.addEventListener("click", function () {
      var open = menu.classList.toggle("is-open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
    });

    // Close after choosing a destination, or on Escape.
    menu.addEventListener("click", function (event) {
      if (event.target.closest("a")) close();
    });

    document.addEventListener("keydown", function (event) {
      if (event.key === "Escape") close();
    });

    window.addEventListener("resize", function () {
      if (window.innerWidth > 900) close();
    });
  }

  /* ----------------------------------------------------------------------
     STICKY HEADER SHADOW + BACK-TO-TOP VISIBILITY
     ---------------------------------------------------------------------- */

  function initScrollState() {
    var header = document.querySelector(".site-header");
    var toTop  = document.querySelector("[data-to-top]");
    var ticking = false;

    function update() {
      var y = window.scrollY || window.pageYOffset;
      if (header) header.classList.toggle("is-scrolled", y > 8);
      if (toTop)  toTop.classList.toggle("is-visible", y > 600);
      ticking = false;
    }

    window.addEventListener("scroll", function () {
      if (!ticking) {
        window.requestAnimationFrame(update);
        ticking = true;
      }
    }, { passive: true });

    update();

    if (toTop) {
      toTop.addEventListener("click", function () {
        var reduce = window.matchMedia &&
                     window.matchMedia("(prefers-reduced-motion: reduce)").matches;
        window.scrollTo({ top: 0, behavior: reduce ? "auto" : "smooth" });
      });
    }
  }

  /* ----------------------------------------------------------------------
     SCROLL REVEAL  (subtle; skipped entirely if the visitor prefers
     reduced motion, or if IntersectionObserver is unavailable)
     ---------------------------------------------------------------------- */

  function initReveal() {
    var items = document.querySelectorAll(".reveal");
    if (!items.length) return;

    var reduce = window.matchMedia &&
                 window.matchMedia("(prefers-reduced-motion: reduce)").matches;

    if (reduce || !("IntersectionObserver" in window)) {
      for (var i = 0; i < items.length; i++) items[i].classList.add("is-visible");
      return;
    }

    // threshold must stay 0: a section taller than the viewport can never
    // reach a percentage threshold, which would leave it invisible forever
    // on small screens. rootMargin alone gives the small delay we want.
    var observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add("is-visible");
          observer.unobserve(entry.target);
        }
      });
    }, { rootMargin: "0px 0px -40px 0px", threshold: 0 });

    items.forEach(function (item) { observer.observe(item); });
  }

  /* ----------------------------------------------------------------------
     LIGHTBOX  (portfolio images)
     Opens any image carrying data-full. Keyboard accessible, restores focus
     on close, and does nothing at all if the markup is not on the page.
     ---------------------------------------------------------------------- */

  function initLightbox() {
    var box = document.querySelector("[data-lightbox]");
    if (!box) return;

    var img = box.querySelector("[data-lightbox-img]");
    var cap = box.querySelector("[data-lightbox-cap]");
    var closeBtn = box.querySelector("[data-lightbox-close]");
    var opener = null;

    var shots = document.querySelectorAll("img[data-full]");
    if (!shots.length) return;

    function open(source) {
      opener = source;
      img.src = source.getAttribute("data-full");
      img.alt = source.getAttribute("alt") || "";
      var text = source.getAttribute("data-cap") || "";
      cap.textContent = text;
      cap.style.display = text ? "" : "none";
      box.classList.add("is-open");
      box.setAttribute("aria-hidden", "false");
      document.body.style.overflow = "hidden";
      closeBtn.focus();
    }

    function close() {
      box.classList.remove("is-open");
      box.setAttribute("aria-hidden", "true");
      document.body.style.overflow = "";
      img.src = "";
      if (opener) { opener.focus(); opener = null; }
    }

    for (var i = 0; i < shots.length; i++) {
      (function (el) {
        el.setAttribute("tabindex", "0");
        el.setAttribute("role", "button");
        el.addEventListener("click", function () { open(el); });
        el.addEventListener("keydown", function (e) {
          if (e.key === "Enter" || e.key === " ") { e.preventDefault(); open(el); }
        });
      })(shots[i]);
    }

    box.addEventListener("click", close);
    closeBtn.addEventListener("click", function (e) { e.stopPropagation(); close(); });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && box.classList.contains("is-open")) close();
    });
  }

  /* ----------------------------------------------------------------------
     FOOTER YEAR
     ---------------------------------------------------------------------- */

  function initYear() {
    var nodes = document.querySelectorAll("[data-year]");
    var year = String(new Date().getFullYear());
    for (var i = 0; i < nodes.length; i++) nodes[i].textContent = year;
  }

  /* ---------------------------------------------------------------------- */

  function init() {
    initTheme();
    initNav();
    initScrollState();
    initReveal();
    initLightbox();
    initYear();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
