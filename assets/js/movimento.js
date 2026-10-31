/*
 * Entrada ao rolar da LP (LP v2, IFI-65 / IFI-66).
 *
 * Marca com .visivel cada elemento [data-anima] quando ele entra na tela; o
 * CSS em estilos.css (seção 07) faz o resto. Itens que entram juntos (uma
 * linha de cards no computador) ganham um atraso escalonado; itens empilhados
 * no celular entram um de cada vez, sem esperar os anteriores.
 *
 * Sem este script, ou num navegador sem IntersectionObserver, a classe
 * .movimento-ativo não é aplicada e todo o conteúdo fica visível (RF-01).
 */
(function () {
  "use strict";

  var raiz = document.documentElement;

  if (!("IntersectionObserver" in window)) {
    return;
  }

  var alvos = Array.prototype.slice.call(document.querySelectorAll("[data-anima]"));
  var alturaTela = window.innerHeight || raiz.clientHeight;

  // Mede antes de ativar o movimento: o que já está na tela não anima (RF-03).
  var jaVisiveis = alvos.filter(function (alvo) {
    var caixa = alvo.getBoundingClientRect();
    return caixa.top < alturaTela && caixa.bottom > 0;
  });

  jaVisiveis.forEach(function (alvo) {
    alvo.classList.add("visivel");
  });
  raiz.classList.add("movimento-ativo");

  function intervalo(alvo) {
    var valor = window.getComputedStyle(alvo).getPropertyValue("--motion-escalonamento");
    var numero = parseFloat(valor);
    if (isNaN(numero)) {
      return 0;
    }
    return valor.indexOf("ms") === -1 ? numero * 1000 : numero;
  }

  var observador = new IntersectionObserver(
    function (entradas) {
      var ordem = 0;
      entradas.forEach(function (entrada) {
        if (!entrada.isIntersecting) {
          return;
        }
        var alvo = entrada.target;
        alvo.style.setProperty("--atraso", ordem * intervalo(alvo) + "ms");
        alvo.classList.add("visivel");
        observador.unobserve(alvo);
        ordem += 1;
      });
    },
    { rootMargin: "0px 0px -8% 0px", threshold: 0.12 }
  );

  alvos.forEach(function (alvo) {
    if (jaVisiveis.indexOf(alvo) === -1) {
      observador.observe(alvo);
    }
  });
})();
