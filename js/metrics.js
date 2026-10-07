/* ==========================================================
   Medidas compartidas y posición de scroll.
   - Las medidas (alto de pantalla, de la portada, de la página) se
     guardan y solo se recalculan al cambiar el tamaño: leerlas en
     cada fotograma obliga al navegador a recalcular la maquetación.
   - KF.y() es la posición que siguen las animaciones. Durante el
     recorrido automático es un número continuo (con decimales), así
     los discos se mueven suaves aunque la página avance de píxel en píxel.
   ========================================================== */
(function () {
  "use strict";
  const KF = {
    vh: window.innerHeight,
    vw: window.innerWidth,
    heroH: 0,
    docH: 0,
    autoY: null,
    y() { return KF.autoY != null ? KF.autoY : window.scrollY; },
    listeners: [],
    onMeasure(fn) { KF.listeners.push(fn); },
    measure() {
      KF.vh = window.innerHeight;
      KF.vw = window.innerWidth;
      const hero = document.getElementById("inicio");
      KF.heroH = hero ? hero.offsetHeight : KF.vh;
      KF.docH = document.documentElement.scrollHeight;
      KF.listeners.forEach((fn) => fn(KF));
    }
  };
  /* Medidor de fluidez: cada segundo devuelve qué parte de los fotogramas fue
     lenta, comparando con el ritmo real de la pantalla (60, 90, 120 Hz… o 30 en
     un móvil en ahorro de energía, que no debe contar como «lento»). */
  KF.meter = function () {
    let win = 0, raws = [];
    return function (raw) {
      if (!(raw > 0) || raw >= 1) return null;      // parones de pestaña o carga: no cuentan
      win += raw; raws.push(raw);
      if (win < 1) return null;
      const sorted = raws.slice().sort((a, b) => a - b);
      const beat = sorted[Math.floor(sorted.length * 0.1)];
      const limit = Math.max(beat * 1.5, 0.021);
      const share = raws.filter((r) => r > limit).length / raws.length;
      win = 0; raws = [];
      return share;
    };
  };
  window.KF = KF;
  let queued = false;
  const later = () => { if (queued) return; queued = true; requestAnimationFrame(() => { queued = false; KF.measure(); }); };
  window.addEventListener("resize", later);
  window.addEventListener("load", later);
  if (window.ResizeObserver) new ResizeObserver(later).observe(document.documentElement);
  KF.measure();   // los scripts van al final de la página: ya está todo
})();
