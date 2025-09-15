# Implementation Plan: Flow AI Platform - Revolutionary Business Operating System

**Branch**: `main` | **Date**: September 15, 2025 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `.specify/spec.md`

## Execution Flow (/plan command scope)
```
✓ 1. Load feature spec from Input path
✓ 2. Fill Technical Context (scan for NEEDS CLARIFICATION)
   → Project Type: multi-platform (web + mobile + n8n workflows)
   → Structure Decision: Multi-platform with n8n orchestration
✓ 3. Evaluate Constitution Check section below
   → Agent-first architecture justified for business automation
   → Update Progress Tracking: Initial Constitution Check
✓ 4. Execute Phase 0 → research.md
✓ 5. Execute Phase 1 → contracts, data-model.md, quickstart.md, CLAUDE.md
✓ 6. Re-evaluate Constitution Check section
   → Multi-platform complexity justified by business requirements
   → Update Progress Tracking: Post-Design Constitution Check
✓ 7. Plan Phase 2 → Describe task generation approach (DO NOT create tasks.md)
✓ 8. STOP - Ready for /tasks command
```

## Summary
Flow AI Platform is a revolutionary business operating system featuring AI agents as team members, accessible through iMessage-style interfaces on web and native iPhone app. Technical approach leverages n8n as workflow automation backbone (60-70% development acceleration), FastAPI backend, Next.js frontend, and native iOS development. The platform includes a meta-agent system capable of building specialized agents automatically, creating a self-improving ecosystem for business automation.

## Technical Context
**Language/Version**:
- Backend: Python 3.11+ with FastAPI
- Frontend: Next.js 14 with React Server Components
- Mobile: Swift 5.9 with SwiftUI for iOS 17+
- Workflows: n8n with custom TypeScript nodes

**Primary Dependencies**:
- n8n workflow engine, FastAPI, Next.js, SwiftUI
- PostgreSQL 15 with pgvector, Qdrant, Redis
- OpenAI GPT-4 Turbo, Anthropic Claude 3 Haiku
- React Query, Zustand, Socket.io

**Storage**: PostgreSQL 15 with pgvector extension, Qdrant vector database, Redis cache
**Testing**: pytest + FastAPI TestClient (backend), Vitest + Testing Library (frontend), XCTest (iOS)
**Target Platform**: Linux containers for backend, web browsers, iOS 17+ devices
**Project Type**: multi-platform - web application + native mobile app + workflow automation
**Performance Goals**: <100ms chat response, <3s agent processing, 99.9% uptime, 1M+ daily messages
**Constraints**: SOC 2 compliance, GDPR ready, enterprise security, real-time communication
**Scale/Scope**: 10k+ workspaces, 100+ concurrent users per workspace, 50+ agent types

## Constitution Check
*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Simplicity**:
- Projects: 4 (n8n workflows, FastAPI backend, Next.js frontend, iOS app)
- Using framework directly? (n8n, FastAPI, Next.js, SwiftUI - no wrapper abstraction)
- Single data model? (Domain entities map across all platforms consistently)
- Avoiding patterns? (No over-engineering - direct integration with proven tools)

**Architecture**:
- EVERY feature as library? (Agent engine, workflow orchestrator, chat service, auth service)
- Libraries listed:
  - agent-engine: Core AI agent execution and memory management
  - workflow-orchestrator: n8n custom nodes and automation logic
  - chat-service: Real-time messaging and conversation management
  - auth-service: Multi-platform authentication and workspace management
  - ios-sdk: Swift package for native iOS integration
- CLI per library: Admin CLI for agent management, workflow debugging, system monitoring
- Library docs: llms.txt format for AI context and developer documentation

