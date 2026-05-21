/**
 * KNA CERT - Google Sheet to WordPress Auto Post
 *
 * Cách dùng:
 * 1. Import templates/wordpress-auto-post-template.csv vào Google Sheets.
 * 2. Vào Extensions > Apps Script, dán toàn bộ file này.
 * 3. Sửa thông tin trong setWordPressConfig(), chạy hàm này 1 lần.
 * 4. Chạy setupSheetFormatting() 1 lần để định dạng Sheet.
 * 5. Chạy installAutoPostTrigger() 1 lần để tạo trigger tự động.
 * 6. Nhập dữ liệu bài viết, sau cùng đặt Publish Action = create hoặc pending.
 *
 * Không lưu mật khẩu WordPress trong Google Sheet.
 */

const SHEET_NAME = 'wordpress-auto-post-template';

const COL = {
  ROW: 1,
  ACTION: 2,
  WP_STATUS: 3,
  POST_TYPE: 4,
  POST_ID: 5,
  TITLE: 6,
  SLUG: 7,
  CONTENT: 8,
  EXCERPT: 9,
  CATEGORIES: 10,
  TAGS: 11,
  FEATURED_MEDIA_ID: 12,
  META_TITLE: 13,
  META_DESCRIPTION: 14,
  WP_URL: 15,
  PUBLISH_STATUS: 16,
  ERROR: 17,
  LAST_RUN: 18,
  NOTES: 19,
};

const VALID_ACTIONS = ['pending', 'create', 'update'];
const VALID_STATUSES = ['draft', 'pending', 'publish', 'private'];

function setWordPressConfig() {
  PropertiesService.getScriptProperties().setProperties({
    WP_SITE_URL: 'https://knacert.com.vn',
    WP_USERNAME: 'YOUR_WORDPRESS_USERNAME',
    WP_APP_PASSWORD: 'YOUR_WORDPRESS_APPLICATION_PASSWORD',
  });
}

function installAutoPostTrigger() {
  const triggers = ScriptApp.getProjectTriggers();
  triggers.forEach((trigger) => {
    if (trigger.getHandlerFunction() === 'onEditAutoPost') {
      ScriptApp.deleteTrigger(trigger);
    }
  });

  ScriptApp.newTrigger('onEditAutoPost')
    .forSpreadsheet(SpreadsheetApp.getActive())
    .onEdit()
    .create();
}

function setupSheetFormatting() {
  const sheet = SpreadsheetApp.getActiveSheet();
  sheet.setName(SHEET_NAME);
  sheet.setFrozenRows(1);
  sheet.setFrozenColumns(5);

  const header = sheet.getRange(1, 1, 1, COL.NOTES);
  header
    .setBackground('#263238')
    .setFontColor('#ffffff')
    .setFontWeight('bold')
    .setWrap(true);

  sheet.setColumnWidth(COL.ROW, 55);
  sheet.setColumnWidth(COL.ACTION, 130);
  sheet.setColumnWidth(COL.WP_STATUS, 110);
  sheet.setColumnWidth(COL.POST_TYPE, 100);
  sheet.setColumnWidth(COL.POST_ID, 90);
  sheet.setColumnWidth(COL.TITLE, 320);
  sheet.setColumnWidth(COL.SLUG, 230);
  sheet.setColumnWidth(COL.CONTENT, 520);
  sheet.setColumnWidth(COL.EXCERPT, 320);
  sheet.setColumnWidth(COL.WP_URL, 320);
  sheet.setColumnWidth(COL.ERROR, 360);
  sheet.setColumnWidth(COL.NOTES, 260);

  addValidation(sheet, COL.ACTION, ['skip', 'pending', 'create', 'update']);
  addValidation(sheet, COL.WP_STATUS, ['draft', 'pending', 'publish', 'private']);
  addValidation(sheet, COL.POST_TYPE, ['posts', 'pages', 'service']);
  addValidation(sheet, COL.PUBLISH_STATUS, ['success', 'error', 'skipped']);

  sheet.getRange(2, 1, Math.max(sheet.getMaxRows() - 1, 1), COL.NOTES)
    .setWrap(true)
    .setVerticalAlignment('top');
}

