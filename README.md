# MCP Evaluation Framework for SDK Integration

A Python-based automated framework for evaluating the reliability and correctness of **Model Context Protocol (MCP) tools** in real SDK integration workflows.

The framework verifies that MCP tools perform the operations they are expected to perform when invoked by an LLM, and validates the resulting application behavior end-to-end.

---

## Overview

As LLMs increasingly interact with external systems through MCP, it is not enough to verify that an MCP tool returns a successful response.

The actual question is:

> **Did the MCP tool perform the requested operation correctly?**

This project provides an automated environment for testing MCP behavior in a real application workflow.

The LLM acts as the **client that invokes the MCP tools**, while the framework evaluates the MCP execution and its real-world outcome.

The evaluation continues beyond the tool response and verifies whether the requested operation was successfully reflected in the application.

---

## What We Test

The framework evaluates the MCP execution across the complete workflow:

```text
User Request
     ↓
    LLM
     ↓
MCP Tool Invocation
     ↓
MCP Execution
     ↓
Application Changes
     ↓
Build
     ↓
Runtime
     ↓
Behavior Validation
```

The LLM is part of the execution environment, but the primary subject of evaluation is the **MCP layer and its effect on the application**.

---

## Key Capabilities

* Automated MCP tool evaluation
* End-to-end SDK integration testing
* Execution with real MCP tools
* Fresh sandbox for every test
* Automated application compilation
* Runtime validation
* Deep Link validation
* Execution tracing and auditing
* Failure detection and attribution
* Interactive HTML reports

---

## Evaluation Methodology

Each test follows a controlled evaluation pipeline:

```text
Define
  ↓
Execute
  ↓
Observe
  ↓
Validate
  ↓
Report
```

### Define

A test scenario specifies the requested operation, application context, MCP tools involved, and expected outcome.

### Execute

The LLM interacts with the MCP server and invokes the relevant MCP tools.

No MCP behavior is mocked during the actual evaluation.

### Observe

The framework records the interaction and execution flow, including tool calls and responses.

### Validate

The framework verifies the result at multiple levels:

1. **MCP level** — Was the requested tool operation executed?
2. **Build level** — Does the resulting application compile?
3. **Runtime level** — Does the application run successfully?
4. **Behavior level** — Does the application demonstrate the expected behavior?

### Report

The collected execution data is analyzed and presented in a structured report.

---

## Fresh Sandbox

Every evaluation starts from a **fresh sandbox**.

This guarantees that:

* Previous executions cannot affect the current test
* Each evaluation starts from the same baseline
* Test results are isolated
* Failures can be reproduced more reliably

The original application template remains unchanged.

```text
                 Application Template
                         │
                         ▼
                   Fresh Sandbox
                         │
              ┌──────────┴──────────┐
              ▼                     ▼
          MCP Execution          Validation
              │                     │
              └──────────┬──────────┘
                         ▼
                       Report
```

---

## First Use Case: AppsFlyer SDK Integration

The first real-world use case for the framework is **AppsFlyer SDK integration**.

The framework evaluates MCP tools responsible for SDK-related operations in iOS applications.

Examples include:

```text
integrateSdk
verifyIosSdk
createDeepLink
createIosDeepLink
```

The evaluation does not stop when an MCP tool reports success.

For example, when an MCP tool is expected to integrate an SDK, the framework continues by compiling and running the application and validating the expected result.

This allows the framework to detect cases where:

```text
MCP Response = Success
        ↓
Application = Incorrect / Incomplete
```

---

## Failure Attribution

When a test fails, the framework collects evidence from the different stages of execution to determine where the failure occurred.

Possible failure points include:

* MCP tool execution
* MCP response
* Generated implementation
* Compilation
* Runtime
* Application behavior
* Validation

This makes it possible to distinguish between a successful tool response and a **successful end-to-end operation**.

---

## Architecture

The framework is orchestrated using a **LangGraph state machine**.

The system contains specialized components responsible for different parts of the evaluation:

```text
                    ┌───────────────┐
                    │  User Request │
                    └───────┬───────┘
                            ▼
                    ┌───────────────┐
                    │  Prompt Agent │
                    └───────┬───────┘
                            ▼
                    ┌───────────────┐
                    │   SDK Agent   │
                    └───────┬───────┘
                            ▼
                    ┌───────────────┐
                    │   MCP Tools   │
                    └───────┬───────┘
                            ▼
                    ┌───────────────┐
                    │  Application  │
                    └───────┬───────┘
                            ▼
                 ┌─────────────────────┐
                 │ Build & Runtime     │
                 └──────────┬──────────┘
                            ▼
                    ┌───────────────┐
                    │  Validation   │
                    └───────┬───────┘
                            ▼
                    ┌───────────────┐
                    │    Report     │
                    └───────────────┘
```

Supporting components provide execution monitoring, audit recording, compilation, and validation.

---

## Technology Stack

* Python
* Model Context Protocol (MCP)
* LangGraph
* LangChain
* LLM-based Agents
* Xcode / iOS Simulator
* Appium
* Automated Testing
* HTML Reporting

---

## Project Structure

```text
PipelineAutomationMCP/
│
├── data/
│   ├── application/
│   ├── reports/
│   ├── rules/
│   └── useCases/
│
├── infra/
│   └── agents/
│       ├── answerAgent/
│       ├── compilationAgent/
│       ├── promptGanertorAgent/
│       └── sdkAgent/
│
├── tests/
├── ui/
├── scripts/
│
├── main.py
├── pyproject.toml
├── CONFIG.md
└── SETUP.md
```

---

## Getting Started

### Prerequisites

Depending on the evaluation scenario, the environment may require:

* Python
* Git
* Xcode and iOS Simulator
* Android SDK
* Appium
* Access to the relevant MCP server
* Required API credentials configured locally

### Installation

Install the project dependencies according to the instructions in:

**[SETUP.md](SETUP.md)**

### Configuration

Runtime credentials and environment-specific configuration must be supplied through environment variables or a local `.env` file.

**Never commit API keys, tokens, or other credentials to the repository.**

For configuration details, see:

**[CONFIG.md](CONFIG.md)**

---

## Project Goal

The goal of this project is to provide a reliable and automated way to answer:

> **Can we verify that an MCP tool actually performed the operation it was expected to perform?**

Instead of evaluating MCP tools only by their responses, the framework validates their **real effect on the application**.

The result is an end-to-end evaluation of MCP behavior — from tool invocation to actual application behavior.
