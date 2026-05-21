/**
 * SEO KNA — Internal Linking & Keyword Mapping
 *
 * Cách dùng:
 * 1. Mở Google Sheet → Extensions → Apps Script
 * 2. Xóa code cũ, paste toàn bộ file này vào
 * 3. Lưu (Ctrl+S) → reload trang Sheet
 * 4. Menu "SEO KNA" sẽ xuất hiện trên thanh menu
 */

// ===================== CONFIG =====================
const CFG = {
  articlesTab:       "Articles",
  gscTab:            "GSC Data",
  keywordMappingTab: "Keyword Mapping",
  internalLinksTab:  "Internal Links",
  linkThreshold:     0.08,   // giảm xuống 0.05 nếu muốn nhiều gợi ý hơn
  maxLinksPerSource: 8,
  keywordThreshold:  0.05,
};

const STOP = new Set([
  "la","va","cua","trong","co","khong","voi","cho","de","tren","theo","khi",
  "nhu","duoc","tu","boi","dang","se","da","cac","nhung","mot","hai","ba",
  "nam","gi","nay","do","hay","hoac","rat","ve","tai","sau","truoc","neu",
  "vi","nen","the","thi","moi","cung","deu","nao","ay","o","a","i",
]);

// ===================== MENU =====================
function onOpen() {
  SpreadsheetApp.getUi()
    .createMenu("SEO KNA")
    .addItem("⚙️  Bước 0 — Tạo tab & hướng dẫn",  "setupTabs")
    .addSeparator()
    .addItem("📊 Bước 1 — Keyword Mapping",         "runKeywordMapping")
    .addItem("🔗 Bước 2 — Tìm Internal Links",      "runLinkFinder")
    .addSeparator()
    .addItem("🔑 Cài đặt WordPress",                "setupWordPress")
    .addItem("🚀 Bước 3 — Chèn link vào WordPress", "runLinkInserter")
    .addToUi();
}

// ===================== SETUP TABS =====================
function setupTabs() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const ui = SpreadsheetApp.getUi();

  _ensureTab(ss, CFG.articlesTab,
    ["URL", "Title", "Target Keywords", "Excerpt"],
    "#1a73e8"
  );

  _ensureTab(ss, CFG.gscTab,
    ["truy_van","luot_nhap","hien_thi","ctr","vi_tri","tu_khoa_chuan_hoa",
     "nhom_dich_vu","tieu_chuan_chung_nhan","nganh_chu_de","y_dinh_chinh",
     "giai_doan_pheu","loai_trang","cum_chu_de","co_hoi_seo","uu_tien_seo","ghi_chu"],
    "#f57c00"
  );

  ui.alert(
    "✅ Tạo tab thành công!\n\n" +
    "Bạn cần làm 2 việc trước khi chạy:\n\n" +
    "① Tab 'Articles':\n" +
    "   Điền danh sách bài viết: URL | Title | Target Keywords | Excerpt\n\n" +
    "② Tab 'GSC Data':\n" +
    "   Mở file  data/gsc/gsc-top100-report.tsv  bằng Excel hoặc Notepad\n" +
    "   → Copy toàn bộ nội dung → Paste vào tab 'GSC Data'\n\n" +
    "Sau đó quay lại menu SEO KNA → Bước 1."
  );

  ss.getSheetByName(CFG.articlesTab).activate();
}

function _ensureTab(ss, name, headers, color) {
  let sheet = ss.getSheetByName(name);
  if (!sheet) {
    sheet = ss.insertSheet(name);
    sheet.appendRow(headers);
    sheet.setFrozenRows(1);
    sheet.getRange(1, 1, 1, headers.length)
      .setBackground(color).setFontColor("#ffffff").setFontWeight("bold");
  }
  return sheet;
}

// ===================== TEXT UTILS =====================
function _normalize(text) {
  if (!text) return [];
  text = String(text).normalize("NFD").replace(/[̀-ͯ]/g, "");
  text = text.toLowerCase().replace(/[^\w\s]/g, " ");
  return text.split(/\s+/).filter(t => t.length > 1 && !STOP.has(t));
}