function onEditAutoPost(e) {
  if (!e || !e.range) return;

  const sheet = e.range.getSheet();
  if (sheet.getName() !== SHEET_NAME || e.range.getRow() < 2) return;

  const row = e.range.getRow();
  const action = getCell(sheet, row, COL.ACTION).toLowerCase();
  if (!VALID_ACTIONS.includes(action)) return;

  processRow(sheet, row);
}

function processPendingRows() {
  const sheet = getInputSheet();
  const lastRow = sheet.getLastRow();
  for (let row = 2; row <= lastRow; row++) {
    const action = getCell(sheet, row, COL.ACTION).toLowerCase();
    if (VALID_ACTIONS.includes(action)) {
      processRow(sheet, row);
    }
  }
}

function processRow(sheet, row) {
  const lock = LockService.getScriptLock();
  if (!lock.tryLock(30000)) return;

  try {
    const data = readRow(sheet, row);

    if (!data.title || !data.content) {
      writeResult(sheet, row, '', '', 'error', 'Thiếu Title hoặc Content HTML.');
      return;
    }

    if (data.action === 'create' && data.postId) {
      writeResult(sheet, row, '', '', 'error', 'Publish Action=create nhưng Post ID đã có. Dùng update nếu muốn cập nhật.');
      return;
    }

    if (data.action === 'update' && !data.postId) {
      writeResult(sheet, row, '', '', 'error', 'Publish Action=update nhưng Post ID đang trống.');
      return;
    }

    const endpointBase = getEndpointBase(data.postType);
    const methodPath = data.action === 'update'
      ? `/wp-json/wp/v2/${endpointBase}/${data.postId}`
      : `/wp-json/wp/v2/${endpointBase}`;

    const payload = buildPayload(data);
    const result = wordpressRequest(methodPath, payload);

    writeResult(
      sheet,
      row,
      result.link || '',
      result.id || data.postId || '',
      'success',
      ''
    );

    sheet.getRange(row, COL.ACTION).setValue('skip');
  } catch (err) {
    writeResult(sheet, row, '', '', 'error', String(err && err.message ? err.message : err));
  } finally {
    lock.releaseLock();
  }
}

function readRow(sheet, row) {
  return {
    action: getCell(sheet, row, COL.ACTION).toLowerCase(),
    wpStatus: normalizeStatus(getCell(sheet, row, COL.WP_STATUS)),
    postType: getCell(sheet, row, COL.POST_TYPE) || 'posts',
    postId: getCell(sheet, row, COL.POST_ID),
    title: getCell(sheet, row, COL.TITLE),
    slug: getCell(sheet, row, COL.SLUG),
    content: getCell(sheet, row, COL.CONTENT),
    excerpt: getCell(sheet, row, COL.EXCERPT),
    categories: parseTokenList(getCell(sheet, row, COL.CATEGORIES)),
    tags: parseTokenList(getCell(sheet, row, COL.TAGS)),
    featuredMediaId: getCell(sheet, row, COL.FEATURED_MEDIA_ID),
    metaTitle: getCell(sheet, row, COL.META_TITLE),
    metaDescription: getCell(sheet, row, COL.META_DESCRIPTION),
  };
}

function buildPayload(data) {
  const payload = {
    title: data.title,
    content: data.content,
    status: data.wpStatus,
  };

  if (data.slug) payload.slug = data.slug;
  if (data.excerpt) payload.excerpt = data.excerpt;
  if (data.categories.length) payload.categories = resolveTermIds('categories', data.categories);
  if (data.tags.length) payload.tags = resolveTermIds('tags', data.tags);
  if (data.featuredMediaId) payload.featured_media = Number(data.featuredMediaId);

  const meta = {};
  if (data.metaTitle) meta._yoast_wpseo_title = data.metaTitle;
  if (data.metaDescription) meta._yoast_wpseo_metadesc = data.metaDescription;
  if (Object.keys(meta).length) payload.meta = meta;

  return payload;
}

