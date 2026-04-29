(function () {
  "use strict";

  var memoryIds = {};
  var globalConfig = window.KouzinaReco || {};
  var CONFIG = {
    apiBaseUrl: globalConfig.apiBaseUrl || "http://localhost:8000",
    publicKey: globalConfig.publicKey || "kouzina_public_dev_key",
    widgetSelector: globalConfig.widgetSelector || "[data-kouzina-reco]",
  };

  function warn(message, error) {
    if (window.console && typeof window.console.warn === "function") {
      window.console.warn("[KouzinaReco] " + message, error || "");
    }
  }

  function generateId(prefix) {
    if (window.crypto && typeof window.crypto.randomUUID === "function") {
      return prefix + "_" + window.crypto.randomUUID();
    }

    return (
      prefix +
      "_" +
      Date.now().toString(36) +
      "_" +
      Math.random().toString(36).slice(2)
    );
  }

  function getStorage(storageName) {
    try {
      return window[storageName];
    } catch (error) {
      warn(storageName + " unavailable", error);
      return null;
    }
  }

  function getOrCreateStorageId(storageName, key, prefix) {
    try {
      var storage = getStorage(storageName);
      if (!storage) {
        throw new Error(storageName + " unavailable");
      }

      var value = storage.getItem(key);
      if (!value) {
        value = generateId(prefix);
        storage.setItem(key, value);
      }
      return value;
    } catch (error) {
      warn("storage unavailable", error);
      if (!memoryIds[key]) {
        memoryIds[key] = generateId(prefix);
      }
      return memoryIds[key];
    }
  }

  var anonymousId = getOrCreateStorageId(
    "localStorage",
    "kouzina_reco_anonymous_id",
    "anon"
  );
  var sessionId = getOrCreateStorageId(
    "sessionStorage",
    "kouzina_reco_session_id",
    "sess"
  );

  function detectProductId() {
    var container = document.querySelector("[data-kouzina-product-id]");
    if (container && container.getAttribute("data-kouzina-product-id")) {
      return container.getAttribute("data-kouzina-product-id");
    }

    var metaProduct = document.querySelector(
      "meta[property='product:retailer_item_id']"
    );
    if (metaProduct && metaProduct.content) {
      return metaProduct.content;
    }

    var bodyText = document.body ? document.body.innerText || "" : "";
    var match = bodyText.match(/Codigo[:\s]+([A-Za-z0-9_-]+)/i);
    return match ? match[1] : null;
  }

  async function sendEvent(eventType, extra) {
    extra = extra || {};

    try {
      await fetch(CONFIG.apiBaseUrl + "/events", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-Kouzina-Public-Key": CONFIG.publicKey,
        },
        body: JSON.stringify({
          event_type: eventType,
          anonymous_id: anonymousId,
          session_id: sessionId,
          page_url: window.location.href,
          product_id: extra.product_id || detectProductId(),
          widget_id: extra.widget_id || null,
          recommended_product_id: extra.recommended_product_id || null,
          metadata: extra.metadata || {},
        }),
        keepalive: true,
      });
    } catch (error) {
      warn("event error", error);
    }
  }

  async function fetchRecommendations(productId, widgetId) {
    var url = new URL(CONFIG.apiBaseUrl + "/recommendations");
    if (productId) {
      url.searchParams.set("product_id", productId);
    }
    if (widgetId) {
      url.searchParams.set("widget_id", widgetId);
    }

    var response = await fetch(url.toString(), {
      headers: {
        "X-Kouzina-Public-Key": CONFIG.publicKey,
      },
    });

    if (!response.ok) {
      throw new Error("recommendations request failed: " + response.status);
    }

    return response.json();
  }

  function formatPrice(value) {
    if (typeof value !== "number") {
      return "";
    }

    return value.toLocaleString("pt-BR", {
      style: "currency",
      currency: "BRL",
    });
  }

  function createCard(item, widgetId, productId) {
    var card = document.createElement("a");
    card.className = "kouzina-reco-card";
    card.href = item.url;
    card.setAttribute("data-kouzina-reco-click", item.product_id);

    if (item.image_url) {
      var image = document.createElement("img");
      image.className = "kouzina-reco-image";
      image.src = item.image_url;
      image.alt = item.name;
      card.appendChild(image);
    }

    var name = document.createElement("strong");
    name.className = "kouzina-reco-name";
    name.textContent = item.name;
    card.appendChild(name);

    var price = formatPrice(item.price);
    if (price) {
      var priceNode = document.createElement("span");
      priceNode.className = "kouzina-reco-price";
      priceNode.textContent = price;
      card.appendChild(priceNode);
    }

    var reason = document.createElement("small");
    reason.className = "kouzina-reco-reason";
    reason.textContent = item.reason;
    card.appendChild(reason);

    card.addEventListener("click", function () {
      sendEvent("recommendation_click", {
        widget_id: widgetId,
        product_id: productId,
        recommended_product_id: item.product_id,
        metadata: {
          score: item.score,
        },
      });
    });

    return card;
  }

  function renderWidget(container, data, widgetId, productId) {
    container.innerHTML = "";

    var root = document.createElement("section");
    root.className = "kouzina-reco";

    var style = document.createElement("style");
    style.textContent =
      ".kouzina-reco{border:1px solid #e7e2d8;border-radius:14px;padding:18px;margin:24px 0;background:#fffaf0;color:#1f1a14;font-family:Georgia,'Times New Roman',serif}" +
      ".kouzina-reco-title{font-size:22px;margin:0 0 6px}" +
      ".kouzina-reco-subtitle{margin:0 0 16px;color:#6a5f52;font-size:14px}" +
      ".kouzina-reco-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:12px}" +
      ".kouzina-reco-card{display:block;text-decoration:none;color:#1f1a14;border:1px solid #eee2cf;border-radius:12px;padding:14px;background:#fff;transition:transform .15s ease,border-color .15s ease}" +
      ".kouzina-reco-card:hover{transform:translateY(-2px);border-color:#b8864b}" +
      ".kouzina-reco-image{display:block;max-width:100%;height:auto;margin-bottom:10px;border-radius:8px}" +
      ".kouzina-reco-name{display:block;margin-bottom:8px;font-size:15px;line-height:1.3}" +
      ".kouzina-reco-price{display:block;margin-bottom:8px;color:#7a4b17;font-weight:700}" +
      ".kouzina-reco-reason{display:block;color:#6a5f52;line-height:1.35}";
    root.appendChild(style);

    var title = document.createElement("h2");
    title.className = "kouzina-reco-title";
    title.textContent = data.widget_title || "Complete seu projeto";
    root.appendChild(title);

    var subtitle = document.createElement("p");
    subtitle.className = "kouzina-reco-subtitle";
    subtitle.textContent = "Produtos selecionados para complementar sua escolha.";
    root.appendChild(subtitle);

    var grid = document.createElement("div");
    grid.className = "kouzina-reco-grid";

    (data.recommendations || []).forEach(function (item) {
      grid.appendChild(createCard(item, widgetId, productId));
    });

    root.appendChild(grid);
    container.appendChild(root);
  }

  async function initContainer(container, productId) {
    var widgetId = container.getAttribute("data-kouzina-reco") || "product-page";

    try {
      var data = await fetchRecommendations(productId, widgetId);
      renderWidget(container, data, widgetId, productId);

      sendEvent("recommendation_impression", {
        widget_id: widgetId,
        product_id: productId,
        metadata: {
          recommendation_count: (data.recommendations || []).length,
          recommended_product_ids: (data.recommendations || []).map(function (item) {
            return item.product_id;
          }),
        },
      });
    } catch (error) {
      warn("recommendation error", error);
    }
  }

  function init() {
    try {
      var productId = detectProductId();
      sendEvent("page_view", { product_id: productId });

      var containers = document.querySelectorAll(CONFIG.widgetSelector);
      if (!containers.length) {
        warn("no widget containers found");
        return;
      }

      containers.forEach(function (container) {
        initContainer(container, productId);
      });
    } catch (error) {
      warn("init error", error);
    }
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
