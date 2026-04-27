# Authentication & Sessions

> Adapted from [VibeSec-Skill](https://github.com/BehiSecc/VibeSec-Skill) (Apache 2.0).

## JWT Security

JWT misconfigurations can lead to full authentication bypass and token forgery.

### Vulnerabilities

| Vulnerability | Prevention |
|---------------|------------|
| `alg: none` attack | Always verify algorithm server-side, reject `none` |
| Algorithm confusion | Explicitly specify expected algorithm, never derive from token |
| Weak HMAC secrets | Use 256+ bit cryptographically random secrets |
| Missing expiration | Always set `exp` claim |
| Token in localStorage | Store in httpOnly, Secure, SameSite=Strict cookies, never localStorage |


### Secure Implementation

```javascript
// 1. SIGNING
// Always use environment variables for secrets
const secret = process.env.JWT_SECRET;

const token = jwt.sign({
  sub: userId,
  iat: Math.floor(Date.now() / 1000),
  exp: Math.floor(Date.now() / 1000) + (15 * 60), // 15 mins (Short-lived)
  jti: crypto.randomUUID() // Unique ID for revocation/blacklisting
}, secret, {
  algorithm: 'HS256'
});

// 2. SENDING (Cookie Best Practices)
// Protect against XSS and CSRF
res.cookie('token', token, {
  httpOnly: true,
  secure: true,
  sameSite: 'strict'
});

// 3. VERIFYING
// CRITICAL: Whitelist the allowed algorithm
jwt.verify(token, secret, { algorithms: ['HS256'] }, (err, decoded) => {
  if (err) {
    // Handle invalid token
  }
  // Trust the payload
});
```

### JWT Checklist

- [ ] Algorithm explicitly specified on verification (never trust token header)
- [ ] `alg: none` rejected
- [ ] Secret is 256+ bits of random data (not a password or phrase)
- [ ] `exp` claim always set and validated
- [ ] Tokens stored in httpOnly cookies (not localStorage/sessionStorage)
- [ ] Refresh token rotation implemented (old refresh token invalidated on use)

---

## PAI Extensions

Cloudflare Workers / D1 / Hono / TypeScript-specific additions beyond VibeSec.

### JWT Attack Vectors (Detailed)

#### alg:none Attack

Attacker modifies JWT header to `{"alg": "none"}` and removes the signature.
Vulnerable libraries accept the token without verification.

```typescript
// VULNERABLE — library accepts alg:none
jwt.verify(token, secret); // No algorithm restriction

// SECURE — explicitly whitelist algorithms
jwt.verify(token, secret, { algorithms: ['HS256'] });
```

#### Algorithm Confusion

Attacker changes algorithm from RS256 to HS256, then signs with the RSA **public key**
(which is publicly available). Server uses public key as HMAC secret.

```typescript
// VULNERABLE — algorithm derived from token header
jwt.verify(token, publicKey); // Attacker uses HS256 with publicKey as secret

// SECURE — explicit algorithm, separate key handling
jwt.verify(token, secret, { algorithms: ['HS256'] }); // HMAC
jwt.verify(token, publicKey, { algorithms: ['RS256'] }); // RSA
```

### Password Storage

#### Recommended Algorithms

| Algorithm | Parameters | Notes |
|-----------|-----------|-------|
| Argon2id | m=65536, t=3, p=4 | Best choice — memory-hard |
| bcrypt | cost=12+ | Good fallback — widely available |
| scrypt | N=2^15, r=8, p=1 | Memory-hard alternative |

**Never use:** MD5, SHA1, SHA256 (plain), or any unsalted hash.

```typescript
// bcrypt example (Node.js)
import bcrypt from 'bcrypt';

const SALT_ROUNDS = 12;
const hash = await bcrypt.hash(password, SALT_ROUNDS);
const isValid = await bcrypt.compare(password, hash);
```

### Timing Attack Prevention

PAI extension — not in VibeSec source.

#### The Problem

String comparison with `===` returns early on first mismatched character.
Attacker measures response time to determine how many characters match.

```typescript
// VULNERABLE — timing leak
function verifyToken(provided: string, stored: string): boolean {
  return provided === stored; // Returns faster for wrong first chars
}

// SECURE — constant-time comparison
import { timingSafeEqual } from 'crypto';

function verifyToken(provided: string, stored: string): boolean {
  if (provided.length !== stored.length) return false;
  return timingSafeEqual(
    Buffer.from(provided),
    Buffer.from(stored)
  );
}
```

#### Where to Use Constant-Time Comparison

- API token verification
- HMAC signature verification
- CSRF token validation
- Webhook signature verification
- Any secret/token comparison

### Token Revocation Patterns

PAI extension — not in VibeSec source.

#### Short-Lived + Refresh Token (D1)

```typescript
// Access token: 15 min, refresh token: 7 days
// On refresh: issue new access token, rotate refresh token
// Store refresh token hash in DB — can revoke by deleting

async function refreshTokens(refreshToken: string, db: D1Database) {
  const hash = await hashToken(refreshToken);
  const stored = await db.prepare(
    'SELECT * FROM refresh_tokens WHERE token_hash = ? AND revoked_at IS NULL'
  ).bind(hash).first();

  if (!stored || isExpired(stored.expires_at)) {
    throw new Error('Invalid refresh token');
  }

  // Rotate: revoke old, issue new
  await db.prepare(
    'UPDATE refresh_tokens SET revoked_at = ? WHERE id = ?'
  ).bind(new Date().toISOString(), stored.id).run();

  const newRefresh = crypto.randomUUID();
  await db.prepare(
    'INSERT INTO refresh_tokens (token_hash, user_id, expires_at) VALUES (?, ?, ?)'
  ).bind(await hashToken(newRefresh), stored.user_id, newExpiry()).run();

  return { accessToken: signJWT(stored.user_id), refreshToken: newRefresh };
}
```

#### Revocation on Account Changes

- Password change: revoke ALL refresh tokens
- Account deletion/deactivation: revoke ALL tokens and sessions
- Role change: revoke ALL tokens (force re-authentication with new claims)
- Suspicious activity: revoke ALL tokens, force re-login