function wordpressRequest(path, payload) {
  const props = PropertiesService.getScriptProperties();
  const siteUrl = requiredProp(props, 'WP_SITE_URL').replace(/\/$/, '');
  const username = requiredProp(props, 'WP_USERNAME');
  const appPassword = requiredProp(props, 'WP_APP_PASSWORD');
  const token = Utilities.base64Encode(`${username}:${appPassword}`);

  const response = UrlFetchApp.fetch(`${siteUrl}${path}`, {
    method: 'post',
    muteHttpExceptions: true,
    contentType: 'application/json; charset=utf-8',
    headers: {
      Authorization: `Basic ${token}`,
      Accept: 'application/json',
    },
    payload: JSON.stringify(payload),
  });

  const status = response.getResponseCode();
  const body = response.getContentText();
  let parsed = {};
  try {
    parsed = body ? JSON.parse(body) : {};
  } catch (err) {
    parsed = { raw: body };
  }

  if (status < 200 || status >= 300) {
    throw new Error(`WordPress API lỗi ${status}: ${body}`);
  }

  return parsed;
}

function getEndpointBase(postType) {
  const value = String(postType || 'posts').trim().replace(/^\/+|\/+$/g, '');
  if (value === 'post') return 'posts';
  if (value === 'page') return 'pages';
  return value;
}

function normalizeStatus(value) {
  const status = String(value || 'draft').trim().toLowerCase();
  return VALID_STATUSES.includes(status) ? status : 'draft';
}

function parseTokenList(value) {
  return String(value || '')
    .split(',')
    .map((item) => item.trim())
    .filter(Boolean);
}

function resolveTermIds(endpoint, tokens) {
  const terms = getWpTerms(endpoint);
  return tokens.map((token) => {
    if (/^\d+$/.test(token)) return Number(token);

    const normalized = normalizeTermText(token);
    const term = terms.find((item) =>
      normalizeTermText(item.name) === normalized ||
      normalizeTermText(item.slug) === normalized
    );

    if (!term && endpoint === 'tags') {
      const created = createWpTerm(endpoint, token);
      terms.push(created);
      return Number(created.id);
    }

    if (!term) {
      throw new Error(`Không tìm thấy ${endpoint === 'categories' ? 'Category' : 'Tag'}: "${token}". Hãy chọn đúng tên trong tab WP ${endpoint === 'categories' ? 'Categories' : 'Tags'}.`);
    }

    return Number(term.id);
  }).filter((item) => Number.isInteger(item) && item > 0);
}

function getWpTerms(endpoint) {
  const cache = CacheService.getScriptCache();
  const cacheKey = `wp_terms_${endpoint}`;
  const cached = cache.get(cacheKey);
  if (cached) return JSON.parse(cached);

  const props = PropertiesService.getScriptProperties();
  const siteUrl = requiredProp(props, 'WP_SITE_URL').replace(/\/$/, '');
  let page = 1;
  const terms = [];

  while (page <= 10) {
    const response = UrlFetchApp.fetch(
      `${siteUrl}/wp-json/wp/v2/${endpoint}?per_page=100&page=${page}&orderby=name&order=asc`,
      { method: 'get', muteHttpExceptions: true, headers: { Accept: 'application/json' } }
    );

    if (response.getResponseCode() === 400 && page > 1) break;
    if (response.getResponseCode() < 200 || response.getResponseCode() >= 300) {
      throw new Error(`Không đọc được danh sách ${endpoint}: ${response.getContentText()}`);
    }

    const chunk = JSON.parse(response.getContentText() || '[]');
    if (!chunk.length) break;
    terms.push(...chunk.map((item) => ({ id: item.id, name: decodeHtml(item.name), slug: item.slug })));
    if (chunk.length < 100) break;
    page++;
  }

  cache.put(cacheKey, JSON.stringify(terms), 21600);
  return terms;
}

