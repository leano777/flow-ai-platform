# Flow AI Platform - Complete Development Prompt

## Project Overview

Build **Flow AI Chat** - a revolutionary business operating system that transforms how small to medium-sized teams (5-50 people) interact with AI agents. The platform presents AI agents as contacts in an iMessage-style interface, making enterprise automation as intuitive as texting a colleague.

## Core Vision

Create a platform where businesses can deploy specialized AI agents that have deep access to their documentation and can take real actions. Users interact with these agents through a familiar chat interface, with each agent appearing as a distinct contact in their list. The platform must feel as natural as messaging apps while delivering sophisticated business automation.

## Technical Requirements

### Platform Architecture

**Use n8n as the workflow automation backbone** to accelerate development by 60-70%. n8n will handle:
- Complex agent orchestration
- API integrations (Gmail, Outlook, Slack, etc.)
- Workflow automation and visual design
- Webhook processing and event handling

**Core Technology Stack:**
- **Backend**: FastAPI (Python 3.11+) with WebSocket support
- **Workflow Engine**: n8n (self-hosted with custom nodes)
- **Frontend**: Next.js 14 with React Server Components
- **Database**: PostgreSQL 15 with pgvector extension
- **Vector Store**: Qdrant for RAG implementation
- **Cache**: Redis for session management
- **Message Queue**: Built-in n8n queue with Bull/Redis
- **Primary LLM**: GPT-4 Turbo for complex reasoning
- **Secondary LLM**: Claude 3 Haiku for high-volume operations
- **Deployment**: Docker Compose for development, Kubernetes for production

### Agent Types to Implement

1. **Project Manager Agent** (Orchestrator)
   - Breaks down complex requests into subtasks
   - Delegates to specialized agents
   - Aggregates responses and provides summaries
   - Manages multi-agent collaboration

2. **Financial Agent**
   - Invoice processing and expense tracking
   - Budget analysis and forecasting
   - Financial report generation
   - QuickBooks/Xero integration capability

3. **Email Agent**
   - Email drafting and response suggestions
   - Inbox management and prioritization
   - Gmail and Outlook integration
   - Automated follow-ups and scheduling

4. **Social Media Agent**
   - Content creation and scheduling
   - Engagement monitoring
   - Multi-platform management
   - Analytics and reporting

5. **Executive Assistant Agent**
   - Calendar management
   - Meeting scheduling and coordination
   - Task prioritization
   - Document preparation

### User Interface Requirements

**Chat Interface (iMessage-style):**
- Agent contacts sidebar with avatars and status indicators
- Real-time message streaming with typing indicators
- File attachments and rich media support
- Thread management for complex conversations
- Search across all conversations
- Mobile-responsive design

**Agent Management Dashboard:**
- Visual agent configuration
- Knowledge base upload interface
- Integration settings panel
- Usage analytics and metrics
- Team member permissions

**Visual Workflow Builder:**
- Drag-and-drop workflow design using React Flow
- Pre-built workflow templates
- Real-time workflow testing
- Version control for workflows

### n8n Custom Node Development

Create these custom n8n nodes:

```typescript
// Required custom nodes
1. FlowAIAgent - Main agent execution node
2. VectorSearch - RAG retrieval from Qdrant
3. ConversationMemory - Context persistence
4. AgentHandoff - Multi-agent orchestration
5. TokenOptimizer - LLM cost management
```

Each node must support:
- Workspace isolation
- Error handling with retry logic
- Metrics collection
- Memory scope management (conversation/workspace/none)

### Database Schema Requirements

Implement multi-tenant architecture with these core tables:
- `workspaces` - Tenant isolation and settings
- `agents` - Agent configurations and prompts
- `conversations` - Thread management
- `messages` - Chat history with agent context
- `agent_memory` - Persistent memory storage
- `workflows` - n8n workflow definitions
- `integrations` - OAuth tokens and settings
- `webhook_endpoints` - n8n webhook registry

Include Row-Level Security (RLS) for tenant isolation.

### Integration Requirements

**Priority 1 (MVP):**
- Gmail API (read, send, draft)
- Outlook/Microsoft Graph API
- Google Calendar
- Basic webhook support

**Priority 2 (Post-MVP):**
- Slack (bi-directional messaging)
- Microsoft Teams
- Notion
- Google Drive/Docs
- Dropbox

**Priority 3 (Enterprise):**
- Salesforce
- HubSpot
- QuickBooks
- Custom API integrations

### Security & Compliance

**Authentication & Authorization:**
- OAuth 2.0 with PKCE for all integrations
- JWT tokens with refresh mechanism
- Role-based access control (RBAC)
- Multi-factor authentication (MFA) option
- SSO support (SAML 2.0) for enterprise

