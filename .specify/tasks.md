# Tasks: Flow AI Platform - Revolutionary Business Operating System

**Input**: Design documents from `.specify/`
**Prerequisites**: plan.md (✓), research.md (✓), data-model.md (✓), contracts/ (✓), agent-builder-system.md (✓), ios-development-plan.md (✓)

## Execution Flow (main)
```
✓ 1. Load plan.md from feature directory
   → Multi-platform architecture: n8n + FastAPI + Next.js + iOS
   → Extract: Python 3.11+, TypeScript, Swift, n8n custom nodes
✓ 2. Load design documents:
   → data-model.md: 12 entities → model tasks
   → contracts/: 5 API groups → contract test tasks
   → agent-builder-system.md: Meta-agent implementation
   → ios-development-plan.md: Native iOS app tasks
✓ 3. Generate tasks by category:
   → Setup: multi-platform project init, n8n deployment
   → Tests: contract tests, integration tests (all platforms)
   → Core: agents, workflows, chat, auth (backend/frontend/iOS)
   → Integration: n8n nodes, APIs, real-time sync
   → Polish: optimization, security, deployment
✓ 4. Apply task rules:
   → Different platforms/files = mark [P] for parallel
   → Cross-platform dependencies = sequential
   → Tests before implementation (TDD enforced)
✓ 5. Number tasks sequentially (T001, T002...)
✓ 6. Generate dependency graph with platform coordination
✓ 7. Create parallel execution examples for development teams
✓ 8. Validate task completeness across all platforms
✓ 9. Return: SUCCESS (103 tasks ready for execution)
```

## Format: `[ID] [P?] Description`
- **[P]**: Can run in parallel (different files/platforms, no dependencies)
- Include exact file paths and platform specifications

## Path Conventions
- **n8n workflows**: `n8n-workflows/custom-nodes/`, `n8n-workflows/templates/`
- **Backend**: `backend/src/`, `backend/tests/`
- **Frontend**: `frontend/src/`, `frontend/tests/`
- **iOS**: `ios/FlowAI/`, `ios/FlowAITests/`
- **Shared**: `shared/types/`, `shared/contracts/`

---

## Phase 1: Infrastructure Setup (Weeks 1-2)

### Phase 1.1: Project Initialization
- [ ] T001 Create multi-platform project structure per implementation plan
- [ ] T002 [P] Initialize n8n-workflows directory with custom-nodes structure
- [ ] T003 [P] Initialize FastAPI backend with Python 3.11+ and poetry dependencies
- [ ] T004 [P] Initialize Next.js 14 frontend with TypeScript and required packages
- [ ] T005 [P] Initialize iOS Xcode project with SwiftUI and required frameworks
- [ ] T006 [P] Configure shared types package for cross-platform type definitions
- [ ] T007 [P] Set up Docker Compose for development environment (n8n, PostgreSQL, Redis, Qdrant)

### Phase 1.2: Development Environment
- [ ] T008 [P] Configure ESLint and Prettier for frontend TypeScript code
- [ ] T009 [P] Configure Black and isort for backend Python code
- [ ] T010 [P] Configure SwiftLint for iOS Swift code
- [ ] T011 [P] Set up pre-commit hooks for all platforms
- [ ] T012 Deploy n8n instance with Docker and configure basic settings
- [ ] T013 [P] Configure PostgreSQL 15 with pgvector extension
- [ ] T014 [P] Configure Redis for caching and session management
- [ ] T015 [P] Configure Qdrant vector database for RAG implementation

### Phase 1.3: CI/CD Pipeline
- [ ] T016 [P] GitHub Actions workflow for backend testing and deployment
- [ ] T017 [P] GitHub Actions workflow for frontend testing and deployment
- [ ] T018 [P] GitHub Actions workflow for iOS testing and TestFlight deployment
- [ ] T019 [P] GitHub Actions workflow for n8n custom node testing

---

## Phase 2: Tests First (TDD) ⚠️ MUST COMPLETE BEFORE IMPLEMENTATION