function createWpTerm(endpoint, name) {
  const props = PropertiesService.getScriptProperties();
  const siteUrl = requiredProp(props, 'WP_SITE_URL').replace(/\/$/, '');
  const username = requiredProp(props, 'WP_USERNAME');
  const appPassword = requiredProp(props, 'WP_APP_PASSWORD');
  const token = Utilities.base64Encode(`${username}:${appPassword}`);

  const response = UrlFetchApp.fetch(`${siteUrl}/wp-json/wp/v2/${endpoint}`, {
    method: 'post',
    muteHttpExceptions: true,
    contentType: 'application/json; charset=utf-8',
    headers: {
      Authorization: `Basic ${token}`,
      Accept: 'application/json',
    },
    payload: JSON.stringify({ name }),
  });

  const status = response.getResponseCode();
  const body = response.getContentText();
  let parsed = {};
  try {
    parsed = body ? JSON.parse(body) : {};
  } catch (err) {
    parsed = { raw: body };
  }

  if (status === 400 && parsed && parsed.code === 'term_exists' && parsed.data && parsed.data.term_id) {
    CacheService.getScriptCache().remove(`wp_terms_${endpoint}`);
    return { id: parsed.data.term_id, name, slug: String(name || '').trim().toLowerCase().replace(/\s+/g, '-') };
  }

  if (status < 200 || status >= 300) {
    throw new Error(`Không tạo được ${endpoint === 'tags' ? 'Tag' : 'Category'} "${name}": ${body}`);
  }

  CacheService.getScriptCache().remove(`wp_terms_${endpoint}`);
  return { id: parsed.id, name: decodeHtml(parsed.name || name), slug: parsed.slug || '' };
}

function normalizeTermText(value) {
  return decodeHtml(String(value || ''))
    .trim()
    .toLowerCase()
    .replace(/\s+/g, ' ');
}

function decodeHtml(value) {
  return String(value || '')
    .replace(/&amp;/g, '&')
    .replace(/&lt;/g, '<')
    .replace(/&gt;/g, '>')
    .replace(/&quot;/g, '"')
    .replace(/&#039;/g, "'");
}

function writeResult(sheet, row, wpUrl, postId, publishStatus, error) {
  if (wpUrl) sheet.getRange(row, COL.WP_URL).setValue(wpUrl);
  if (postId) sheet.getRange(row, COL.POST_ID).setValue(postId);
  sheet.getRange(row, COL.PUBLISH_STATUS).setValue(publishStatus);
  sheet.getRange(row, COL.ERROR).setValue(error || '');
  sheet.getRange(row, COL.LAST_RUN).setValue(new Date());
}

function getInputSheet() {
  const sheet = SpreadsheetApp.getActive().getSheetByName(SHEET_NAME);
  if (!sheet) throw new Error(`Không tìm thấy tab "${SHEET_NAME}".`);
  return sheet;
}

function getCell(sheet, row, col) {
  return String(sheet.getRange(row, col).getValue() || '').trim();
}

function addValidation(sheet, col, values) {
  const rows = Math.max(sheet.getMaxRows() - 1, 1);
  const rule = SpreadsheetApp.newDataValidation()
    .requireValueInList(values, true)
    .setAllowInvalid(false)
    .build();
  sheet.getRange(2, col, rows, 1).setDataValidation(rule);
}

function requiredProp(props, key) {
  const value = String(props.getProperty(key) || '').trim();
  if (!value || value.indexOf('YOUR_') === 0) {
    throw new Error(`Chưa cấu hình ${key}. Hãy sửa và chạy setWordPressConfig().`);
  }
  return value;
}