**Testing (NON-NEGOTIABLE)**:
- RED-GREEN-Refactor cycle enforced? (Tests written first across all platforms)
- Git commits show tests before implementation? (Strict TDD workflow)
- Order: Contract→Integration→E2E→Unit across web, mobile, and workflow platforms
- Real dependencies used? (Actual PostgreSQL, Redis, n8n instances for testing)
- Integration tests for: n8n workflows, agent interactions, mobile-web sync, API contracts
- FORBIDDEN: Implementation before test, skipping RED phase on any platform

**Observability**:
- Structured logging included? (Winston for backend, console for frontend, os_log for iOS)
- Frontend logs → backend? (Centralized logging with request correlation)
- Error context sufficient? (Request IDs, agent context, workflow execution traces)

**Versioning**:
- Version number assigned? (1.0.0 - MAJOR.MINOR.BUILD synchronized across platforms)
- BUILD increments on every change? (Automated CI/CD with platform coordination)
- Breaking changes handled? (API versioning, mobile app backward compatibility)

## Project Structure

### Documentation (this feature)
```
.specify/
├── plan.md              # This file (/plan command output)
├── spec.md              # Platform specification
├── research.md          # Phase 0 output (/plan command)
├── data-model.md        # Phase 1 output (/plan command)
├── quickstart.md        # Phase 1 output (/plan command)
├── contracts/           # Phase 1 output (/plan command)
├── n8n-nodes/           # Custom node specifications
└── tasks.md             # Phase 2 output (/tasks command)
```

### Source Code (repository root)
```
# Multi-platform architecture with n8n orchestration
n8n-workflows/
├── custom-nodes/        # Custom n8n nodes for Flow AI
│   ├── FlowAIAgent/     # Main agent execution node
│   ├── VectorSearch/    # RAG retrieval from Qdrant
│   ├── ConversationMemory/ # Context persistence
│   ├── AgentHandoff/    # Multi-agent orchestration
│   └── TokenOptimizer/  # LLM cost management
├── templates/           # Workflow templates for agents
├── tests/               # n8n workflow testing
└── deployment/          # Docker and k8s configs

backend/
├── src/
│   ├── agents/          # Agent engine and orchestration
│   ├── workflows/       # n8n integration and workflow management
│   ├── chat/            # Real-time chat and WebSocket handling
│   ├── auth/            # Authentication and workspace management
│   ├── integrations/    # Third-party API integrations
│   └── api/             # FastAPI routes and middleware
├── tests/
│   ├── contract/        # API contract tests
│   ├── integration/     # Service integration tests
│   └── unit/            # Unit tests
└── alembic/             # Database migrations

frontend/
├── src/
│   ├── components/      # React components (chat, agents, workflows)
│   ├── pages/           # Next.js pages and routing
│   ├── hooks/           # Custom React hooks
│   ├── stores/          # Zustand state management
│   ├── services/        # API clients and WebSocket handling
│   └── lib/             # Shared utilities and configurations
├── tests/
│   ├── e2e/             # End-to-end tests with Playwright
│   ├── integration/     # Component integration tests
│   └── unit/            # Component unit tests
└── public/              # Static assets and PWA manifest

ios/
├── FlowAI/              # Main iOS application
│   ├── Views/           # SwiftUI views and components
│   ├── ViewModels/      # MVVM architecture
│   ├── Services/        # API clients and background sync
│   ├── Models/          # Data models and CoreData
│   └── Utils/           # iOS-specific utilities
├── FlowAITests/         # Unit tests
├── FlowAIUITests/       # UI automation tests
├── Widgets/             # iOS widgets and extensions
└── WatchApp/            # Apple Watch companion (future)

shared/
├── types/               # TypeScript/Swift type definitions
├── contracts/           # API contract schemas (OpenAPI)
└── protocols/           # Cross-platform communication protocols
```

**Structure Decision**: Multi-platform architecture justified by business requirements for web accessibility, mobile productivity, and sophisticated workflow automation

## Phase 0: Outline & Research

### Research Tasks Completed:

