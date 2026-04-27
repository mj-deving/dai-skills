# API Security

> Adapted from [VibeSec-Skill](https://github.com/BehiSecc/VibeSec-Skill) (Apache 2.0).

## Mass Assignment

Accepting unfiltered request bodies can lead to privilege escalation.

```javascript
// VULNERABLE — user can set { role: "admin" } in request body
User.update(req.body)

// SECURE — whitelist allowed fields
const allowed = ['name', 'email', 'avatar']
const updates = pick(req.body, allowed)
User.update(updates)
```

This applies to any ORM/framework — always explicitly define which fields a request can modify.

## GraphQL

| Vulnerability | Prevention |
| :--- | :--- |
| Introspection in production | Disable introspection in production environments. |
| Query depth attack | Implement query depth limiting (e.g., maximum of 10 levels). |
| Query complexity attack | Calculate and enforce strict query cost limits. |
| Batching attack | Limit the number of operations allowed per single request. |


```javascript
const server = new ApolloServer({
  introspection: process.env.NODE_ENV !== 'production',
  validationRules: [
    depthLimit(10),
    costAnalysis({ maximumCost: 1000 })
  ]
})
```

## Security Headers Checklist

Include these headers in all responses:

```
Strict-Transport-Security: max-age=31536000; includeSubDomains; preload
Content-Security-Policy: [see XSS section]
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
Referrer-Policy: strict-origin-when-cross-origin
Cache-Control: no-store (for sensitive pages)
```

## General Security Principles

When generating code, always:

1. **Validate all input server-side** — Never trust client-side validation alone
2. **Use parameterized queries** — Never concatenate user input into queries
3. **Encode output contextually** — HTML, JS, URL, CSS contexts need different encoding
4. **Apply authentication checks** — On every endpoint, not just at routing
5. **Apply authorization checks** — Verify the user can access the specific resource
6. **Use secure defaults**
7. **Handle errors securely** — Don't leak stack traces or internal details to users
8. **Keep dependencies updated** — Use tools to track vulnerable dependencies

When unsure, choose the more restrictive/secure option and document the security consideration in comments.

---

## PAI Extensions

Cloudflare Workers / D1 / Hono / TypeScript-specific additions beyond VibeSec.

### Mass Assignment Prevention (Hono/TypeScript)

```typescript
// VULNERABLE — user can set { role: "admin", balance: 999999 }
app.patch('/api/users/:id', async (c) => {
  const body = await c.req.json();
  await c.env.DB.prepare('UPDATE users SET ? WHERE id = ?')
    .bind(body, c.req.param('id')).run(); // Accepts ANY field
});

// SECURE — explicit allowlist
const ALLOWED_USER_FIELDS = ['name', 'email', 'avatar'] as const;

function pickAllowed<T extends Record<string, unknown>>(
  body: T,
  allowed: readonly string[]
): Partial<T> {
  const result: Record<string, unknown> = {};
  for (const key of allowed) {
    if (key in body) result[key] = body[key];
  }
  return result as Partial<T>;
}

app.patch('/api/users/:id', async (c) => {
  const body = await c.req.json();
  const updates = pickAllowed(body, ALLOWED_USER_FIELDS);
  // updates will never contain 'role', 'isAdmin', 'balance'
});
```

### Security Headers (Hono Middleware for Workers)

```typescript
app.use('*', async (c, next) => {
  await next();
  c.header('Strict-Transport-Security', 'max-age=31536000; includeSubDomains; preload');
  c.header('X-Content-Type-Options', 'nosniff');
  c.header('X-Frame-Options', 'DENY');
  c.header('Referrer-Policy', 'strict-origin-when-cross-origin');
  // CSP — customize per app
  c.header('Content-Security-Policy', "default-src 'self'; frame-ancestors 'none'");
  // For sensitive pages:
  // c.header('Cache-Control', 'no-store');
});
```

| Header | Value | Purpose |
|--------|-------|---------|
| `Strict-Transport-Security` | `max-age=31536000; includeSubDomains; preload` | Force HTTPS |
| `X-Content-Type-Options` | `nosniff` | Prevent MIME sniffing |
| `X-Frame-Options` | `DENY` | Prevent clickjacking |
| `Referrer-Policy` | `strict-origin-when-cross-origin` | Limit referrer leakage |
| `Content-Security-Policy` | See ClientSide.md | Prevent XSS |
| `Cache-Control` | `no-store` | Sensitive pages only |

### Rate Limiting (Cloudflare Workers KV)

PAI extension — not in VibeSec source.

```typescript
// Rate limiting using KV with sliding window
async function checkRateLimit(
  kv: KVNamespace,
  key: string, // e.g., `ratelimit:${ip}:${endpoint}`
  limit: number,
  windowSeconds: number
): Promise<{ allowed: boolean; remaining: number }> {
  const now = Math.floor(Date.now() / 1000);
  const windowKey = `${key}:${Math.floor(now / windowSeconds)}`;

  const current = parseInt(await kv.get(windowKey) || '0');

  if (current >= limit) {
    return { allowed: false, remaining: 0 };
  }

  await kv.put(windowKey, String(current + 1), {
    expirationTtl: windowSeconds * 2, // Auto-cleanup
  });

  return { allowed: true, remaining: limit - current - 1 };
}

// Usage in Hono middleware
app.use('/api/auth/*', async (c, next) => {
  const ip = c.req.header('CF-Connecting-IP') || 'unknown';
  const { allowed, remaining } = await checkRateLimit(
    c.env.CACHE, `ratelimit:${ip}:auth`, 10, 60 // 10 req/min
  );

  if (!allowed) {
    c.header('Retry-After', '60');
    return c.json({ error: 'Rate limit exceeded' }, 429);
  }

  c.header('X-RateLimit-Remaining', String(remaining));
  await next();
});
```

### Rate Limit Recommendations

| Endpoint Type | Limit | Window |
|--------------|-------|--------|
| Login/auth | 10 req | 1 min |
| API (authenticated) | 100 req | 1 min |
| API (unauthenticated) | 30 req | 1 min |
| Password reset | 3 req | 15 min |
| File upload | 10 req | 5 min |
