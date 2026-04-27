---
name: APITesting
description: Declarative API testing and HTTP probing — Hurl for multi-step API workflows with assertions, httpx for concurrent endpoint discovery. USE WHEN API testing, HTTP test, endpoint testing, Hurl, httpx, REST API, API validation, request chaining, batch URL, probe endpoints, API assertions, status code check, hurl file, test API, API smoke test, endpoint probe, bulk URL check, HTTP probing, API workflow test.
---

# APITesting

Two CLI tools for HTTP API testing: **Hurl** for declarative test workflows, **httpx** for fast concurrent probing.

## Tool Selection

```
Multi-step API workflow, assertions, CI/CD   → Hurl
Request chaining, token capture, auth flows  → Hurl
Bulk URL probing, discovery, quick checks    → httpx
Status code scanning, tech detection         → httpx
Single ad-hoc request                        → just use curl
Browser rendering needed                     → Playwright
WebSocket / gRPC                             → specialized tools
Load testing                                 → k6 or artillery
```

## Prerequisites

Before using either tool, verify installation:

```bash
which hurl httpx
```

---

## Hurl — Declarative API Testing

Hurl runs HTTP requests from `.hurl` files — plain text, version-controllable, CI-friendly. Replaces Postman/Insomnia for automated API testing.

### .hurl File Format

```hurl
# Login and capture token
POST http://localhost:3000/api/login
Content-Type: application/json
{"email": "test@example.com", "password": "secret"}
HTTP 200
[Captures]
token: jsonpath "$.token"

# Use token for authenticated request
GET http://localhost:3000/api/profile
Authorization: Bearer {{token}}
HTTP 200
[Asserts]
jsonpath "$.email" == "test@example.com"
jsonpath "$.role" isString
```

Each entry: method + URL, optional headers/body, then expected status and assertions. Entries in the same file run sequentially — captured values carry forward.

### Running Hurl

```bash
# Run a .hurl file
hurl --test api-tests.hurl

# With variables (swap hosts, credentials, etc.)
hurl --variable host=staging.example.com --test api-tests.hurl

# JSON report output
hurl --test --report-json report.json api-tests.hurl

# Run all .hurl files in a directory
hurl --test tests/*.hurl
```

### Common Assertions

```hurl
[Asserts]
jsonpath "$.id" exists
jsonpath "$.count" >= 1
jsonpath "$.items" count == 10
jsonpath "$.status" == "active"
header "Content-Type" contains "application/json"
duration < 2000
```

### When to Use Hurl

- API contract testing in CI/CD pipelines
- Multi-step workflows (login, then authenticated requests)
- Request chaining with token/value capture
- Regression testing for REST APIs
- Smoke tests against staging/production

---

## httpx — Fast HTTP Probing

httpx (by ProjectDiscovery) probes URLs concurrently with rich metadata extraction. Built for discovery and reconnaissance.

### Core Commands

```bash
# Probe single URL with metadata
echo "https://example.com" | httpx -status-code -title -tech-detect

# Batch probe from file
httpx -l urls.txt -status-code -content-length -json -o results.json

# Follow redirects and show chain
echo "http://example.com" | httpx -follow-redirects -location

# Filter by status code
httpx -l urls.txt -mc 200,301 -json
```

### Useful Flags

| Flag | Purpose |
|------|---------|
| `-status-code` | Show HTTP status |
| `-title` | Extract page title |
| `-tech-detect` | Detect technologies (Wappalyzer) |
| `-content-length` | Show response size |
| `-json` | JSON output |
| `-o results.json` | Write output to file |
| `-mc 200,301` | Match specific status codes |
| `-fc 404,500` | Filter out status codes |
| `-follow-redirects` | Follow redirect chains |
| `-location` | Show redirect destination |
| `-l urls.txt` | Read URLs from file |
| `-threads 50` | Concurrency (default 50) |

### When to Use httpx

- Bulk endpoint discovery and validation
- Quick health checks across many URLs
- Technology detection and fingerprinting
- Filtering live hosts from a URL list
- Pre-scan before deeper testing
