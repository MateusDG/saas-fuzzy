(function () {
  "use strict";

  var output = document.getElementById("apiOutput");
  var statusNode = document.getElementById("apiStatus");
  var tester = document.getElementById("api-tester");
  var clearButton = document.getElementById("clearOutput");

  function setStatus(message, state) {
    statusNode.textContent = message;
    statusNode.className = "status-pill" + (state ? " " + state : "");
  }

  function writeOutput(value) {
    if (typeof value === "string") {
      output.textContent = value;
      return;
    }

    output.textContent = JSON.stringify(value, null, 2);
  }

  function getApiBaseUrl() {
    var input = document.getElementById("apiBaseUrl");
    return input.value.replace(/\/+$/, "");
  }

  function getProductId() {
    return document.getElementById("productId").value.trim();
  }

  function getWidgetId() {
    return document.getElementById("widgetId").value.trim() || "product-page";
  }

  async function parseResponse(response) {
    var text = await response.text();
    var body = text ? JSON.parse(text) : {};

    if (!response.ok) {
      var error = new Error("HTTP " + response.status);
      error.body = body;
      throw error;
    }

    return body;
  }

  async function requestHealth() {
    var response = await fetch(getApiBaseUrl() + "/health");
    return parseResponse(response);
  }

  async function requestRecommendations() {
    var url = new URL(getApiBaseUrl() + "/recommendations");
    var productId = getProductId();
    var widgetId = getWidgetId();

    if (productId) {
      url.searchParams.set("product_id", productId);
    }
    if (widgetId) {
      url.searchParams.set("widget_id", widgetId);
    }

    var response = await fetch(url.toString());
    return parseResponse(response);
  }

  async function requestEvent() {
    var response = await fetch(getApiBaseUrl() + "/events", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        event_type: "recommendation_click",
        anonymous_id: "frontend_visual_anon",
        session_id: "frontend_visual_session",
        page_url: window.location.href,
        product_id: getProductId() || null,
        widget_id: getWidgetId(),
        recommended_product_id: "frontend-test-reco",
        metadata: {
          recommendation_count: 1,
          recommended_product_ids: ["frontend-test-reco"]
        }
      })
    });

    return parseResponse(response);
  }

  async function runAction(action) {
    var actionMap = {
      health: requestHealth,
      recommendations: requestRecommendations,
      event: requestEvent
    };

    if (!actionMap[action]) {
      return;
    }

    setStatus("Testando...", "loading");
    writeOutput("Chamando API local...");

    try {
      var data = await actionMap[action]();
      setStatus("Resposta recebida", "success");
      writeOutput(data);
    } catch (error) {
      setStatus("Falha no teste", "error");
      writeOutput({
        message: "Não foi possível chamar a API. Verifique se ela está em execução em localhost:8000 e se CORS inclui http://localhost:5600.",
        detail: error.message,
        response: error.body || null
      });
    }
  }

  function initTester() {
    if (!tester) {
      return;
    }

    tester.addEventListener("click", function (event) {
      var button = event.target.closest("[data-action]");
      if (!button) {
        return;
      }

      runAction(button.getAttribute("data-action"));
    });

    clearButton.addEventListener("click", function () {
      setStatus("Aguardando teste", "");
      writeOutput("Clique em um botão para ver a resposta JSON.");
    });
  }

  function initReveal() {
    var items = Array.prototype.slice.call(document.querySelectorAll(".reveal"));

    if (!("IntersectionObserver" in window)) {
      items.forEach(function (item) {
        item.classList.add("is-visible");
      });
      return;
    }

    var observer = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add("is-visible");
            observer.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.14 }
    );

    items.forEach(function (item) {
      observer.observe(item);
    });
  }

  initTester();
  initReveal();
})();
