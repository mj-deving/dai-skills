# Templates Data Tables Credentials And Security

## Template Usage

### Search Templates

```javascript
// Search by keyword (default mode)
search_templates({
  query: "webhook slack",
  limit: 20
});

// Search by node types
search_templates({
  searchMode: "by_nodes",
  nodeTypes: ["n8n-nodes-base.httpRequest", "n8n-nodes-base.slack"]
});

// Search by task type
search_templates({
  searchMode: "by_task",
  task: "webhook_processing"
});

// Search by metadata (complexity, setup time)
search_templates({
  searchMode: "by_metadata",
  complexity: "simple",
  maxSetupMinutes: 15
});
```

### Get Template Details

```javascript
get_template({
  templateId: 2947,
  mode: "structure"  // nodes+connections only
});

get_template({
  templateId: 2947,
  mode: "full"  // complete workflow JSON
});
```

### Deploy Template Directly

```javascript
// Deploy template to your n8n instance
n8n_deploy_template({
  templateId: 2947,
  name: "My Weather to Slack",  // Custom name (optional)
  autoFix: true,  // Auto-fix common issues (default)
  autoUpgradeVersions: true  // Upgrade node versions (default)
});
// Returns: workflow ID, required credentials, fixes applied
```

---

## Data Table Management

### n8n_manage_datatable

Unified tool for managing n8n data tables and rows. Supports CRUD operations on tables and rows with filtering, pagination, and dry-run support.

**Table Actions**: `createTable`, `listTables`, `getTable`, `updateTable`, `deleteTable`
**Row Actions**: `getRows`, `insertRows`, `updateRows`, `upsertRows`, `deleteRows`

```javascript
// Create a data table
n8n_manage_datatable({
  action: "createTable",
  name: "Contacts",
  columns: [
    {name: "email", type: "string"},
    {name: "score", type: "number"}
  ]
})

// Get rows with filter
n8n_manage_datatable({
  action: "getRows",
  tableId: "dt-123",
  filter: {
    filters: [{columnName: "status", condition: "eq", value: "active"}]
  },
  limit: 50
})

// Insert rows
n8n_manage_datatable({
  action: "insertRows",
  tableId: "dt-123",
  data: [{email: "a@b.com", score: 10}],
  returnType: "all"
})

// Update with dry run (preview changes)
n8n_manage_datatable({
  action: "updateRows",
  tableId: "dt-123",
  filter: {filters: [{columnName: "score", condition: "lt", value: 5}]},
  data: {status: "inactive"},
  dryRun: true
})

// Upsert (update or insert)
n8n_manage_datatable({
  action: "upsertRows",
  tableId: "dt-123",
  filter: {filters: [{columnName: "email", condition: "eq", value: "a@b.com"}]},
  data: {score: 15},
  returnData: true
})
```

**Filter conditions**: `eq`, `neq`, `like`, `ilike`, `gt`, `gte`, `lt`, `lte`

**Best practices**:
- Use `dryRun: true` before bulk updates/deletes to verify filter correctness
- Define column types upfront (`string`, `number`, `boolean`, `date`)
- Use `returnType: "count"` (default) for insertRows to minimize response size
- `deleteRows` requires a filter - cannot delete all rows without one

---

## Credential Management

### n8n_manage_credentials

Unified tool for managing n8n credentials. Supports full CRUD operations and schema discovery.

**Actions**: `list`, `get`, `create`, `update`, `delete`, `getSchema`

```javascript
// List all credentials
n8n_manage_credentials({action: "list"})
// → Returns: id, name, type, createdAt, updatedAt (never exposes secrets)

// Get credential by ID
n8n_manage_credentials({action: "get", id: "123"})
// → Returns: credential metadata (data field stripped for security)

// Discover required fields for a credential type
n8n_manage_credentials({action: "getSchema", credentialType: "httpHeaderAuth"})
// → Returns: required fields, types, descriptions

// Create credential
n8n_manage_credentials({
  action: "create",
  name: "My Slack Token",
  type: "slackApi",
  data: {accessToken: "xoxb-..."}
})

// Update credential
n8n_manage_credentials({
  action: "update",
  id: "123",
  name: "Updated Name",
  data: {accessToken: "xoxb-new-..."},
  type: "slackApi"  // Optional, needed by some n8n versions
})

// Delete credential
n8n_manage_credentials({action: "delete", id: "123"})
```

**Security**:
- `get`, `create`, and `update` responses strip the `data` field (defense-in-depth)
- `get` action falls back to list+filter if direct GET returns 403/405 (not all n8n versions expose this endpoint)
- Credential request bodies are redacted from debug logs

**Best practices**:
- Use `getSchema` before `create` to discover required fields for a credential type
- The `data` field contains the actual secret values — provide it only on create/update
- Always verify credential creation by listing afterward

---

## Security & Audit

### n8n_audit_instance

Security audit tool that combines n8n's built-in audit with custom deep scanning of all workflows.

```javascript
// Full audit (default — runs both built-in + custom scan)
n8n_audit_instance()

// Built-in audit only (specific categories)
n8n_audit_instance({
  categories: ["credentials", "nodes"],
  includeCustomScan: false
})

// Custom scan only (specific checks)
n8n_audit_instance({
  customChecks: ["hardcoded_secrets", "unauthenticated_webhooks"]
})
```

**Built-in audit categories**: `credentials`, `database`, `nodes`, `instance`, `filesystem`

**Custom deep scan checks**:
- `hardcoded_secrets` — Detects 50+ patterns for API keys, tokens, passwords (OpenAI, AWS, Stripe, GitHub, Slack, etc.) plus PII (email, phone, credit card). Secrets are masked in output (first 6 + last 4 chars).
- `unauthenticated_webhooks` — Flags webhook/form triggers without authentication
- `error_handling` — Flags workflows with 3+ nodes and no error handling
- `data_retention` — Flags workflows saving all execution data (success + failure)

**Parameters** (all optional):
- `categories` — Array of built-in audit categories
- `includeCustomScan` — Boolean (default: `true`)
- `customChecks` — Array subset of the 4 custom checks
- `daysAbandonedWorkflow` — Days threshold for abandoned workflow detection

**Output**: Actionable markdown report with:
- Summary table (critical/high/medium/low finding counts)
- Findings grouped by workflow
- Remediation Playbook with three sections:
  - **Auto-fixable** — Items you can fix with tool chains (e.g., add auth to webhooks)
  - **Requires review** — Items needing human judgment (e.g., PII detection)
  - **Requires user action** — Items needing manual intervention (e.g., rotate exposed keys)

---