function _overlapCoef(a, b) {
  if (!a.length || !b.length) return 0;
  const sb = new Set(b);
  const inter = a.filter(t => sb.has(t)).length;
  return inter / Math.min(new Set(a).size, new Set(b).size);
}

// ===================== SHEET HELPERS =====================
function _readTab(tabName) {
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(tabName);
  if (!sheet) throw new Error(`Tab '${tabName}' không tồn tại. Chạy 'Bước 0 — Tạo tab' trước.`);
  const data = sheet.getDataRange().getValues();
  if (data.length < 2) return [];
  const headers = data[0].map(String);
  return data.slice(1)
    .filter(r => r.some(c => c !== ""))
    .map(r => Object.fromEntries(headers.map((h, i) => [h, r[i] ?? ""])));
}

function _writeTab(tabName, headers, rows, color) {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  let sheet = ss.getSheetByName(tabName);
  if (!sheet) {
    sheet = ss.insertSheet(tabName);
  } else {
    sheet.clearContents();
  }
  sheet.appendRow(headers);
  sheet.setFrozenRows(1);
  sheet.getRange(1, 1, 1, headers.length)
    .setBackground(color || "#2e7d32").setFontColor("#ffffff").setFontWeight("bold");
  if (rows.length) {
    sheet.getRange(2, 1, rows.length, headers.length).setValues(rows);
  }
  return sheet;
}

// ===================== KEYWORD MAPPING =====================
function runKeywordMapping() {
  try {
    const ui = SpreadsheetApp.getUi();
    const keywords = _readTab(CFG.gscTab);
    const articles = _readTab(CFG.articlesTab);

    if (!keywords.length) {
      ui.alert("Tab 'GSC Data' chưa có dữ liệu.\nPaste nội dung từ gsc-top100-report.tsv vào rồi thử lại.");
      return;
    }
    if (!articles.length) {
      ui.alert("Tab 'Articles' chưa có dữ liệu.\nĐiền danh sách bài viết trước.");
      return;
    }

    const headers = ["Keyword","Clicks","Impressions","CTR","Position","Cluster","Intent",
                     "Funnel","Page Type","SEO Priority","Mapped URL","Mapped Title","Confidence","Note"];

    const rows = keywords.map(kw => {
      let best = null, bestScore = 0;
      const artBase = _normalize((kw["truy_van"] || "") + " " + (kw["cum_chu_de"] || ""));

      for (const art of articles) {
        const artTokens = _normalize((art["Title"] || "") + " " + (art["Target Keywords"] || ""));
        const clusterScore = _overlapCoef(_normalize(kw["cum_chu_de"] || ""), artTokens);
        const queryScore   = _overlapCoef(_normalize(kw["truy_van"]   || ""), artTokens);
        const score = 0.4 * clusterScore + 0.6 * queryScore;
        if (score > bestScore) { bestScore = score; best = art; }
      }

      const mapped = bestScore >= CFG.keywordThreshold && best;
      let confidence = "Không khớp";
      if (bestScore >= 0.4)                        confidence = "Cao";
      else if (bestScore >= 0.15)                  confidence = "Trung bình";
      else if (bestScore >= CFG.keywordThreshold)  confidence = "Thấp";

      return [
        kw["truy_van"]       || "",
        kw["luot_nhap"]      || "",
        kw["hien_thi"]       || "",
        kw["ctr"]            || "",
        kw["vi_tri"]         || "",
        kw["cum_chu_de"]     || "",
        kw["y_dinh_chinh"]   || "",
        kw["giai_doan_pheu"] || "",
        kw["loai_trang"]     || "",
        kw["uu_tien_seo"]    || "",
        mapped ? best["URL"]   : "",
        mapped ? best["Title"] : "",
        confidence,
        kw["ghi_chu"] || "",
      ];
    });

    const sheet = _writeTab(CFG.keywordMappingTab, headers, rows, "#1565c0");
    sheet.autoResizeColumns(1, headers.length);

    const mappedCount = rows.filter(r => r[10]).length;
    const unmapped = rows.filter(r => !r[10]).map(r => r[0]).slice(0, 5).join(", ");

    ui.alert(
      `✅ Keyword Mapping hoàn tất!\n\n` +
      `• ${mappedCount}/${keywords.length} từ khóa được map vào bài viết\n` +
      `• ${keywords.length - mappedCount} từ khóa chưa khớp\n` +
      (unmapped ? `  Ví dụ: ${unmapped}...\n  → Thêm bài viết tương ứng vào tab Articles\n` : "") +
      `\nXem kết quả ở tab '${CFG.keywordMappingTab}'`
    );
    SpreadsheetApp.getActiveSpreadsheet().getSheetByName(CFG.keywordMappingTab).activate();

  } catch (e) {
    SpreadsheetApp.getUi().alert("❌ Lỗi: " + e.message);
  }
}

