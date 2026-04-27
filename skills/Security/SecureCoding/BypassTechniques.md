# Bypass Techniques

> Adapted from [VibeSec-Skill](https://github.com/BehiSecc/VibeSec-Skill) (Apache 2.0).

Consolidated quick-reference of ALL bypass techniques across security domains.
This is VibeSec's highest-value content — 38+ techniques that attackers actually use.

## Open Redirect Bypasses (11 techniques)

| # | Technique | Payload Example | How It Works |
|---|-----------|----------------|--------------|
| 1 | @ symbol | `https://legit.com@evil.com` | Browser treats legit.com as username, navigates to evil.com |
| 2 | Subdomain abuse | `https://legit.com.evil.com` | evil.com owns the subdomain legit.com.evil.com |
| 3 | Protocol tricks | `javascript:alert(1)` | XSS via redirect handler |
| 4 | Double URL encoding | `%252f%252fevil.com` | Decodes to `//evil.com` after double decode |
| 5 | Backslash | `https://legit.com\@evil.com` | Some parsers normalize `\` to `/` |
| 6 | Null byte | `https://legit.com%00.evil.com` | Some parsers truncate at null byte |
| 7 | Tab/newline | `https://legit.com%09.evil.com` | Whitespace confusion in parsers |
| 8 | Unicode normalization | `https://legit.com` (Cyrillic chars) | IDN homograph attack |
| 9 | Data URLs | `data:text/html,<script>...</script>` | Direct payload execution |
| 10 | Protocol-relative | `//evil.com` | Uses current page's protocol |
| 11 | Fragment abuse | `https://legit.com#@evil.com` | Parsed differently by different libraries |

### IDN Homograph Attack Protection

- Convert URLs to Punycode before validation
- Consider blocking non-ASCII domains entirely for sensitive redirects

### Defense

- Allowlist valid redirect domains
- Parse URL, validate hostname matches allowlist
- Convert to Punycode before validation (block IDN homographs)
- Use relative paths only when possible, validate no `//` or `\`

## SSRF IP Bypasses (12 techniques)

| # | Technique | Payload Example | How It Works |
|---|-----------|----------------|--------------|
| 1 | Decimal IP | `http://2130706433` | 127.0.0.1 as single decimal |
| 2 | Octal IP | `http://0177.0.0.1` | Octal representation of 127 |
| 3 | Hex IP | `http://0x7f.0x0.0x0.0x1` | Hexadecimal octets |
| 4 | IPv6 localhost | `http://[::1]` | IPv6 loopback address |
| 5 | IPv6 mapped IPv4 | `http://[::ffff:127.0.0.1]` | IPv4-mapped IPv6 address |
| 6 | Short IPv6 | `http://[::]` | All-zeros IPv6 (binds to 0.0.0.0) |
| 7 | DNS rebinding | Attacker DNS alternates IPs | First resolve: external. Second: internal |
| 8 | CNAME to internal | Attacker domain CNAMEs to internal | DNS points to internal hostname |
| 9 | URL parser confusion | `http://attacker.com#@internal` | Different parsing by different libraries |
| 10 | Redirect chains | External URL 302s to internal | Follow redirect reaches internal network |
| 11 | IPv6 scope ID | `http://[fe80::1%25eth0]` | Interface-scoped IPv6 |
| 12 | Rare IP formats | `http://127.1` | Shortened IP notation |

### DNS Rebinding Prevention

1. Resolve DNS before making request
2. Validate resolved IP is not internal
3. Pin the resolved IP for the request (don't re-resolve)
4. Or: Resolve twice with delay, ensure both resolve to same external IP

### Cloud Metadata Endpoints to Block

| Provider | Endpoint |
|----------|----------|
| AWS | `169.254.169.254` |
| GCP | `metadata.google.internal`, `169.254.169.254`, `http://metadata` |
| Azure | `169.254.169.254` |
| DigitalOcean | `169.254.169.254` |

### Defense

- Resolve DNS before making request, validate resolved IP is external
- Pin resolved IP (don't re-resolve — prevents DNS rebinding)
- Block all private ranges: `10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16`, `127.0.0.0/8`
- Block metadata IPs: `169.254.169.254`
- Disable or validate each redirect hop
- Use allowlist for known-good domains

## CSRF Bypasses (8 techniques)

| # | Technique | How It Works |
|---|-----------|--------------|
| 1 | Missing token = skip validation | Server only validates token IF present — omit it entirely |
| 2 | Subdomain CSRF | Subdomain takeover allows setting cookies for parent domain |
| 3 | GET with side effects | State changes on GET bypass SameSite=Lax (sent on navigations) |
| 4 | Flash/PDF plugin abuse | Legacy browser plugins bypass SameSite restrictions |
| 5 | Content-type tricks | JSON APIs assume Content-Type check prevents CSRF — forms can send `text/plain` |
| 6 | CORS misconfiguration | Overly permissive CORS (`Access-Control-Allow-Origin: *`) with credentials |
| 7 | Token in URL | CSRF token leaks via Referer header to third-party resources |
| 8 | Token not tied to session | Stolen/leaked token from one session reusable in another |

### Defense

- ALWAYS require CSRF token (reject if absent, not just if invalid)
- Tie token to user session
- Use SameSite=Strict cookies + CSRF tokens (defense in depth)
- Never perform state changes on GET requests
- Validate Origin/Referer headers as additional check
- Regenerate token on login/auth state change

## File Upload Bypasses (11 techniques)

| # | Technique | Payload Example | How It Works |
|---|-----------|----------------|--------------|
| 1 | Extension bypass | `shell.php.jpg` | Server checks last extension only |
| 2 | Null byte | `shell.php%00.jpg` | Null terminates filename at .php |
| 3 | Double extension | `shell.jpg.php` | Server executes based on last extension |
| 4 | MIME type spoofing | Content-Type: `image/jpeg` | Server trusts client-provided MIME type |
| 5 | Magic byte injection | Valid JPEG header + PHP code | Passes header-only magic byte check |
| 6 | Polyglot files | Valid as both JPEG and JS | File serves as image AND executes as code |
| 7 | SVG with JavaScript | `<svg onload="alert(1)">` | SVG is XML, supports event handlers |
| 8 | XXE via file upload | Malicious DOCX/XLSX (XML-based) | Office formats are ZIP with XML inside |
| 9 | ZIP slip | `../../../etc/passwd` in archive | Path traversal during extraction |
| 10 | Filename injection | `; rm -rf /` as filename | Command injection via unsanitized name |
| 11 | Content-type confusion | Browser MIME sniffs actual content | Ignores declared Content-Type |

### Magic Bytes Reference

| Type | Magic Bytes (hex) |
|------|-------------------|
| JPEG | `FF D8 FF` |
| PNG | `89 50 4E 47 0D 0A 1A 0A` |
| GIF | `47 49 46 38` |
| PDF | `25 50 44 46` |
| ZIP | `50 4B 03 04` |
| DOCX/XLSX | `50 4B 03 04` (ZIP-based) |

### Defense

- Check extension against allowlist (not blocklist)
- Validate magic bytes match declared type (check full structure, not just header)
- Rename to random UUID (discard original filename entirely)
- Store outside webroot or on separate domain (CDN/R2)
- Serve with `Content-Disposition: attachment` and `X-Content-Type-Options: nosniff`
- Set non-executable permissions on uploaded files
- Sanitize or reject SVG files (strip scripts)
- Validate archive entry paths for traversal (ZIP slip)

## Quick Decision Matrix

| "I'm building..." | Check These Bypass Tables |
|-------------------|--------------------------|
| Redirect/login flow | Open Redirect (11) |
| Webhook/URL fetch | SSRF (12) |
| Form submission | CSRF (8) |
| File upload | File Upload (11) |
| Any auth endpoint | CSRF (8) + relevant domain |
| URL parsing | Open Redirect (11) + SSRF (12) |