**Data Security:**
- AES-256 encryption for stored credentials
- TLS 1.3 for all connections
- End-to-end encryption for sensitive data
- GDPR/CCPA compliance tools
- Audit logging for all actions

**Compliance Targets:**
- SOC 2 Type I (Year 1)
- SOC 2 Type II (Year 2)
- GDPR compliance from launch
- HIPAA ready (future)

### Performance Requirements

**Response Times:**
- Chat message response: <100ms p95
- Agent response: <3 seconds for simple queries
- Workflow execution: <10 seconds for complex tasks
- File upload: Support up to 25MB

**Scalability:**
- Support 10,000+ workspaces
- 100+ concurrent users per workspace
- 1M+ messages per day
- 99.9% uptime SLA

### Development Phases

**Phase 1: MVP (Weeks 1-6)**

*Week 1-2: Infrastructure Setup*
- Deploy n8n with Docker Compose
- Set up PostgreSQL and Redis
- Configure FastAPI backend
- Initialize Next.js frontend
- Create development environment

*Week 3-4: Core Agent System*
- Develop custom n8n nodes for agents
- Implement basic chat flow
- Create agent configuration system
- Build conversation persistence
- Set up WebSocket connections

*Week 5-6: Essential Features*
- Gmail integration via n8n
- Basic chat UI with agent selection
- Simple RAG implementation
- User authentication with Auth0
- Deploy to staging environment

**Deliverables:**
- Working chat with 2 agent types (Email + Executive Assistant)
- Gmail integration functional
- 10 beta users onboarded
- Basic documentation

**Phase 2: Integration Layer (Weeks 7-12)**

*Week 7-8: Extended Integrations*
- Outlook/Microsoft Graph integration
- Calendar synchronization
- Slack connector
- Google Drive access

*Week 9-10: Advanced Agents*
- Financial Agent with calculation abilities
- Social Media Agent with scheduling
- Project Manager orchestration
- Agent memory implementation

*Week 11-12: UI Enhancement*
- Visual workflow builder
- Agent marketplace UI
- Analytics dashboard
- Mobile optimization

**Deliverables:**
- All 5 agent types functional
- 5+ integrations live
- Visual workflow builder
- 100+ beta users

**Phase 3: Production Ready (Weeks 13-16)**

*Week 13-14: Performance & Scaling*
- Kubernetes deployment setup
- Load testing and optimization
- Caching layer implementation
- Database optimization

*Week 15-16: Security & Polish*
- Security audit and fixes
- GDPR compliance tools
- Onboarding flow optimization
- Documentation and training materials

**Deliverables:**
- Production deployment
- 99.9% uptime achieved
- SOC 2 preparation complete
- Public launch ready

### n8n Workflow Templates Required

1. **Master Orchestration Workflow**
   - Receives chat messages
   - Routes to appropriate agent
   - Handles multi-agent collaboration
   - Returns responses to chat

2. **Email Processing Workflow**
   - Monitors inbox via trigger
   - Classifies email importance
   - Generates response suggestions
   - Creates drafts or auto-responds

3. **Document Analysis Workflow**
   - Extracts text from uploads
   - Chunks and embeds content
   - Stores in vector database
   - Updates agent knowledge base

4. **Meeting Scheduler Workflow**
   - Finds available time slots
   - Sends calendar invites
   - Handles rescheduling
   - Sends reminders

5. **Report Generation Workflow**
   - Aggregates data from multiple sources
   - Generates visualizations
   - Creates formatted documents
   - Distributes to stakeholders

### API Endpoints to Implement

```python
# Core Chat APIs
POST   /api/chat/{workspace_id}/message
GET    /api/chat/{workspace_id}/conversations
GET    /api/chat/{workspace_id}/conversation/{id}/messages
DELETE /api/chat/{workspace_id}/conversation/{id}

# Agent Management
GET    /api/agents/{workspace_id}/list
POST   /api/agents/{workspace_id}/create
PUT    /api/agents/{workspace_id}/{agent_id}/update
DELETE /api/agents/{workspace_id}/{agent_id}
POST   /api/agents/{workspace_id}/{agent_id}/train

# Workflow Management
GET    /api/workflows/{workspace_id}/list
POST   /api/workflows/{workspace_id}/create
PUT    /api/workflows/{workspace_id}/{workflow_id}
POST   /api/workflows/{workspace_id}/{workflow_id}/execute
GET    /api/workflows/{workspace_id}/{workflow_id}/history

# Integration Management
GET    /api/integrations/{workspace_id}/available
POST   /api/integrations/{workspace_id}/connect
DELETE /api/integrations/{workspace_id}/{integration_id}
POST   /api/integrations/{workspace_id}/oauth/callback

# Workspace Management
POST   /api/workspace/create
GET    /api/workspace/{id}/settings
PUT    /api/workspace/{id}/settings
POST   /api/workspace/{id}/invite
GET    /api/workspace/{id}/members
```

