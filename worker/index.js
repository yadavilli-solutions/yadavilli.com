/**
 * Password gate for /insights/*.
 *
 * Everything else is served straight from the static asset bundle. Only the
 * paths listed under `assets.run_worker_first` in wrangler.jsonc reach this
 * script, so the public pages keep their edge-cache behaviour untouched.
 *
 * Secrets (set with `npx wrangler secret put <NAME>`):
 *   INSIGHTS_PASSWORD       shared password readers type in
 *   INSIGHTS_COOKIE_SECRET  HMAC key for the session cookie (any long random string)
 */

const COOKIE_NAME = 'ys_insights';
const COOKIE_PATH = '/insights';
const SESSION_TTL = 60 * 60 * 24 * 30; // 30 days
const GATED = /^\/insights(\/|$)/;

export default {
  async fetch(request, env) {
    const url = new URL(request.url);

    if (!GATED.test(url.pathname)) {
      return env.ASSETS.fetch(request);
    }

    if (!env.INSIGHTS_PASSWORD || !env.INSIGHTS_COOKIE_SECRET) {
      // Fail closed: a missing secret must never expose the section.
      return gatedResponse('Insights is temporarily unavailable.', 503);
    }

    if (url.pathname === '/insights/logout') {
      const res = redirect('/');
      res.headers.append('Set-Cookie', expireCookie());
      return res;
    }

    if (request.method === 'POST') {
      return handleLogin(request, env, url);
    }

    if (request.method !== 'GET' && request.method !== 'HEAD') {
      return gatedResponse('Method not allowed.', 405);
    }

    if (await hasValidSession(request, env)) {
      return withGateHeaders(await env.ASSETS.fetch(request));
    }

    return loginPage(url.pathname + url.search, null, 401);
  },
};

async function handleLogin(request, env, url) {
  const form = await request.formData().catch(() => null);
  if (!form) return loginPage(url.pathname, 'Something went wrong. Try again.', 400);

  const submitted = String(form.get('password') || '');
  const target = safeTarget(String(form.get('next') || url.pathname));

  if (!timingSafeEqual(submitted, env.INSIGHTS_PASSWORD)) {
    return loginPage(target, 'That password is not right.', 401);
  }

  const res = redirect(target);
  res.headers.append('Set-Cookie', await sessionCookie(env));
  return res;
}

/* ---------------------------------------------------------------- session */

async function sessionCookie(env) {
  const expires = Math.floor(Date.now() / 1000) + SESSION_TTL;
  const value = `${expires}.${await sign(String(expires), env.INSIGHTS_COOKIE_SECRET)}`;
  return `${COOKIE_NAME}=${value}; Path=${COOKIE_PATH}; Max-Age=${SESSION_TTL}; HttpOnly; Secure; SameSite=Lax`;
}

function expireCookie() {
  return `${COOKIE_NAME}=; Path=${COOKIE_PATH}; Max-Age=0; HttpOnly; Secure; SameSite=Lax`;
}

async function hasValidSession(request, env) {
  const raw = readCookie(request.headers.get('Cookie'), COOKIE_NAME);
  if (!raw) return false;

  const [expires, signature] = raw.split('.');
  if (!expires || !signature) return false;
  if (!/^\d+$/.test(expires) || Number(expires) < Math.floor(Date.now() / 1000)) return false;

  return timingSafeEqual(signature, await sign(expires, env.INSIGHTS_COOKIE_SECRET));
}

async function sign(payload, secret) {
  const key = await crypto.subtle.importKey(
    'raw',
    new TextEncoder().encode(secret),
    { name: 'HMAC', hash: 'SHA-256' },
    false,
    ['sign'],
  );
  const mac = await crypto.subtle.sign('HMAC', key, new TextEncoder().encode(payload));
  return [...new Uint8Array(mac)].map((b) => b.toString(16).padStart(2, '0')).join('');
}

function timingSafeEqual(a, b) {
  const left = new TextEncoder().encode(a);
  const right = new TextEncoder().encode(b);
  // Compare a fixed-length digest of both sides so length alone leaks nothing.
  let diff = left.length ^ right.length;
  for (let i = 0; i < Math.max(left.length, right.length); i++) {
    diff |= (left[i] ?? 0) ^ (right[i] ?? 0);
  }
  return diff === 0;
}

function readCookie(header, name) {
  if (!header) return null;
  for (const part of header.split(';')) {
    const [key, ...rest] = part.trim().split('=');
    if (key === name) return rest.join('=');
  }
  return null;
}

/* --------------------------------------------------------------- responses */

function safeTarget(candidate) {
  // Only ever redirect back inside the gated section.
  return GATED.test(candidate) && !candidate.startsWith('//') ? candidate : '/insights/';
}

function gateHeaders(extra = {}) {
  return {
    'Cache-Control': 'private, no-store',
    'X-Robots-Tag': 'noindex, nofollow',
    ...extra,
  };
}

function withGateHeaders(response) {
  const res = new Response(response.body, response);
  for (const [key, value] of Object.entries(gateHeaders())) res.headers.set(key, value);
  return res;
}

function redirect(location) {
  return new Response(null, {
    status: 303,
    headers: gateHeaders({ Location: location }),
  });
}