1. **n8n Custom Node Development Research**:
   - **Decision**: TypeScript-based custom nodes with shared agent execution framework
   - **Rationale**: Enables rapid workflow development while maintaining type safety and reusability
   - **Alternatives considered**: Direct API orchestration (rejected: loses visual workflow benefits)

2. **Multi-Platform State Synchronization Research**:
   - **Decision**: WebSocket + Redis for real-time sync with offline-first mobile architecture
   - **Rationale**: Ensures seamless experience across web and mobile with conflict resolution
   - **Alternatives considered**: Pure REST API (rejected: poor real-time experience)

3. **iOS Development Strategy Research**:
   - **Decision**: Native SwiftUI app with shared business logic via API
   - **Rationale**: Superior user experience, deep iOS integration, App Store optimization
   - **Alternatives considered**: React Native (rejected: compromises native feel)

4. **Agent Memory and Context Research**:
   - **Decision**: Hybrid approach with PostgreSQL for structured data and Qdrant for semantic search
   - **Rationale**: Balances query performance with semantic understanding capabilities
   - **Alternatives considered**: Single vector database (rejected: poor structured query performance)

5. **Workflow Orchestration Research**:
   - **Decision**: n8n with custom nodes for 60-70% development acceleration
   - **Rationale**: Visual workflow design, extensive integrations, rapid deployment
   - **Alternatives considered**: Custom orchestrator (rejected: significant development overhead)

6. **Agent Builder Meta-System Research**:
   - **Decision**: LLM-powered agent specification generation with template system
   - **Rationale**: Enables self-improving platform with rapid agent deployment
   - **Alternatives considered**: Manual agent configuration (rejected: scaling limitations)

**Output**: research.md with all technical decisions and mobile-web-workflow integration strategy

## Phase 1: Design & Contracts

### Data Model Entities (data-model.md):

**Core Platform Entities**:
1. **Workspace**: id, name, domain, plan_type, settings, created_at
2. **User**: id, email, name, avatar_url, workspace_memberships, preferences
3. **WorkspaceMember**: workspace_id, user_id, role, permissions, joined_at

**Agent System Entities**:
4. **Agent**: id, workspace_id, name, type, avatar, prompt, capabilities, config
5. **AgentTemplate**: id, name, description, prompt_template, workflow_template
6. **Conversation**: id, workspace_id, user_id, agent_id, title, context, metadata
7. **Message**: id, conversation_id, sender_type, content, timestamp, message_type

**Workflow Entities**:
8. **WorkflowTemplate**: id, name, description, n8n_workflow_json, agent_types
9. **WorkflowExecution**: id, workflow_id, trigger_data, status, result, logs
10. **Integration**: id, workspace_id, provider, oauth_tokens, config, status

**Mobile Sync Entities**:
11. **SyncEvent**: id, workspace_id, entity_type, entity_id, action, timestamp
12. **DeviceRegistration**: id, user_id, device_token, platform, last_sync

### API Contracts (/contracts/):

**Core Platform APIs**:
```yaml
# /contracts/platform-api.yaml
POST /api/workspaces: Create new workspace
GET /api/workspaces/{id}: Get workspace details
POST /api/workspaces/{id}/members: Invite workspace member
PUT /api/workspaces/{id}/settings: Update workspace configuration
```

**Agent Management APIs**:
```yaml
# /contracts/agent-api.yaml
GET /api/workspaces/{id}/agents: List available agents
POST /api/workspaces/{id}/agents: Create custom agent
PUT /api/agents/{id}/config: Update agent configuration
POST /api/agents/{id}/train: Train agent on knowledge base
GET /api/agents/{id}/capabilities: Get agent capability matrix
```

**Chat and Conversation APIs**:
```yaml
# /contracts/chat-api.yaml
GET /api/conversations: List user conversations with pagination
POST /api/conversations: Create new conversation with agent
POST /api/conversations/{id}/messages: Send message to agent
WebSocket /ws/chat/{conversation_id}: Real-time chat communication
```