// ===================== LINK FINDER =====================
function runLinkFinder() {
  try {
    const ui = SpreadsheetApp.getUi();
    const articles = _readTab(CFG.articlesTab);

    if (articles.length < 2) {
      ui.alert("Cần ít nhất 2 bài viết trong tab 'Articles'.");
      return;
    }

    // Build token sets
    const tokenMap = {};
    for (const art of articles) {
      tokenMap[art["URL"]] = _normalize(
        (art["Title"] || "") + " " + (art["Target Keywords"] || "") + " " + (art["Excerpt"] || "")
      );
    }

    // Score all ordered pairs
    const pairs = [];
    for (let i = 0; i < articles.length; i++) {
      for (let j = 0; j < articles.length; j++) {
        if (i === j) continue;
        const score = _overlapCoef(tokenMap[articles[i]["URL"]], tokenMap[articles[j]["URL"]]);
        if (score >= CFG.linkThreshold) {
          pairs.push([score, articles[i], articles[j]]);
        }
      }
    }
    pairs.sort((a, b) => b[0] - a[0]);

    // Cap outgoing links per source
    const outgoing = {};
    const opportunities = [];
    for (const [score, src, tgt] of pairs) {
      const srcUrl = src["URL"];
      if ((outgoing[srcUrl] || 0) >= CFG.maxLinksPerSource) continue;
      const anchor = _findAnchor(src, tgt);
      if (!anchor) continue;
      opportunities.push([srcUrl, src["Title"] || "", tgt["URL"], tgt["Title"] || "", anchor, score.toFixed(3), "pending"]);
      outgoing[srcUrl] = (outgoing[srcUrl] || 0) + 1;
    }

    // Append-only to preserve existing Status edits
    const headers = ["Source URL","Source Title","Target URL","Target Title","Anchor Text","Relevance Score","Status"];
    const ss = SpreadsheetApp.getActiveSpreadsheet();
    let sheet = ss.getSheetByName(CFG.internalLinksTab);
    const existingKeys = new Set();

    if (!sheet) {
      sheet = ss.insertSheet(CFG.internalLinksTab);
      sheet.appendRow(headers);
      sheet.setFrozenRows(1);
      sheet.getRange(1, 1, 1, headers.length)
        .setBackground("#2e7d32").setFontColor("#ffffff").setFontWeight("bold");
    } else {
      const existing = sheet.getDataRange().getValues().slice(1);
      existing.forEach(r => existingKeys.add(`${r[0]}|||${r[2]}`));
    }

    const toAdd = opportunities.filter(r => !existingKeys.has(`${r[0]}|||${r[2]}`));
    if (toAdd.length) {
      sheet.getRange(sheet.getLastRow() + 1, 1, toAdd.length, headers.length).setValues(toAdd);
    }

    ui.alert(
      `✅ Tìm Internal Links hoàn tất!\n\n` +
      `• Tìm thấy: ${opportunities.length} cơ hội\n` +
      `• Thêm mới: ${toAdd.length} dòng\n\n` +
      `Tiếp theo:\n` +
      `Mở tab '${CFG.internalLinksTab}' → đổi cột Status:\n` +
      `  pending  →  approved  (link muốn chèn)\n` +
      `  pending  →  rejected  (link bỏ qua)\n\n` +
      `Sau đó: SEO KNA → Bước 3 — Chèn link vào WordPress`
    );
    ss.getSheetByName(CFG.internalLinksTab).activate();

  } catch (e) {
    SpreadsheetApp.getUi().alert("❌ Lỗi: " + e.message);
  }
}