function gatedResponse(message, status) {
  return new Response(message, {
    status,
    headers: gateHeaders({ 'Content-Type': 'text/plain; charset=utf-8' }),
  });
}

function loginPage(next, error, status) {
  return new Response(renderLogin(next, error), {
    status,
    headers: gateHeaders({ 'Content-Type': 'text/html; charset=utf-8' }),
  });
}

function escapeHtml(value) {
  return value.replace(/[&<>"']/g, (c) => ({
    '&': '&amp;',
    '<': '&lt;',
    '>': '&gt;',
    '"': '&quot;',
    "'": '&#39;',
  })[c]);
}

function renderLogin(next, error) {
  return `<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>Insights | Yadavilli Solutions</title>
<link rel="icon" href="/img/favicon.ico" sizes="any">
<meta name="theme-color" content="#02023e">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Amethysta&family=Questrial&display=swap" rel="stylesheet">
<style>
  :root {
    --brand-cyan: #08c7d6;
    --brand-navy: #02023e;
    --text-2: #a5aec9;
  }
  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    min-height: 100vh;
    display: grid;
    place-items: center;
    padding: 2rem 1.5rem;
    background:
      radial-gradient(90rem 60rem at -10% -10%, rgba(8,199,214,0.22) 0%, rgba(8,199,214,0) 60%),
      var(--brand-navy);
    color: #fff;
    font-family: 'Inter', system-ui, sans-serif;
    line-height: 1.6;
    -webkit-font-smoothing: antialiased;
  }
  .card {
    width: 100%;
    max-width: 27rem;
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.10);
    border-radius: 16px;
    padding: 2.5rem 2rem;
    box-shadow: 0 4px 40px rgba(0,0,0,0.35);
    text-align: center;
  }
  a { color: inherit; text-decoration: none; }
  .logo { display: inline-flex; align-items: center; gap: 0.7rem; margin-bottom: 1.75rem; }
  .logo-mark {
    width: 40px; height: 40px; border-radius: 8px;
    display: grid; place-items: center;
    background: linear-gradient(120deg, var(--brand-cyan), var(--brand-navy));
    font-family: 'Amethysta', Georgia, serif; font-size: 1.35rem; line-height: 1;
  }
  .logo-text { display: block; font-family: 'Amethysta', Georgia, serif; font-size: 1.35rem; line-height: 1; white-space: nowrap; }
  .logo-slogan {
    display: block;
    font-family: 'Questrial', system-ui, sans-serif;
    font-size: 0.56rem; letter-spacing: 0.3em; text-transform: uppercase;
    color: var(--text-2); margin-top: 0.3rem; white-space: nowrap;
  }
  .logo-lockup { text-align: left; }
  h1 { font-size: 1.35rem; font-weight: 700; margin-bottom: 0.5rem; }
  p.lede { color: var(--text-2); font-size: 0.95rem; margin-bottom: 1.5rem; }
  label { display: block; text-align: left; font-size: 0.8rem; font-weight: 600; color: var(--text-2); margin-bottom: 0.4rem; }
  input {
    width: 100%; padding: 0.8rem 1rem; font-size: 1rem; font-family: inherit;
    color: #fff; background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.14); border-radius: 10px;
  }
  input:focus { outline: none; border-color: var(--brand-cyan); box-shadow: 0 0 0 3px rgba(8,199,214,0.18); }
  button {
    width: 100%; margin-top: 1rem; padding: 0.85rem 1.5rem; cursor: pointer;
    font-family: inherit; font-size: 0.95rem; font-weight: 700;
    color: var(--brand-navy); background: linear-gradient(135deg, var(--brand-cyan), #0592b5);
    border: none; border-radius: 100px; transition: transform 0.2s ease, box-shadow 0.2s ease;
  }
  button:hover { transform: translateY(-1px); box-shadow: 0 4px 20px rgba(8,199,214,0.35); }
  .error {
    margin-bottom: 1rem; padding: 0.6rem 0.9rem; border-radius: 10px; font-size: 0.85rem;
    color: #ffd7d7; background: rgba(220,38,38,0.14); border: 1px solid rgba(220,38,38,0.35);
  }
  .back { display: inline-block; margin-top: 1.5rem; font-size: 0.85rem; color: var(--text-2); text-decoration: none; }
  .back:hover { color: #fff; }
</style>
</head>
<body>
  <main class="card">
    <a class="logo" href="/">
      <span class="logo-mark" aria-hidden="true">Y</span>
      <span class="logo-lockup">
        <span class="logo-text">Yadavilli Solutions</span>
        <span class="logo-slogan">Solutions Delivered</span>
      </span>
    </a>
    <h1>Insights is private</h1>
    <p class="lede">Enter the access password to read our research and analysis.</p>
    ${error ? `<p class="error">${escapeHtml(error)}</p>` : ''}
    <form method="POST" action="${escapeHtml(next)}">
      <input type="hidden" name="next" value="${escapeHtml(next)}">
      <label for="password">Password</label>
      <input id="password" name="password" type="password" autocomplete="current-password" autofocus required>
      <button type="submit">Unlock Insights</button>
    </form>
    <a class="back" href="/">&larr; Back to yadavilli.com</a>
  </main>
</body>
</html>`;
}
