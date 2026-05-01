# Architecture

## Overview

AI WorkOS Academy is a mission runtime platform where users complete realistic workplace scenarios using ChatGPT-powered agents.

### Core modules

1. **Mission Runtime Engine**
   - Loads mission definitions
   - Maintains step state
   - Triggers dynamic events

2. **Workspace Simulator**
   - Multi-tab context workspace: Inbox, Meetings, Docs, Data, Chat
   - Source payload browsing and filtering

3. **Agent Orchestration Console**
   - Specialized agent calls:
     - Chief of Staff
     - Research Analyst
     - Data Analyst
     - Comms Writer
     - Risk Reviewer

4. **Deliverable Desk**
   - Stores generated artifacts
   - Compares draft vs improved versions
   - Exports final bundle

5. **Evaluation Engine**
   - Rubric-based scoring across six dimensions
   - Pass/fail enforcement
   - Risk flags

6. **Coaching Engine**
   - Converts evaluation gaps into retry plans

## Execution loop

1. User starts mission
2. Runtime loads step + sources
3. User works in chat and agents
4. Artifacts are captured per step
5. Dynamic event optionally injected
6. Evaluator scores result
7. Coach proposes retry plan or next mission unlock

## Data model (logical)

- `users`
- `courses`
- `modules`
- `missions`
- `mission_sources`
- `attempts`
- `artifacts`
- `scores`
- `progress`
- `automation_templates`

## Scoring dimensions

- Outcome quality
- Decision quality
- Communication quality
- Risk handling
- Efficiency
- Automation readiness

## Suggested stack

- Frontend: Next.js + TypeScript
- Backend: FastAPI
- DB: PostgreSQL
- Cache/session: Redis
- Object store: S3-compatible

## Model services

- `assist` — user-facing execution assistant
- `simulate` — scenario event generator
- `evaluate` — rubric grading service
- `coach` — post-attempt guidance

