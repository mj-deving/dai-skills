# Usage Patterns

## Tool Usage Patterns

### Pattern 1: Node Discovery (Most Common)

**Common workflow**: 18s average between steps

```javascript
// Step 1: Search (fast!)
const results = await search_nodes({
  query: "slack",
  mode: "OR",  // Default: any word matches
  limit: 20
});
// → Returns: nodes-base.slack, nodes-base.slackTrigger

// Step 2: Get details (~18s later, user reviewing results)
const details = await get_node({
  nodeType: "nodes-base.slack",
  includeExamples: true  // Get real template configs
});
// → Returns: operations, properties, metadata
```

### Pattern 2: Validation Loop

**Typical cycle**: 23s thinking, 58s fixing

```javascript
// Step 1: Validate
const result = await validate_node({
  nodeType: "nodes-base.slack",
  config: {
    resource: "channel",
    operation: "create"
  },
  profile: "runtime"
});

// Step 2: Check errors (~23s thinking)
if (!result.valid) {
  console.log(result.errors);  // "Missing required field: name"
}

// Step 3: Fix config (~58s fixing)
config.name = "general";

// Step 4: Validate again
await validate_node({...});  // Repeat until clean
```

### Pattern 3: Workflow Editing

**Most used update tool**: 99.0% success rate, 56s average between edits

```javascript
// Iterative workflow building (NOT one-shot!)
// Edit 1
await n8n_update_partial_workflow({
  id: "workflow-id",
  intent: "Add webhook trigger",
  operations: [{type: "addNode", node: {...}}]
});

// ~56s later...

// Edit 2
await n8n_update_partial_workflow({
  id: "workflow-id",
  intent: "Connect webhook to processor",
  operations: [{type: "addConnection", source: "...", target: "..."}]
});

// ~56s later...

// Edit 3 (validation)
await n8n_validate_workflow({id: "workflow-id"});

// Ready? Activate!
await n8n_update_partial_workflow({
  id: "workflow-id",
  intent: "Activate workflow for production",
  operations: [{type: "activateWorkflow"}]
});
```

---

## Detailed Guides

### Node Discovery Tools
See [SEARCH_GUIDE.md](SEARCH_GUIDE.md) for:
- search_nodes
- get_node with detail levels (minimal, standard, full)
- get_node modes (info, docs, search_properties, versions)

### Validation Tools
See [VALIDATION_GUIDE.md](VALIDATION_GUIDE.md) for:
- Validation profiles explained
- validate_node with modes (minimal, full)
- validate_workflow complete structure
- Auto-sanitization system
- Handling validation errors

### Workflow Management
See [WORKFLOW_GUIDE.md](WORKFLOW_GUIDE.md) for:
- n8n_create_workflow
- n8n_update_partial_workflow (19 operation types including patchNodeField!)
- Smart parameters (branch, case)
- AI connection types (8 types)
- Workflow activation (activateWorkflow/deactivateWorkflow)
- n8n_deploy_template
- n8n_workflow_versions
- n8n_manage_credentials (credential CRUD + schema discovery)
- n8n_audit_instance (security auditing)

---
