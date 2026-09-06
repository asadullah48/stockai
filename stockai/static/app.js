// StockAI Interactive Controller & Bilingual Localization

let currentLang = 'en';

const TRANSLATIONS = {
  en: {
    badgeTitle: "Inventory Automation",
    statusLive: "Supply Chain Harness Active (:8019)",
    heroTitle: "Autonomous Stock Monitoring, Demand Forecasting & PO Automation",
    heroSubtitle: "Eliminate stockouts and excess inventory costs with MonitorAgent (velocity tracking), ForecastAgent (30-day seasonal demand), and OrderAgent (automated supplier PO & email drafting).",
    metric1Label: "Stockout Prevention",
    metric1Sub: "Buffer ROP Calculation",
    metric2Label: "Demand Accuracy",
    metric2Sub: "Seasonal Multipliers",
    metric3Label: "Reorder Latency",
    metric3Sub: "Instant PO Drafting",
    metric4Label: "SME Working Capital",
    metric4Sub: "Zero Excess Holding",
    studioTitle: "Autonomous Inventory Control Studio",
    studioDesc: "Inspect real-time SKU stock levels, trigger automated demand forecasting, and review generated supplier purchase order drafts.",
    lblPresets: "Select Preset SKU Scenario:",
    lblSKU: "SKU Code",
    lblCurrentStock: "Current Stock",
    lblSafety: "Safety Threshold",
    lblRunRate: "Daily Run Rate",
    btnExecuteProcess: "📦 Execute Stock Pipeline & Draft PO",
    titlePurchaseOrder: "Draft Supplier Purchase Order",
    lblInsight: "🧠 InsightAgent Executive Summary:",
    lblEmailDraft: "Automated Supplier Reorder Email:"
  },
  ar: {
    badgeTitle: "أتمتة المخزون والتوريد",
    statusLive: "محرك سلاسل الإمداد نشط (:8019)",
    heroTitle: "مراقبة المخزون التلقائية، والتنبؤ بالطلب، وتوليد أوامر الشراء",
    heroSubtitle: "القضاء على نفاد المخزون وتكاليف التخزين الفائض مع MonitorAgent (تتبع سرعة النضوب)، و ForecastAgent (التنبؤ بالطلب لـ 30 يوماً)، و OrderAgent (صياغة أوامر الشراء ورسائل الموردين).",
    metric1Label: "منع نفاد المخزون",
    metric1Sub: "حساب نقطة إعادة الطلب ROP",
    metric2Label: "دقة التنبؤ بالطلب",
    metric2Sub: "معاملات النمو الموسمي",
    metric3Label: "سرعة توليد أمر الشراء",
    metric3Sub: "صياغة فورية للبريد والطلب",
    metric4Label: "كفاءة رأس المال العامل",
    metric4Sub: "انعدام المخزون الراكد",
    studioTitle: "استوديو التحكم الذكي بالمخزون",
    studioDesc: "فحص مستويات المنتجات الحالية، وإطلاق التنبؤ بالطلب، والاطلاع على مسودة أمر الشراء والبريد الإلكتروني الموجه للمورد.",
    lblPresets: "اختر سيناريو منتج مسبق:",
    lblSKU: "رمز المنتج (SKU)",
    lblCurrentStock: "المخزون الحالي",
    lblSafety: "حد الأمان الأدنى",
    lblRunRate: "معدل السحب اليومي",
    btnExecuteProcess: "📦 تشغيل دورة المخزون وتوليد أمر الشراء",
    titlePurchaseOrder: "مسودة أمر شراء المورد (PO)",
    lblInsight: "🧠 الملخص التنفيذي لوكيل الرؤى:",
    lblEmailDraft: "البريد الإلكتروني المؤتمت لإعادة الطلب:"
  }
};

const SCENARIOS = [
  {
    name: "🖱️ SKU-9920: Ergonomic Wireless Mouse (Low Stock)",
    sku: "SKU-9920",
    stock: 14,
    safety: 25,
    rate: 4.5
  },
  {
    name: "🎧 SKU-4412: ANC Wireless Headphones (Critical Outage)",
    sku: "SKU-4412",
    stock: 4,
    safety: 30,
    rate: 6.0
  },
  {
    name: "⌨️ SKU-7731: Mechanical Gaming Keyboard (Optimal)",
    sku: "SKU-7731",
    stock: 85,
    safety: 20,
    rate: 3.0
  }
];

