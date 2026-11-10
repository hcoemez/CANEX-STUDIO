/* CANEX Hair Studio – kleine Funktionen ohne Fremdbibliotheken */
(function () {
  "use strict";
  document.documentElement.classList.remove("no-js");

  /* ---------- Navigation: Hintergrund beim Scrollen, mobiles Menü ---------- */
  var nav = document.querySelector(".nav");
  if (nav) {
    var onScroll = function () { nav.classList.toggle("scrolled", window.scrollY > 50); };
    window.addEventListener("scroll", onScroll, { passive: true });
    onScroll();

    var toggle = nav.querySelector(".nav-toggle");
    if (toggle) {
      toggle.addEventListener("click", function () {
        var open = nav.classList.toggle("open");
        toggle.setAttribute("aria-expanded", open ? "true" : "false");
      });
      nav.querySelectorAll(".nav-mobile a").forEach(function (a) {
        a.addEventListener("click", function () {
          nav.classList.remove("open");
          toggle.setAttribute("aria-expanded", "false");
        });
      });
    }
  }

  /* ---------- Einblenden beim Scrollen ---------- */
  var reveals = document.querySelectorAll(".reveal");
  if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { e.target.classList.add("visible"); io.unobserve(e.target); }
      });
    }, { rootMargin: "0px 0px -100px 0px" });
    reveals.forEach(function (el) { io.observe(el); });
  } else {
    reveals.forEach(function (el) { el.classList.add("visible"); });
  }

  /* ---------- Galerie mit Großansicht ---------- */
  var items = Array.prototype.slice.call(document.querySelectorAll(".gallery-item"));
  var lb = document.querySelector(".lightbox");
  if (items.length && lb) {
    var lbImg = lb.querySelector("img");
    var lbCap = lb.querySelector("figcaption");
    var current = 0;
    var lastFocus = null;
    var show = function (i) {
      current = (i + items.length) % items.length;
      var img = items[current].querySelector("img");
      lbImg.src = img.getAttribute("src");
      lbImg.alt = img.alt;
      lbCap.textContent = items[current].getAttribute("data-caption") || "";
    };
    var open = function (i) {
      lastFocus = document.activeElement;
      show(i);
      lb.classList.add("open");
      document.body.style.overflow = "hidden";
      lb.querySelector(".lb-close").focus();
    };
    var close = function () {
      lb.classList.remove("open");
      document.body.style.overflow = "";
      if (lastFocus) lastFocus.focus();
    };
    items.forEach(function (item, i) { item.addEventListener("click", function () { open(i); }); });
    lb.addEventListener("click", function (e) { if (e.target === lb) close(); });
    lb.querySelector(".lb-close").addEventListener("click", close);
    lb.querySelector(".lb-prev").addEventListener("click", function () { show(current - 1); });
    lb.querySelector(".lb-next").addEventListener("click", function () { show(current + 1); });
    document.addEventListener("keydown", function (e) {
      if (!lb.classList.contains("open")) return;
      if (e.key === "Escape") close();
      if (e.key === "ArrowLeft") show(current - 1);
      if (e.key === "ArrowRight") show(current + 1);
    });
  }

  /* ---------- Bewertungen (Wechsel per Pfeil/Punkt) ---------- */
  var reviewBox = document.querySelector("[data-reviews]");
  if (reviewBox) {
    var slides = reviewBox.querySelectorAll(".review");
    var dots = reviewBox.querySelectorAll(".review-dots button");
    var idx = 0;
    var go = function (i) {
      idx = (i + slides.length) % slides.length;
      slides.forEach(function (s, n) { s.hidden = n !== idx; });
      dots.forEach(function (d, n) { d.classList.toggle("active", n === idx); });
    };
    reviewBox.querySelector(".review-prev").addEventListener("click", function () { go(idx - 1); });
    reviewBox.querySelector(".review-next").addEventListener("click", function () { go(idx + 1); });
    dots.forEach(function (d, n) { d.addEventListener("click", function () { go(n); }); });
    go(0);
  }

  /* ---------- Google Maps erst nach Klick laden (DSGVO) ---------- */
  var mapBtn = document.querySelector("[data-load-map]");
  if (mapBtn) {
    mapBtn.addEventListener("click", function () {
      var box = mapBtn.closest(".map");
      var iframe = document.createElement("iframe");
      iframe.src = box.getAttribute("data-map-src");
      iframe.title = "CANEX Standort auf Google Maps";
      iframe.loading = "lazy";
      iframe.referrerPolicy = "no-referrer-when-downgrade";
      iframe.allowFullscreen = true;
      box.innerHTML = "";
      box.appendChild(iframe);
    });
  }

  /* ---------- Schnellkontakt unten rechts ---------- */
  var fab = document.getElementById("fab");
  if (fab) {
    var fabBtn = fab.querySelector(".fab-toggle");
    var setFab = function (open) {
      fab.classList.toggle("open", open);
      fabBtn.setAttribute("aria-expanded", open ? "true" : "false");
      fabBtn.setAttribute("aria-label", open ? "Kontaktmöglichkeiten schließen" : "Kontaktmöglichkeiten öffnen");
    };
    fabBtn.addEventListener("click", function (e) { e.stopPropagation(); setFab(!fab.classList.contains("open")); });
    document.addEventListener("click", function (e) { if (!fab.contains(e.target)) setFab(false); });
    document.addEventListener("keydown", function (e) { if (e.key === "Escape") setFab(false); });
  }

  /* ---------- Aktuelles Jahr im Footer ---------- */
  document.querySelectorAll("[data-year]").forEach(function (el) {
    el.textContent = new Date().getFullYear();
  });
})();
