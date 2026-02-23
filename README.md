# Projeto PS2 - Modular Architecture

## Overview

This project uses a modular, orchestrated architecture designed for scalability and extensibility.

Core principles:
- Central Orchestrator
- Dependency Injection (Container)
- Stateless Modules
- Pipeline-based execution
- Plugin system
- Middleware validation
- Event-driven execution
- Centralized logging
- Automated test harness

## Execution Flow

UI → AppController → Orchestrator → Pipeline → Module → Service

## Running

```bash
python main.py