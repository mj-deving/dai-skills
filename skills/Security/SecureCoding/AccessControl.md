# Access Control

> Adapted from [VibeSec-Skill](https://github.com/BehiSecc/VibeSec-Skill) (Apache 2.0).

Access control vulnerabilities occur when users can access resources or perform actions beyond their intended permissions.

### Core Requirements

For **every data point and action** that requires authentication:

1. **User-Level Authorization**
   - Each user must only access/modify their own data
   - No user should access data from other users or organizations
   - Always verify ownership at the data layer, not just the route level

2. **Use UUIDs Instead of Sequential IDs**
   - Use UUIDv4 or similar non-guessable identifiers
   - Exception: Only use sequential IDs if explicitly requested by user

3. **Account Lifecycle Handling**
   - When a user is removed from an organization: immediately revoke all access tokens and sessions
   - When an account is deleted/deactivated: invalidate all active sessions and API keys
   - Implement token revocation lists or short-lived tokens with refresh mechanisms

### Authorization Checks Checklist

- [ ] Verify user owns the resource on every request (don't trust client-side data)
- [ ] Check organization membership for multi-tenant apps
- [ ] Validate role permissions for role-based actions
- [ ] Re-validate permissions after any privilege change
- [ ] Check parent resource ownership (e.g., if accessing a comment, verify user owns the parent post)

### Common Pitfalls to Avoid

- **IDOR (Insecure Direct Object Reference)**: Always verify the requesting user has permission to access the requested resource ID
- **Privilege Escalation**: Validate role changes server-side; never trust role info from client
- **Horizontal Access**: User A accessing User B's resources with the same privilege level
- **Vertical Access**: Regular user accessing admin functionality
- **Mass Assignment**: Filter which fields users can update; don't blindly accept all request body fields

### Implementation Pattern

```
# Pseudocode for secure resource access
function getResource(resourceId, currentUser):
    resource = database.find(resourceId)

    if resource is null:
        return 404  # Don't reveal if resource exists

    if resource.ownerId != currentUser.id:
        if not currentUser.hasOrgAccess(resource.orgId):
            return 404  # Return 404, not 403, to prevent enumeration

    return resource
```

---

## PAI Extensions

Cloudflare Workers / D1 / Hono / TypeScript-specific additions beyond VibeSec.

### Hono Middleware — Resource Ownership (Cloudflare Workers)

```typescript
// Middleware: verify resource ownership before handler
const requireOwnership = async (c: Context, next: Next) => {
  const userId = c.get('userId'); // from auth middleware
  const resourceId = c.req.param('id');

  const resource = await c.env.DB.prepare(
    'SELECT owner_id FROM resources WHERE id = ?'
  ).bind(resourceId).first();

  if (!resource) return c.json({ error: 'Not found' }, 404);
  if (resource.owner_id !== userId) return c.json({ error: 'Not found' }, 404); // 404, not 403

  await next();
};
```

### D1 Row-Level Tenant Isolation

```typescript
// Always include tenant_id in WHERE clauses
const items = await c.env.DB.prepare(
  'SELECT * FROM items WHERE tenant_id = ? AND id = ?'
).bind(tenantId, itemId).all();

// Never: SELECT * FROM items WHERE id = ? (missing tenant filter)
```

### Mass Assignment Prevention (TypeScript)

```typescript
// Whitelist allowed fields explicitly
const ALLOWED_UPDATE_FIELDS = ['name', 'email', 'avatar'] as const;

function sanitizeUpdate(body: Record<string, unknown>) {
  const sanitized: Record<string, unknown> = {};
  for (const field of ALLOWED_UPDATE_FIELDS) {
    if (field in body) sanitized[field] = body[field];
  }
  return sanitized;
}

// Usage in Hono route
app.patch('/api/users/:id', async (c) => {
  const updates = sanitizeUpdate(await c.req.json());
  // updates will never contain 'role', 'isAdmin', etc.
});
```

### Account Lifecycle — Token Revocation (D1)

```typescript
// When user is removed from org, revoke all tokens
async function revokeUserAccess(db: D1Database, userId: string) {
  await db.prepare(
    'UPDATE api_tokens SET revoked_at = ? WHERE user_id = ? AND revoked_at IS NULL'
  ).bind(new Date().toISOString(), userId).run();

  // Also invalidate any cached sessions in KV
  // Short-lived JWTs + refresh token rotation is preferred
}
```