function _findAnchor(src, tgt) {
  const srcText = ((src["Title"] || "") + " " + (src["Target Keywords"] || "") + " " + (src["Excerpt"] || ""))
    .toLowerCase().normalize("NFD").replace(/[̀-ͯ]/g, "");
  const kwList = (tgt["Target Keywords"] || "").split(",").map(k => k.trim()).filter(Boolean);
  kwList.sort((a, b) => b.length - a.length); // prefer longer phrases
  for (const kw of kwList) {
    const norm = kw.toLowerCase().normalize("NFD").replace(/[̀-ͯ]/g, "");
    if (srcText.includes(norm)) return kw;
  }
  return kwList[0] || tgt["Title"] || "";
}

// ===================== WORDPRESS — SETUP =====================
function setupWordPress() {
  const ui = SpreadsheetApp.getUi();
  const props = PropertiesService.getScriptProperties();

  let r = ui.prompt("WordPress URL", "Ví dụ: https://knacert.com.vn", ui.ButtonSet.OK_CANCEL);
  if (r.getSelectedButton() !== ui.Button.OK) return;
  props.setProperty("WP_URL", r.getResponseText().trim().replace(/\/$/, ""));

  r = ui.prompt("WordPress Username", "Email hoặc tên đăng nhập admin", ui.ButtonSet.OK_CANCEL);
  if (r.getSelectedButton() !== ui.Button.OK) return;
  props.setProperty("WP_USER", r.getResponseText().trim());

  r = ui.prompt(
    "WordPress Application Password",
    "Lấy tại: WP Admin → Users → Profile → Application Passwords → Generate",
    ui.ButtonSet.OK_CANCEL
  );
  if (r.getSelectedButton() !== ui.Button.OK) return;
  props.setProperty("WP_PASS", r.getResponseText().trim());

  ui.alert("✅ Đã lưu thông tin WordPress!\n\nMật khẩu được lưu mã hóa trong Script Properties, không ai thấy được.");
}

// ===================== WORDPRESS — INSERT LINKS =====================
function runLinkInserter() {
  const ui = SpreadsheetApp.getUi();

  // Check WP credentials
  const props = PropertiesService.getScriptProperties();
  if (!props.getProperty("WP_URL")) {
    ui.alert("Chưa cài đặt WordPress.\nChạy: SEO KNA → Cài đặt WordPress trước.");
    return;
  }

  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const sheet = ss.getSheetByName(CFG.internalLinksTab);
  if (!sheet) {
    ui.alert("Tab 'Internal Links' không tồn tại. Chạy Bước 2 trước.");
    return;
  }

  const data = sheet.getDataRange().getValues();
  const headers = data[0].map(String);
  const srcCol    = headers.indexOf("Source URL");
  const tgtCol    = headers.indexOf("Target URL");
  const anchorCol = headers.indexOf("Anchor Text");
  const statusCol = headers.indexOf("Status");

  const approved = [];
  for (let i = 1; i < data.length; i++) {
    if (String(data[i][statusCol] || "").trim().toLowerCase() === "approved") {
      approved.push({ row: i + 1, src: data[i][srcCol], tgt: data[i][tgtCol], anchor: data[i][anchorCol] });
    }
  }

  if (!approved.length) {
    ui.alert("Không có dòng nào với Status = 'approved'.\nMở tab 'Internal Links', đổi Status của các link muốn chèn thành 'approved' rồi thử lại.");
    return;
  }

  const confirm = ui.alert(
    `Xác nhận chèn ${approved.length} internal link vào WordPress?`,
    ui.ButtonSet.YES_NO
  );
  if (confirm !== ui.Button.YES) return;

  let inserted = 0, skipped = 0, errors = 0;
  const postCache = {};

  for (const item of approved) {
    try {
      if (!postCache[item.src]) postCache[item.src] = _findWpPost(item.src);
      const found = postCache[item.src];

      if (!found) {
        sheet.getRange(item.row, statusCol + 1).setValue("error: bài không tìm thấy");
        errors++;
        continue;
      }

      const rawContent = (found.post.content && found.post.content.raw) || "";
      const [newContent, wasInserted] = _insertLink(rawContent, item.anchor, item.tgt);

      if (!wasInserted) {
        sheet.getRange(item.row, statusCol + 1).setValue("skipped: anchor không có trong bài");
        skipped++;
        continue;
      }

      _wpPost(`${found.type}/${found.post.id}`, { content: newContent });
      sheet.getRange(item.row, statusCol + 1).setValue("inserted");
      inserted++;
      Utilities.sleep(600); // tránh quá tải API

    } catch (e) {
      sheet.getRange(item.row, statusCol + 1).setValue("error: " + e.message.substring(0, 80));
      errors++;
    }
  }

  ui.alert(
    `✅ Hoàn tất!\n\n` +
    `✓ Chèn thành công: ${inserted}\n` +
    `− Bỏ qua (không tìm thấy anchor): ${skipped}\n` +
    `✗ Lỗi: ${errors}\n\n` +
    (errors > 0 ? "Xem cột Status để biết lỗi cụ thể." : "")
  );
}

