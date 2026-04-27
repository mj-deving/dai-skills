# Tool Selection

## Tool Categories

n8n-mcp provides tools organized into categories:

1. **Node Discovery** → [SEARCH_GUIDE.md](SEARCH_GUIDE.md)
2. **Configuration Validation** → [VALIDATION_GUIDE.md](VALIDATION_GUIDE.md)
3. **Workflow Management** → [WORKFLOW_GUIDE.md](WORKFLOW_GUIDE.md)
4. **Template Library** - Search and deploy 2,700+ real workflows
5. **Data Tables** - Manage n8n data tables and rows (`n8n_manage_datatable`)
6. **Credential Management** - Full credential CRUD + schema discovery (`n8n_manage_credentials`)
7. **Security & Audit** - Instance security auditing with custom deep scan (`n8n_audit_instance`)
8. **Documentation & Guides** - Tool docs, AI agent guide, Code node guides

---

## Quick Reference

### Most Used Tools (by success rate)

| Tool | Use When | Speed |
|------|----------|-------|
| `search_nodes` | Finding nodes by keyword | <20ms |
| `get_node` | Understanding node operations (detail="standard") | <10ms |
| `validate_node` | Checking configurations (mode="full") | <100ms |
| `n8n_create_workflow` | Creating workflows | 100-500ms |
| `n8n_update_partial_workflow` | Editing workflows (MOST USED!) | 50-200ms |
| `validate_workflow` | Checking complete workflow | 100-500ms |
| `n8n_deploy_template` | Deploy template to n8n instance | 200-500ms |
| `n8n_manage_datatable` | Managing data tables and rows | 50-500ms |
| `n8n_manage_credentials` | Credential CRUD + schema discovery | 50-500ms |
| `n8n_audit_instance` | Security audit (built-in + custom scan) | 500-5000ms |
| `n8n_autofix_workflow` | Auto-fix validation errors | 200-1500ms |

---

## Tool Selection Guide

### Finding the Right Node

**Workflow**:
```
1. search_nodes({query: "keyword"})
2. get_node({nodeType: "nodes-base.name"})
3. [Optional] get_node({nodeType: "nodes-base.name", mode: "docs"})
```

**Example**:
```javascript
// Step 1: Search
search_nodes({query: "slack"})
// Returns: nodes-base.slack

// Step 2: Get details
get_node({nodeType: "nodes-base.slack"})
// Returns: operations, properties, examples (standard detail)

// Step 3: Get readable documentation
get_node({nodeType: "nodes-base.slack", mode: "docs"})
// Returns: markdown documentation
```

**Common pattern**: search → get_node (18s average)

### Validating Configuration

**Workflow**:
```
1. validate_node({nodeType, config: {}, mode: "minimal"}) - Check required fields
2. validate_node({nodeType, config, profile: "runtime"}) - Full validation
3. [Repeat] Fix errors, validate again
```

**Common pattern**: validate → fix → validate (23s thinking, 58s fixing per cycle)

### Managing Workflows

**Workflow**:
```
1. n8n_create_workflow({name, nodes, connections})
2. n8n_validate_workflow({id})
3. n8n_update_partial_workflow({id, operations: [...]})
4. n8n_validate_workflow({id}) again
5. n8n_update_partial_workflow({id, operations: [{type: "activateWorkflow"}]})
```

**Common pattern**: iterative updates (56s average between edits)

---