### WebSocket Events to Handle

```javascript
// Client -> Server
'message.send'
'agent.select'
'conversation.create'
'conversation.archive'
'typing.start'
'typing.stop'
'file.upload'

// Server -> Client
'message.received'
'agent.response'
'agent.thinking'
'agent.error'
'conversation.updated'
'user.joined'
'user.left'
```

### Testing Requirements

**Unit Testing:**
- 80% code coverage minimum
- Test all agent nodes independently
- Mock external API calls
- Test error handling paths

**Integration Testing:**
- Test n8n workflow execution
- Verify API integrations
- Test multi-agent interactions
- Validate webhook processing

**E2E Testing:**
- Complete user flows
- Multi-user scenarios
- Performance under load
- Mobile responsiveness

### Monitoring & Analytics

**Infrastructure Monitoring:**
- n8n execution metrics
- API response times
- Database query performance
- Redis cache hit rates
- LLM token usage

**Business Metrics:**
- Active workspaces
- Messages per day
- Agent utilization
- User engagement
- Feature adoption rates

**Error Tracking:**
- Sentry for error monitoring
- Custom error categorization
- Alert thresholds
- Incident response automation

### Documentation Requirements

1. **Developer Documentation:**
   - API reference with examples
   - n8n node development guide
   - Deployment instructions
   - Architecture diagrams

2. **User Documentation:**
   - Getting started guide
   - Agent configuration tutorials
   - Integration setup guides
   - Video walkthroughs

3. **Internal Documentation:**
   - System architecture
   - Database schema
   - Security protocols
   - Runbooks for common issues

### Success Criteria

**MVP Success Metrics:**
- 50+ active workspaces
- 80% week-over-week retention
- <200ms median response time
- 5+ integrations per workspace

**3-Month Targets:**
- 500+ paying customers
- $50K MRR
- 95% uptime
- NPS score >50

**Year 1 Goals:**
- 10,000+ workspaces
- $500K MRR
- Enterprise tier launched
- SOC 2 Type I certified

### Development Environment Setup

```bash
# Required tools
- Docker Desktop
- Node.js 18+
- Python 3.11+
- PostgreSQL 15
- Redis 7+
- n8n CLI tools

# Environment variables
N8N_WEBHOOK_URL=http://localhost:5678/webhook
DATABASE_URL=postgresql://user:pass@localhost/flowai
REDIS_URL=redis://localhost:6379
OPENAI_API_KEY=your-key
ANTHROPIC_API_KEY=your-key
QDRANT_URL=http://localhost:6333
AUTH0_DOMAIN=your-domain
AUTH0_CLIENT_ID=your-client-id
```

### Team Responsibilities

**Backend Team:**
- n8n custom node development
- API development (FastAPI)
- Database design and optimization
- Integration development
- Security implementation

**Frontend Team:**
- Chat interface (React/Next.js)
- Agent management dashboard
- Visual workflow builder
- Mobile responsiveness
- Real-time WebSocket handling

**DevOps Team:**
- n8n deployment and scaling
- Kubernetes configuration
- CI/CD pipeline setup
- Monitoring and alerting
- Security compliance

**AI/ML Team:**
- Agent prompt engineering
- RAG implementation
- Fine-tuning pipelines
- Performance optimization
- Context management

### Risk Mitigation

**Technical Risks:**
- n8n scalability limits → Plan for custom orchestrator if needed
- LLM costs → Implement aggressive caching and token optimization
- Integration breaking changes → Version lock critical dependencies
- Data privacy concerns → Implement zero-trust architecture

**Business Risks:**
- Slow adoption → Focus on specific industry verticals
- Competition from Microsoft/Google → Differentiate with superior UX
- Compliance requirements → Start SOC 2 process early
- Support burden → Build comprehensive self-service resources

### Launch Strategy

**Beta Launch (Week 6):**
- 10 hand-picked customers
- Daily feedback sessions
- Rapid iteration on core features
- Focus on stability

**Limited Release (Week 12):**
- 100 customers from waitlist
- ProductHunt launch
- Content marketing campaign
- Case study development

**Public Launch (Week 16):**
- Open registration
- Pricing tiers announced
- Affiliate program
- Partner integrations

## Final Notes

This platform combines the simplicity of messaging apps with the power of enterprise automation. By using n8n as the orchestration engine, we can deliver a production-ready MVP in 6-8 weeks instead of 3+ months. The architecture supports rapid iteration while maintaining enterprise-grade security and scalability.

Focus on making the agent interactions feel magical - users should feel like they're chatting with knowledgeable colleagues who can actually get things done, not just chatbots. The visual workflow builder will be a key differentiator, allowing non-technical users to create sophisticated automations.

Remember: We're not just building a chat interface for AI - we're building a new way for businesses to operate, where AI agents are first-class members of the team.