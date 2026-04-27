# Node Type Formats

## Critical: nodeType Formats

**Two different formats** for different tools!

### Format 1: Search/Validate Tools
```javascript
// Use SHORT prefix
"nodes-base.slack"
"nodes-base.httpRequest"
"nodes-base.webhook"
"nodes-langchain.agent"
```

**Tools that use this**:
- search_nodes (returns this format)
- get_node
- validate_node
- validate_workflow

### Format 2: Workflow Tools
```javascript
// Use FULL prefix
"n8n-nodes-base.slack"
"n8n-nodes-base.httpRequest"
"n8n-nodes-base.webhook"
"@n8n/n8n-nodes-langchain.agent"
```

**Tools that use this**:
- n8n_create_workflow
- n8n_update_partial_workflow

### Conversion

```javascript
// search_nodes returns BOTH formats
{
  "nodeType": "nodes-base.slack",          // For search/validate tools
  "workflowNodeType": "n8n-nodes-base.slack"  // For workflow tools
}
```

---