**n8n Workflow APIs**:
```yaml
# /contracts/workflow-api.yaml
GET /api/workflows/templates: List available workflow templates
POST /api/workflows: Create workflow from template
POST /api/workflows/{id}/execute: Trigger workflow execution
GET /api/workflows/{id}/executions: Get workflow execution history
```

**iOS-Specific APIs**:
```yaml
# /contracts/mobile-api.yaml
POST /api/mobile/devices: Register device for push notifications
GET /api/mobile/sync/{timestamp}: Get changes since timestamp
POST /api/mobile/sync/conflicts: Resolve sync conflicts
GET /api/mobile/offline-data: Get offline-capable data subset
```

### n8n Custom Node Specifications (/n8n-nodes/):

**FlowAIAgent Node**:
```typescript
// FlowAI Agent execution with memory and context
interface FlowAIAgentConfig {
  agentId: string;
  prompt: string;
  model: 'gpt-4-turbo' | 'claude-3-haiku';
  maxTokens: number;
  temperature: number;
  memoryScope: 'conversation' | 'workspace' | 'none';
}
```

**VectorSearch Node**:
```typescript
// RAG retrieval from Qdrant with relevance scoring
interface VectorSearchConfig {
  collection: string;
  query: string;
  limit: number;
  scoreThreshold: number;
  filters: Record<string, any>;
}
```

**AgentHandoff Node**:
```typescript
// Multi-agent orchestration and task delegation
interface AgentHandoffConfig {
  targetAgent: string;
  handoffReason: string;
  contextData: Record<string, any>;
  requiresApproval: boolean;
}
```

### iOS App Architecture (/ios-architecture/):

**SwiftUI View Hierarchy**:
- `ContentView`: Main container with tab navigation
- `ChatListView`: iMessage-style conversation list
- `ChatView`: Individual conversation with agent
- `AgentListView`: Available agents with status indicators
- `WorkflowView`: Visual workflow builder (simplified)
- `SettingsView`: App preferences and account management

**Data Persistence Strategy**:
- Core Data for offline-first architecture
- CloudKit integration for cross-device sync
- Background sync with conflict resolution
- Optimistic UI updates with rollback capability

### Contract Tests Generated:
- agent-contract.test.ts: Agent creation, configuration, and execution
- chat-contract.test.ts: Real-time messaging and conversation management
- workflow-contract.test.ts: n8n workflow execution and monitoring
- mobile-contract.test.ts: iOS-specific API endpoints and sync
- integration-contract.test.ts: Third-party API integration testing

### Integration Test Scenarios (quickstart.md):
1. **Complete Platform Setup**: Workspace creation, user onboarding, agent deployment
2. **Multi-Agent Conversation**: Project Manager delegating to specialized agents
3. **Mobile-Web Sync**: Starting conversation on mobile, continuing on web
4. **Workflow Automation**: Email agent processing inbox and creating calendar events
5. **Agent Builder Usage**: Creating custom agent using meta-agent system
6. **Enterprise Onboarding**: Team setup, permissions, and integration configuration

### Agent Context File (CLAUDE.md):
- Multi-platform development patterns and conventions
- n8n custom node development guidelines
- iOS and web synchronization protocols
- Agent memory and context management strategies
- Cross-platform testing and deployment procedures