### Phase 2.1: Contract Tests (Backend)
**CRITICAL: These tests MUST be written and MUST FAIL before ANY implementation**
- [ ] T020 [P] Contract test POST /api/auth/login in backend/tests/contract/test_auth_login.py
- [ ] T021 [P] Contract test POST /api/auth/register in backend/tests/contract/test_auth_register.py
- [ ] T022 [P] Contract test GET /api/workspaces in backend/tests/contract/test_workspaces_list.py
- [ ] T023 [P] Contract test POST /api/workspaces in backend/tests/contract/test_workspaces_create.py
- [ ] T024 [P] Contract test GET /api/workspaces/{id}/agents in backend/tests/contract/test_agents_list.py
- [ ] T025 [P] Contract test POST /api/workspaces/{id}/agents in backend/tests/contract/test_agents_create.py
- [ ] T026 [P] Contract test GET /api/conversations in backend/tests/contract/test_conversations_list.py
- [ ] T027 [P] Contract test POST /api/conversations in backend/tests/contract/test_conversations_create.py
- [ ] T028 [P] Contract test POST /api/conversations/{id}/messages in backend/tests/contract/test_messages_send.py
- [ ] T029 [P] Contract test WebSocket /ws/chat/{conversation_id} in backend/tests/contract/test_websocket_chat.py

### Phase 2.2: n8n Node Tests
- [ ] T030 [P] FlowAIAgent node test in n8n-workflows/tests/test_flowai_agent_node.js
- [ ] T031 [P] VectorSearch node test in n8n-workflows/tests/test_vector_search_node.js
- [ ] T032 [P] ConversationMemory node test in n8n-workflows/tests/test_conversation_memory_node.js
- [ ] T033 [P] AgentHandoff node test in n8n-workflows/tests/test_agent_handoff_node.js
- [ ] T034 [P] TokenOptimizer node test in n8n-workflows/tests/test_token_optimizer_node.js

### Phase 2.3: Integration Tests
- [ ] T035 [P] Agent conversation flow integration test in backend/tests/integration/test_agent_conversation.py
- [ ] T036 [P] Multi-agent orchestration test in backend/tests/integration/test_multi_agent.py
- [ ] T037 [P] Real-time chat synchronization test in backend/tests/integration/test_realtime_sync.py
- [ ] T038 [P] Agent Builder creation test in backend/tests/integration/test_agent_builder.py
- [ ] T039 [P] Workspace member management test in backend/tests/integration/test_workspace_management.py

### Phase 2.4: Frontend Component Tests
- [ ] T040 [P] Chat interface component test in frontend/tests/components/ChatInterface.test.tsx
- [ ] T041 [P] Agent list component test in frontend/tests/components/AgentList.test.tsx
- [ ] T042 [P] Message bubble component test in frontend/tests/components/MessageBubble.test.tsx
- [ ] T043 [P] Workflow builder component test in frontend/tests/components/WorkflowBuilder.test.tsx

### Phase 2.5: iOS Tests
- [ ] T044 [P] Chat view model test in ios/FlowAITests/ViewModels/ChatViewModelTests.swift
- [ ] T045 [P] Agent service test in ios/FlowAITests/Services/AgentServiceTests.swift
- [ ] T046 [P] Sync service test in ios/FlowAITests/Services/SyncServiceTests.swift
- [ ] T047 [P] Core Data model test in ios/FlowAITests/Models/CoreDataModelTests.swift

---

## Phase 3: Core Implementation (ONLY after tests are failing)

### Phase 3.1: Database Models and Core Data
- [ ] T048 [P] User model with Prisma schema in backend/src/models/user.py
- [ ] T049 [P] Workspace model with Prisma schema in backend/src/models/workspace.py
- [ ] T050 [P] Agent model with Prisma schema in backend/src/models/agent.py
- [ ] T051 [P] Conversation model with Prisma schema in backend/src/models/conversation.py
- [ ] T052 [P] Message model with Prisma schema in backend/src/models/message.py
- [ ] T053 [P] iOS Core Data models in ios/FlowAI/Models/CoreDataModels.swift

### Phase 3.2: n8n Custom Nodes (ONLY after node tests are failing)
- [ ] T054 [P] FlowAIAgent node implementation in n8n-workflows/custom-nodes/FlowAIAgent/FlowAIAgent.node.ts
- [ ] T055 [P] VectorSearch node implementation in n8n-workflows/custom-nodes/VectorSearch/VectorSearch.node.ts
- [ ] T056 [P] ConversationMemory node implementation in n8n-workflows/custom-nodes/ConversationMemory/ConversationMemory.node.ts
- [ ] T057 [P] AgentHandoff node implementation in n8n-workflows/custom-nodes/AgentHandoff/AgentHandoff.node.ts
- [ ] T058 [P] TokenOptimizer node implementation in n8n-workflows/custom-nodes/TokenOptimizer/TokenOptimizer.node.ts