function _wpPost(path, payload) {
  const props = PropertiesService.getScriptProperties();
  const token = Utilities.base64Encode(`${props.getProperty("WP_USER")}:${props.getProperty("WP_PASS")}`);
  const resp = UrlFetchApp.fetch(
    `${props.getProperty("WP_URL")}/wp-json/wp/v2/${path}`,
    {
      method: "post",
      headers: { "Authorization": `Basic ${token}`, "Content-Type": "application/json" },
      payload: JSON.stringify(payload),
      muteHttpExceptions: true,
    }
  );
  const code = resp.getResponseCode();
  if (code < 200 || code >= 300) throw new Error(`HTTP ${code}: ${resp.getContentText().substring(0, 150)}`);
  return JSON.parse(resp.getContentText());
}

function _wpGet(path) {
  const props = PropertiesService.getScriptProperties();
  const token = Utilities.base64Encode(`${props.getProperty("WP_USER")}:${props.getProperty("WP_PASS")}`);
  const resp = UrlFetchApp.fetch(
    `${props.getProperty("WP_URL")}/wp-json/wp/v2/${path}`,
    {
      method: "get",
      headers: { "Authorization": `Basic ${token}` },
      muteHttpExceptions: true,
    }
  );
  const code = resp.getResponseCode();
  if (code < 200 || code >= 300) return null;
  return JSON.parse(resp.getContentText());
}

function _findWpPost(postUrl) {
  const slug = postUrl.replace(/\/$/, "").split("/").pop();
  for (const type of ["posts", "pages"]) {
    const results = _wpGet(`${type}?slug=${encodeURIComponent(slug)}&context=edit&_fields=id,content,title`);
    if (Array.isArray(results) && results.length) return { type, post: results[0] };
  }
  return null;
}

function _insertLink(content, anchor, targetUrl) {
  // Collect existing linked ranges
  const linkRe = /<a\b[^>]*>[\s\S]*?<\/a>/gi;
  const linked = [];
  let m;
  while ((m = linkRe.exec(content)) !== null) linked.push([m.index, m.index + m[0].length]);

  const escaped = anchor.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
  const re = new RegExp(escaped, "i");
  const match = re.exec(content);
  if (!match) return [content, false];

  const inLink = linked.some(([s, e]) => match.index >= s && match.index < e);
  if (inLink) return [content, false];

  return [
    content.substring(0, match.index) +
    `<a href="${targetUrl}">${match[0]}</a>` +
    content.substring(match.index + match[0].length),
    true
  ];
}
