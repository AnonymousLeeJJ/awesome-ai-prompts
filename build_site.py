# -*- coding: utf-8 -*-
"""Build docs/index.html by inlining prompts.json so the site works on GitHub Pages and file://."""
import json, pathlib

root = pathlib.Path(__file__).parent
data = json.loads((root / "prompts.json").read_text(encoding="utf-8"))
docs = root / "docs"
docs.mkdir(exist_ok=True)

html = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Awesome AI Prompts - 高质量中文 AI 提示词库</title>
<meta name="description" content="精心筛选的高质量 AI 提示词库，每一条都经过实战打磨，即复制即用">
<style>
  :root {
    --bg: #f7f8fa; --card: #ffffff; --text: #1f2328; --muted: #656d76;
    --accent: #4f6ef7; --accent-soft: #eef1fe; --border: #e3e6ea; --radius: 14px;
  }
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body { font-family: -apple-system, "PingFang SC", "Microsoft YaHei", "Segoe UI", sans-serif;
         background: var(--bg); color: var(--text); line-height: 1.6; }
  .wrap { max-width: 1080px; margin: 0 auto; padding: 0 20px; }
  header.hero { text-align: center; padding: 64px 20px 36px; }
  header.hero h1 { font-size: 2.4rem; letter-spacing: -0.5px; }
  header.hero h1 .emoji { margin-right: 8px; }
  header.hero p.sub { color: var(--muted); margin-top: 12px; font-size: 1.05rem; }
  .stats { margin-top: 18px; display: flex; gap: 24px; justify-content: center; flex-wrap: wrap; }
  .stat { background: var(--card); border: 1px solid var(--border); border-radius: 999px;
          padding: 6px 18px; font-size: 0.9rem; color: var(--muted); }
  .stat b { color: var(--accent); }
  .toolbar { position: sticky; top: 0; z-index: 10; background: rgba(247,248,250,0.92);
             backdrop-filter: blur(8px); padding: 14px 0 10px; border-bottom: 1px solid var(--border); }
  .search { width: 100%; padding: 12px 18px; border: 1px solid var(--border); border-radius: 999px;
            font-size: 1rem; background: var(--card); outline: none; transition: border-color .15s; }
  .search:focus { border-color: var(--accent); }
  .chips { display: flex; gap: 8px; flex-wrap: wrap; margin-top: 12px; }
  .chip { padding: 5px 14px; border-radius: 999px; border: 1px solid var(--border);
          background: var(--card); cursor: pointer; font-size: 0.88rem; color: var(--muted);
          transition: all .15s; user-select: none; }
  .chip:hover { border-color: var(--accent); color: var(--accent); }
  .chip.active { background: var(--accent); border-color: var(--accent); color: #fff; }
  main { padding: 28px 0 60px; }
  .cat-title { display: flex; align-items: baseline; gap: 10px; margin: 30px 0 14px; }
  .cat-title h2 { font-size: 1.25rem; }
  .cat-title span { color: var(--muted); font-size: 0.85rem; }
  .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); gap: 14px; }
  .card { background: var(--card); border: 1px solid var(--border); border-radius: var(--radius);
          padding: 18px 20px; cursor: pointer; transition: transform .15s, box-shadow .15s; }
  .card:hover { transform: translateY(-2px); box-shadow: 0 6px 20px rgba(31,35,40,0.08); }
  .card h3 { font-size: 1.02rem; margin-bottom: 6px; }
  .card p { color: var(--muted); font-size: 0.88rem; }
  .card .tags { margin-top: 10px; display: flex; gap: 6px; flex-wrap: wrap; }
  .tag { font-size: 0.75rem; background: var(--accent-soft); color: var(--accent);
         border-radius: 6px; padding: 2px 8px; }
  dialog { border: none; border-radius: 18px; max-width: 720px; width: calc(100% - 40px);
           padding: 0; box-shadow: 0 20px 60px rgba(0,0,0,0.25); }
  dialog::backdrop { background: rgba(31,35,40,0.45); backdrop-filter: blur(3px); }
  .modal-head { padding: 22px 26px 0; }
  .modal-head h3 { font-size: 1.3rem; }
  .modal-head .desc { color: var(--muted); margin-top: 4px; font-size: 0.92rem; }
  .modal-body { padding: 16px 26px 26px; }
  .prompt-box { background: #f0f2f5; border-radius: 12px; padding: 16px 18px;
                white-space: pre-wrap; font-size: 0.9rem; line-height: 1.7;
                max-height: 50vh; overflow-y: auto; font-family: "SF Mono", Consolas, monospace; }
  .modal-actions { display: flex; gap: 10px; margin-top: 16px; }
  .btn { flex: 1; padding: 11px; border-radius: 10px; border: 1px solid var(--border);
         background: var(--card); cursor: pointer; font-size: 0.95rem; transition: all .15s; }
  .btn.primary { background: var(--accent); color: #fff; border-color: var(--accent); }
  .btn.primary:hover { filter: brightness(1.08); }
  .btn:hover { border-color: var(--accent); color: var(--accent); }
  .btn.primary:hover { color: #fff; }
  footer { text-align: center; padding: 36px 20px 48px; color: var(--muted); font-size: 0.88rem; }
  footer a { color: var(--accent); text-decoration: none; }
  .empty { text-align: center; color: var(--muted); padding: 60px 0; }
  .toast { position: fixed; left: 50%; bottom: 32px; transform: translateX(-50%);
           background: #1f2328; color: #fff; padding: 10px 22px; border-radius: 999px;
           font-size: 0.9rem; opacity: 0; transition: opacity .25s; pointer-events: none; z-index: 99; }
  .toast.show { opacity: 1; }
  @media (max-width: 600px) { header.hero h1 { font-size: 1.8rem; } }
</style>
</head>
<body>
<header class="hero">
  <h1><span class="emoji">🎯</span>Awesome AI Prompts</h1>
  <p class="sub">精心筛选的高质量中文 AI 提示词库 · 每一条都经过实战打磨 · 即复制即用</p>
  <div class="stats">
    <div class="stat"><b id="statPrompts">0</b> 条提示词</div>
    <div class="stat"><b id="statCats">0</b> 个分类</div>
    <div class="stat">CC0 协议 · 随意使用</div>
  </div>
</header>

<div class="toolbar">
  <div class="wrap">
    <input class="search" id="search" type="search" placeholder="🔍 搜索提示词，如：周报、代码、面试…">
    <div class="chips" id="chips"></div>
  </div>
</div>

<main class="wrap" id="main"></main>

<dialog id="modal">
  <div class="modal-head"><h3 id="mTitle"></h3><p class="desc" id="mDesc"></p></div>
  <div class="modal-body">
    <div class="prompt-box" id="mPrompt"></div>
    <div class="modal-actions">
      <button class="btn primary" id="copyBtn">📋 复制提示词</button>
      <button class="btn" id="closeBtn">关闭</button>
    </div>
  </div>
</dialog>

<div class="toast" id="toast">已复制到剪贴板 ✅</div>

<footer>
  <p>用 ❤️ 维护 · <a href="https://github.com/YOUR_USERNAME/awesome-ai-prompts" target="_blank" rel="noopener">GitHub 仓库</a> · 欢迎 Star ⭐ 与投稿</p>
</footer>

<script id="prompts-data" type="application/json">__DATA__</script>
<script>
const DATA = JSON.parse(document.getElementById('prompts-data').textContent);
const { categories, prompts } = DATA;
const state = { q: '', cat: 'all' };

document.getElementById('statPrompts').textContent = prompts.length;
document.getElementById('statCats').textContent = categories.length;

const chipsEl = document.getElementById('chips');
const mainEl = document.getElementById('main');
const modal = document.getElementById('modal');
const toast = document.getElementById('toast');
let currentPrompt = '';

function renderChips() {
  const all = [{ id: 'all', name: '全部', icon: '✨' }, ...categories];
  chipsEl.innerHTML = all.map(c =>
    `<span class="chip ${state.cat === c.id ? 'active' : ''}" data-id="${c.id}">${c.icon || ''} ${c.name}</span>`
  ).join('');
  chipsEl.querySelectorAll('.chip').forEach(el =>
    el.addEventListener('click', () => { state.cat = el.dataset.id; renderChips(); renderList(); }));
}

function matches(p) {
  if (state.cat !== 'all' && p.category !== state.cat) return false;
  if (!state.q) return true;
  const q = state.q.toLowerCase();
  return (p.title + p.titleEn + p.description + p.prompt + p.tags.join(' ')).toLowerCase().includes(q);
}

function renderList() {
  const groups = categories
    .map(c => ({ cat: c, items: prompts.filter(p => p.category === c.id && matches(p)) }))
    .filter(g => g.items.length);
  if (!groups.length) {
    mainEl.innerHTML = '<div class="empty">没有找到匹配的提示词，换个关键词试试 🧐</div>';
    return;
  }
  mainEl.innerHTML = groups.map(g => `
    <div class="cat-title"><h2>${g.cat.icon} ${g.cat.name}</h2><span>${g.items.length} 条</span></div>
    <div class="grid">${g.items.map(p => `
      <div class="card" data-id="${p.id}">
        <h3>${p.title}</h3>
        <p>${p.description}</p>
        <div class="tags">${p.tags.map(t => `<span class="tag">${t}</span>`).join('')}</div>
      </div>`).join('')}
    </div>`).join('');
  mainEl.querySelectorAll('.card').forEach(el =>
    el.addEventListener('click', () => openModal(+el.dataset.id)));
}

function openModal(id) {
  const p = prompts.find(x => x.id === id);
  if (!p) return;
  currentPrompt = p.prompt;
  document.getElementById('mTitle').textContent = p.title + ' · ' + p.titleEn;
  document.getElementById('mDesc').textContent = p.description;
  document.getElementById('mPrompt').textContent = p.prompt;
  modal.showModal();
}

document.getElementById('copyBtn').addEventListener('click', async () => {
  try { await navigator.clipboard.writeText(currentPrompt); }
  catch {
    const ta = document.createElement('textarea');
    ta.value = currentPrompt; document.body.appendChild(ta);
    ta.select(); document.execCommand('copy'); ta.remove();
  }
  toast.classList.add('show');
  setTimeout(() => toast.classList.remove('show'), 1600);
});
document.getElementById('closeBtn').addEventListener('click', () => modal.close());
modal.addEventListener('click', e => { if (e.target === modal) modal.close(); });
document.getElementById('search').addEventListener('input', e => { state.q = e.target.value.trim(); renderList(); });

renderChips();
renderList();
</script>
</body>
</html>
"""

html = html.replace("__DATA__", json.dumps(data, ensure_ascii=False))
(docs / "index.html").write_text(html, encoding="utf-8")
print("OK ->", docs / "index.html", f"({len(data['prompts'])} prompts)")