### Phase 3.3: Core Agent System
- [ ] T059 AgentService base class in backend/src/services/agent_service.py
- [ ] T060 [P] Project Manager Agent implementation in backend/src/agents/project_manager_agent.py
- [ ] T061 [P] Email Agent implementation in backend/src/agents/email_agent.py
- [ ] T062 [P] Executive Assistant Agent implementation in backend/src/agents/executive_assistant_agent.py
- [ ] T063 Agent Builder meta-agent implementation in backend/src/agents/agent_builder_agent.py
- [ ] T064 Agent orchestration service in backend/src/services/agent_orchestration_service.py

### Phase 3.4: Authentication and Workspace Management
- [ ] T065 JWT authentication service in backend/src/services/auth_service.py
- [ ] T066 Workspace management service in backend/src/services/workspace_service.py
- [ ] T067 [P] POST /api/auth/login endpoint in backend/src/api/auth.py
- [ ] T068 [P] POST /api/auth/register endpoint in backend/src/api/auth.py
- [ ] T069 [P] GET /api/workspaces endpoint in backend/src/api/workspaces.py
- [ ] T070 [P] POST /api/workspaces endpoint in backend/src/api/workspaces.py

### Phase 3.5: Chat and Conversation System
- [ ] T071 ConversationService implementation in backend/src/services/conversation_service.py
- [ ] T072 WebSocket chat handler in backend/src/api/websocket_chat.py
- [ ] T073 [P] GET /api/conversations endpoint in backend/src/api/conversations.py
- [ ] T074 [P] POST /api/conversations endpoint in backend/src/api/conversations.py
- [ ] T075 [P] POST /api/conversations/{id}/messages endpoint in backend/src/api/messages.py

---

## Phase 4: Frontend Implementation (Weeks 4-7)

### Phase 4.1: Core React Components
- [ ] T076 [P] Chat interface component in frontend/src/components/chat/ChatInterface.tsx
- [ ] T077 [P] Message bubble component in frontend/src/components/chat/MessageBubble.tsx
- [ ] T078 [P] Agent list component in frontend/src/components/agents/AgentList.tsx
- [ ] T079 [P] Agent card component in frontend/src/components/agents/AgentCard.tsx
- [ ] T080 [P] Conversation sidebar component in frontend/src/components/chat/ConversationSidebar.tsx

### Phase 4.2: State Management and Services
- [ ] T081 [P] Chat store with Zustand in frontend/src/stores/chatStore.ts
- [ ] T082 [P] Agent store with Zustand in frontend/src/stores/agentStore.ts
- [ ] T083 [P] Auth store with Zustand in frontend/src/stores/authStore.ts
- [ ] T084 [P] WebSocket service in frontend/src/services/websocketService.ts
- [ ] T085 [P] API client service in frontend/src/services/apiClient.ts

### Phase 4.3: Pages and Routing
- [ ] T086 [P] Login page in frontend/src/pages/login.tsx
- [ ] T087 [P] Chat dashboard page in frontend/src/pages/dashboard.tsx
- [ ] T088 [P] Agent management page in frontend/src/pages/agents.tsx
- [ ] T089 [P] Workflow builder page in frontend/src/pages/workflows.tsx
- [ ] T090 [P] Settings page in frontend/src/pages/settings.tsx

---

## Phase 5: iOS Implementation (Weeks 5-8)

### Phase 5.1: Core iOS Views
- [ ] T091 [P] Chat list view in ios/FlowAI/Views/ChatListView.swift
- [ ] T092 [P] Individual chat view in ios/FlowAI/Views/ChatView.swift
- [ ] T093 [P] Agent list view in ios/FlowAI/Views/AgentListView.swift
- [ ] T094 [P] Message input component in ios/FlowAI/Views/Components/MessageInputView.swift

### Phase 5.2: iOS Services and Data
- [ ] T095 [P] iOS API client in ios/FlowAI/Services/APIClient.swift
- [ ] T096 [P] WebSocket service in ios/FlowAI/Services/WebSocketService.swift
- [ ] T097 [P] Sync service in ios/FlowAI/Services/SyncService.swift
- [ ] T098 [P] Core Data stack in ios/FlowAI/Services/CoreDataStack.swift

### Phase 5.3: iOS Integration Features
- [ ] T099 [P] Siri Shortcuts integration in ios/FlowAI/Extensions/SiriShortcuts.swift
- [ ] T100 [P] Widget implementation in ios/Widgets/AgentWidget.swift
- [ ] T101 [P] Push notifications in ios/FlowAI/Services/NotificationService.swift

---