**Output**: data-model.md, /contracts/* schemas, /n8n-nodes/* specs, iOS architecture, failing tests, quickstart.md, CLAUDE.md

## Phase 2: Task Planning Approach
*This section describes what the /tasks command will do - DO NOT execute during /plan*

**Task Generation Strategy**:
- Load `/templates/tasks-template.md` as comprehensive base
- Generate tasks from Phase 1 design docs across all platforms
- Platform-specific task categories:
  - Infrastructure setup tasks [P] (8 tasks)
  - n8n custom node development [P] (15 tasks)
  - Backend API implementation (20 tasks)
  - Frontend web development (18 tasks)
  - iOS app development (22 tasks)
  - Integration and testing (12 tasks)
  - Deployment and monitoring (8 tasks)

**Ordering Strategy**:
- TDD order: Tests before implementation across all platforms
- Platform dependency order: n8n nodes → Backend APIs → Frontend/iOS (parallel)
- Cross-platform sync points for integration testing
- Mark [P] for parallel execution within platform boundaries
- Sequential gates for critical dependencies (auth before chat, etc.)

**Mobile Development Integration**:
- iOS development runs parallel to web development after backend APIs
- Shared testing for API contracts and data synchronization
- App Store submission process integrated into deployment pipeline
- Device testing and beta distribution coordination

**Agent Builder System Tasks**:
- Meta-agent prompt engineering and testing
- Agent template creation and validation system
- Automated agent deployment and configuration pipeline
- Performance monitoring and optimization for generated agents

**Estimated Output**: 103 numbered, ordered tasks in tasks.md covering:
1. Infrastructure and n8n setup (Weeks 1-2)
2. Custom node development and testing (Weeks 2-4)
3. Backend API and agent system (Weeks 3-6)
4. Frontend web application (Weeks 4-7)
5. iOS app development (Weeks 5-8)
6. Advanced agent features and builder system (Weeks 7-10)
7. Integration testing and optimization (Weeks 9-12)
8. Enterprise features and deployment (Weeks 11-16)

**IMPORTANT**: This phase is executed by the /tasks command, NOT by /plan

## Phase 3+: Future Implementation
*These phases are beyond the scope of the /plan command*

**Phase 3**: Task execution (/tasks command creates tasks.md)
**Phase 4**: Multi-platform implementation following constitutional TDD principles
**Phase 5**: Integration testing across web, mobile, and workflow platforms
**Phase 6**: Performance optimization and enterprise deployment
**Phase 7**: Agent Builder system launch and ecosystem development

## Complexity Tracking
*Multi-platform complexity justified by business requirements*

| Complexity Area | Business Justification | Simpler Alternative Rejected Because |
|-----------------|------------------------|-------------------------------------|
| Multi-platform (4 codebases) | Mobile productivity essential for target market | Web-only solution insufficient for SMB mobility needs |
| n8n + Custom nodes | 60-70% development acceleration critical | Custom orchestrator would delay MVP by 3+ months |
| Agent Builder meta-system | Self-improving platform creates competitive moat | Manual agent creation doesn't scale to 50+ agent types |
| Real-time sync | Business automation requires immediate responsiveness | Polling-based sync creates poor user experience |

## Progress Tracking
*This checklist is updated during execution flow*

**Phase Status**:
- [x] Phase 0: Research complete (/plan command)
- [x] Phase 1: Design complete (/plan command)
- [x] Phase 2: Task planning complete (/plan command - describe approach only)
- [ ] Phase 3: Tasks generated (/tasks command)
- [ ] Phase 4: Multi-platform implementation complete
- [ ] Phase 5: Integration testing passed
- [ ] Phase 6: Performance optimization complete
- [ ] Phase 7: Agent Builder system launched

**Gate Status**:
- [x] Initial Constitution Check: PASS (complexity justified)
- [x] Post-Design Constitution Check: PASS (TDD enforced across platforms)
- [x] All NEEDS CLARIFICATION resolved
- [x] Complexity deviations documented and justified

**Platform Readiness**:
- [x] n8n custom node specifications complete
- [x] Backend API contracts defined
- [x] Frontend architecture planned
- [x] iOS app architecture designed
- [x] Cross-platform sync strategy established
- [x] Agent Builder system specified

---
*Based on Constitution v2.1.1 - See `.specify/memory/constitution.md`*
*Multi-platform architecture enables revolutionary business automation with consumer-app simplicity*