function init() {
  renderPresets();
  runInventoryPipeline();
}

function toggleLanguage() {
  currentLang = currentLang === 'en' ? 'ar' : 'en';
  document.documentElement.lang = currentLang;
  document.documentElement.dir = currentLang === 'ar' ? 'rtl' : 'ltr';
  document.getElementById('langLabel').innerText = currentLang === 'en' ? 'العربية' : 'English';

  document.querySelectorAll('[data-i18n]').forEach(el => {
    const key = el.getAttribute('data-i18n');
    if (TRANSLATIONS[currentLang][key]) {
      el.innerText = TRANSLATIONS[currentLang][key];
    }
  });
}

function renderPresets() {
  const container = document.getElementById('scenarioButtons');
  container.innerHTML = '';
  SCENARIOS.forEach((sc, idx) => {
    const btn = document.createElement('button');
    btn.className = 'preset-btn';
    btn.innerText = sc.name;
    btn.onclick = () => loadScenario(idx);
    container.appendChild(btn);
  });
}

function loadScenario(idx) {
  const sc = SCENARIOS[idx];
  document.getElementById('skuInput').value = sc.sku;
  document.getElementById('stockInput').value = sc.stock;
  document.getElementById('safetyInput').value = sc.safety;
  document.getElementById('rateInput').value = sc.rate;
  runInventoryPipeline();
}

async function runInventoryPipeline() {
  const btn = document.getElementById('processBtn');
  const sku = document.getElementById('skuInput').value;
  const stock = parseInt(document.getElementById('stockInput').value);
  const safety = parseInt(document.getElementById('safetyInput').value);
  const rate = parseFloat(document.getElementById('rateInput').value);

  btn.disabled = true;
  btn.innerText = "Monitoring Stock -> Forecasting 30D Demand -> Drafting Supplier PO...";

  try {
    const res = await fetch('/api/v1/inventory/process-sku', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        sku: sku,
        item_name: "Electronics Peripheral Component",
        category: "Hardware",
        current_stock: stock,
        safety_stock_threshold: safety,
        daily_run_rate: rate,
        unit_cost_usd: 24.50,
        lead_time_days: 7,
        vendor_name: "Apex Precision Components Ltd",
        vendor_email: "orders@apexprecision.com"
      })
    });

    const data = await res.json();
    renderPipelineResult(data);

  } catch (err) {
    document.getElementById('emailStream').innerText = `Error: ${err.message}`;
  } finally {
    btn.disabled = false;
    btn.innerText = TRANSLATIONS[currentLang].btnExecuteProcess;
  }
}

function renderPipelineResult(data) {
  const badge = document.getElementById('stockBadge');
  badge.innerText = `${data.monitoring.status.replace('_', ' ')} (Risk: ${data.monitoring.risk_level})`;

  const bar = document.getElementById('pipelineBar');
  bar.innerHTML = `
    <span class="pipe-tag">ETA to Stockout: ${data.monitoring.stockout_eta_days} Days</span>
    <span class="pipe-tag">Demand (30D): ${data.forecast.predicted_demand_units} Units</span>
    <span class="pipe-tag">Reorder Qty: ${data.purchase_order.order_quantity} Units</span>
    <span class="pipe-tag">Total PO: $${data.purchase_order.total_amount_usd.toFixed(2)}</span>
  `;

  document.getElementById('emailStream').innerText = data.purchase_order.email_body_draft;

  document.getElementById('insightStream').innerText = data.insight.summary;
  const sourceBadge = document.getElementById('insightSourceBadge');
  const isLLM = data.insight.source.startsWith('ollama:');
  sourceBadge.innerText = isLLM ? `LLM · ${data.insight.source}` : 'rule-based template';
  sourceBadge.className = isLLM ? 'badge badge-success' : 'badge badge-warning';
}

window.addEventListener('DOMContentLoaded', init);