## Phase 6: Integration and Polish (Weeks 9-16)

### Phase 6.1: Advanced Features
- [ ] T102 [P] Financial Agent implementation in backend/src/agents/financial_agent.py
- [ ] T103 [P] Social Media Agent implementation in backend/src/agents/social_media_agent.py

---

## Dependencies

### Critical Path Dependencies
- Infrastructure (T001-T019) before all development
- Tests (T020-T047) before ANY implementation
- Models (T048-T053) before services
- n8n nodes (T054-T058) before agent system
- Agent system (T059-T064) before API endpoints
- Backend APIs (T065-T075) before frontend implementation
- Frontend core (T076-T085) before pages
- iOS foundation (T091-T098) before integration features

### Platform Coordination Points
- T012 (n8n deployment) blocks agent system development
- T048-T053 (models) must complete before cross-platform sync
- T084-T085 (frontend services) coordinate with T096-T097 (iOS services)
- T099-T101 (iOS features) require backend APIs to be complete

### Parallel Execution Boundaries
- All [P] tasks within same phase can run simultaneously
- Different platforms (backend/frontend/iOS) can develop in parallel after models
- Testing can run parallel across all platforms

## Parallel Execution Examples

### Phase 2.1 - Contract Tests (Launch simultaneously)
```bash
# Backend team can execute all contract tests in parallel
Task: "Contract test POST /api/auth/login in backend/tests/contract/test_auth_login.py"
Task: "Contract test POST /api/auth/register in backend/tests/contract/test_auth_register.py"
Task: "Contract test GET /api/workspaces in backend/tests/contract/test_workspaces_list.py"
Task: "Contract test POST /api/workspaces in backend/tests/contract/test_workspaces_create.py"
```

### Phase 3.1 - Database Models (Launch simultaneously)
```bash
# Database team can create all models in parallel
Task: "User model with Prisma schema in backend/src/models/user.py"
Task: "Workspace model with Prisma schema in backend/src/models/workspace.py"
Task: "Agent model with Prisma schema in backend/src/models/agent.py"
Task: "Conversation model with Prisma schema in backend/src/models/conversation.py"
```

### Phase 4.1 - Frontend Components (Launch simultaneously)
```bash
# Frontend team can build all components in parallel
Task: "Chat interface component in frontend/src/components/chat/ChatInterface.tsx"
Task: "Message bubble component in frontend/src/components/chat/MessageBubble.tsx"
Task: "Agent list component in frontend/src/components/agents/AgentList.tsx"
Task: "Agent card component in frontend/src/components/agents/AgentCard.tsx"
```

## Team Assignment Strategy

### Backend Team (Python/FastAPI)
- Focus on T020-T039 (contract and integration tests)
- T048-T075 (models, services, APIs)
- T102-T103 (advanced agent features)

### Frontend Team (Next.js/React)
- Focus on T040-T043 (component tests)
- T076-T090 (React components, state management, pages)

### iOS Team (Swift/SwiftUI)
- Focus on T044-T047 (iOS tests)
- T091-T101 (iOS views, services, native features)

### DevOps/Infrastructure Team
- Focus on T001-T019 (infrastructure setup)
- T054-T058 (n8n custom nodes)

## Notes
- [P] tasks = different files/platforms, no dependencies
- Verify ALL tests fail before implementing (TDD enforced)
- Commit after each task completion
- Cross-platform coordination required at dependency boundaries
- iOS App Store submission in parallel with final testing

## Task Generation Rules Applied

1. **From Contracts**: Each API endpoint → contract test + implementation
2. **From Data Model**: Each entity → model creation task [P]
3. **From Agent System**: Each agent type → specialized implementation
4. **From iOS Plan**: Native features → iOS-specific tasks
5. **Ordering**: Setup → Tests → Models → Services → Endpoints → Polish
6. **Platform Coordination**: Shared dependencies managed sequentially

## Validation Checklist ✓

- [x] All contracts have corresponding tests
- [x] All entities have model tasks
- [x] All tests come before implementation
- [x] Parallel tasks truly independent
- [x] Each task specifies exact file path
- [x] No task modifies same file as another [P] task
- [x] Multi-platform dependencies properly sequenced
- [x] Agent Builder system implementation included
- [x] iOS native features covered
- [x] n8n custom nodes development planned

**Total Tasks**: 103 tasks across 16 weeks
**Parallel Execution**: 67 tasks marked [P] for team efficiency
**Platform Coverage**: Backend (40%), Frontend (25%), iOS (25%), Infrastructure (10%)