
---

# 📄 ARCHITECTURE.md

```markdown
# Architecture Overview

## Core Components

### Orchestrator
Coordinates pipeline execution.

### Registry
Stores modules and pipelines.

### Container
Handles dependency injection.

### Modules
Stateless execution units.

### Services
Business logic layer.

### Middleware
Context validation layer.

### EventBus
Internal event system.

### PluginLoader
Auto-loads plugins at bootstrap.

---

## Design Rules

1. Modules do not call other modules directly.
2. Services do not depend on Orchestrator.
3. UI does not contain business logic.
4. No shared global state.
5. All execution flows through Orchestrator.