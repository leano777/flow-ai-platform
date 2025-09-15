# Flow AI Platform - Revolutionary Business Operating System

<div align="center">

![Flow AI Logo](https://img.shields.io/badge/Flow%20AI-Platform-blue?style=for-the-badge)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)
[![GitHub Stars](https://img.shields.io/github/stars/your-username/flow-ai-platform?style=for-the-badge)](https://github.com/your-username/flow-ai-platform/stargazers)

**Transform your business with AI agents that work like team members**

[🚀 Quick Start](#quick-start) • [📖 Documentation](#documentation) • [🤝 Contributing](#contributing) • [💬 Community](#community)

</div>

## 🌟 Overview

Flow AI Platform is a revolutionary business operating system that transforms how small to medium-sized teams (5-50 people) interact with AI agents. The platform presents specialized AI agents as contacts in an iMessage-style interface, making enterprise automation as intuitive as texting a colleague.

### ✨ Key Features

- **🤖 AI Agents as Team Members**: Not chatbots, but actual business teammates with specific roles
- **💬 iMessage-Style Interface**: Familiar chat experience requiring zero training
- **⚡ Real Action Capability**: Agents send emails, create calendar events, process invoices
- **🎨 Visual Workflow Builder**: Non-technical users create sophisticated automations
- **🧠 Agent Builder System**: Meta-agent creates specialized agents automatically
- **📱 Cross-Platform**: Web app + native iPhone app with full feature parity

### 🎯 Agent Types

| Agent | Specialization | Key Capabilities |
|-------|---------------|------------------|
| **Project Manager** | Orchestration | Task delegation, progress tracking, team coordination |
| **Financial Agent** | Finance Operations | Invoice processing, budget analysis, forecasting |
| **Email Agent** | Communication | Email drafting, inbox management, automated responses |
| **Social Media Agent** | Marketing | Content creation, scheduling, engagement monitoring |
| **Executive Assistant** | Administration | Calendar management, meeting coordination, travel planning |
| **Agent Builder** | Meta-Development | Creates new specialized agents automatically |

## 🏗️ Architecture

```mermaid
graph TB
    subgraph "Frontend Layer"
        WEB[Web App - Next.js 14]
        iOS[iOS App - SwiftUI]
    end

    subgraph "Backend Layer"
        API[FastAPI Backend]
        AUTH[Authentication Service]
        CHAT[Chat Service]
    end

    subgraph "AI & Workflow Layer"
        N8N[n8n Workflow Engine]
        AGENTS[AI Agent System]
        LLM[LLM Providers]
    end

    subgraph "Data Layer"
        DB[(PostgreSQL + pgvector)]
        VECTOR[(Qdrant Vector DB)]
        CACHE[(Redis Cache)]
    end

    WEB --> API
    iOS --> API
    API --> AUTH
    API --> CHAT
    CHAT --> N8N
    N8N --> AGENTS
    AGENTS --> LLM
    API --> DB
    AGENTS --> VECTOR
    API --> CACHE
```

## 🚀 Quick Start

### Prerequisites

- **Docker & Docker Compose** - Container orchestration
- **Node.js 18+** - Frontend development
- **Python 3.11+** - Backend development
- **Xcode 15+** - iOS development (macOS only)

### 1. Clone and Setup

```bash
git clone https://github.com/your-username/flow-ai-platform.git
cd flow-ai-platform

# Copy environment configuration
cp .env.example .env
```

### 2. Configure Environment

```bash
# .env - Add your API keys
OPENAI_API_KEY=your_openai_key
ANTHROPIC_API_KEY=your_anthropic_key
DATABASE_URL=postgresql://user:pass@localhost:5432/flowai
REDIS_URL=redis://localhost:6379
N8N_BASIC_AUTH_PASSWORD=your_secure_password
```

### 3. Start Development Environment

```bash
# Start all services
docker-compose up -d

# Install dependencies
npm install                 # Frontend
cd backend && poetry install # Backend
```

### 4. Access Applications

- **Web App**: http://localhost:3000
- **API Documentation**: http://localhost:8000/docs
- **n8n Workflow Builder**: http://localhost:5678
- **Database Admin**: http://localhost:8080

## 📁 Project Structure

```
flow-ai-platform/
├── 📄 README.md                    # This file
├── 🔧 docker-compose.yml          # Development environment
├── 📋 .specify/                   # GitHub Spec Kit specifications
│   ├── spec.md                   # Platform specification
│   ├── plan.md                   # Technical implementation plan
│   ├── tasks.md                  # 103-task breakdown
│   └── agent-*.md               # Agent specifications
├── 🔙 backend/                    # FastAPI backend
│   ├── src/                      # Source code
│   ├── tests/                    # Test suites
│   └── alembic/                  # Database migrations
├── 🎨 frontend/                   # Next.js web application
│   ├── src/                      # React components
│   ├── tests/                    # Frontend tests
│   └── public/                   # Static assets
├── 📱 ios/                        # Native iOS application
│   ├── FlowAI/                   # SwiftUI app
│   └── FlowAITests/              # iOS tests
├── 🔄 n8n-workflows/             # Workflow automation
│   ├── custom-nodes/             # Custom n8n nodes
│   └── templates/                # Workflow templates
├── 🤝 shared/                     # Shared types and contracts
│   ├── types/                    # TypeScript definitions
│   └── contracts/                # API contracts
└── 📚 docs/                       # Documentation
```

## 🛠️ Development

### Backend Development

```bash
cd backend

# Install dependencies
poetry install

# Run development server
poetry run uvicorn src.main:app --reload --port 8000

# Run tests
poetry run pytest

# Database migrations
poetry run alembic upgrade head
```

### Frontend Development

```bash
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev

# Run tests
npm run test

# Build for production
npm run build
```

### iOS Development

```bash
cd ios

# Open in Xcode
open FlowAI.xcodeproj

# Or build from command line
xcodebuild -project FlowAI.xcodeproj -scheme FlowAI build
```

### n8n Custom Nodes

```bash
cd n8n-workflows/custom-nodes

# Build custom nodes
npm run build

# Link to n8n instance
npm run dev
```

## 🤖 AI Agent Development

### Creating New Agents

Flow AI Platform includes an **Agent Builder** meta-agent that can create specialized agents automatically. However, you can also create agents manually:

```python
# Example: Customer Support Agent
from src.agents.base import BaseAgent

class CustomerSupportAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Customer Support Agent",
            description="Handles customer inquiries with knowledge base integration",
            capabilities=[
                "ticket_classification",
                "knowledge_base_search",
                "response_generation",
                "escalation_routing"
            ]
        )

    async def process_message(self, message: str, context: dict) -> str:
        # Agent implementation
        pass
```

### Agent Coordination

All agents coordinate through the **FELIX Project Manager Agent**:

```typescript
interface AgentMessage {
  agent: string;
  taskId: string;
  status: 'ACKNOWLEDGED' | 'IN_PROGRESS' | 'COMPLETED' | 'BLOCKED';
  message: string;
  progress?: number;
  estimatedCompletion?: string;
}
```

## 📊 Monitoring & Analytics

### Health Dashboard

Monitor your Flow AI Platform deployment:

- **System Health**: http://localhost:3000/admin/health
- **Agent Performance**: http://localhost:3000/admin/agents
- **Usage Analytics**: http://localhost:3000/admin/analytics

### Key Metrics

- **Response Time**: < 200ms API responses
- **Agent Effectiveness**: 90% successful task completion
- **User Engagement**: 80% daily active users
- **System Uptime**: 99.9% availability

## 🔒 Security

Flow AI Platform implements enterprise-grade security:

- **🔐 Authentication**: JWT with refresh tokens, OAuth2, MFA support
- **🛡️ Authorization**: Role-based access control (RBAC)
- **🔒 Encryption**: AES-256 at rest, TLS 1.3 in transit
- **🕵️ Monitoring**: Real-time threat detection and incident response
- **📋 Compliance**: GDPR, CCPA, SOC 2 ready

### Security Reporting

Found a security vulnerability? Please email security@flowai.com

## 🧪 Testing

### Test Coverage Requirements

- **Unit Tests**: 80% minimum coverage
- **Integration Tests**: 70% coverage for critical paths
- **E2E Tests**: 90% coverage for user journeys

### Running Tests

```bash
# All tests
npm run test:all

# Platform-specific tests
npm run test:backend    # Python tests
npm run test:frontend   # React tests
npm run test:ios        # Swift tests
npm run test:e2e        # End-to-end tests
```

## 🚀 Deployment

### Production Deployment

```bash
# Build all platforms
npm run build:all

# Deploy to production
npm run deploy:production

# Deploy specific platforms
npm run deploy:backend
npm run deploy:frontend
npm run deploy:ios
```

### Environment Configuration

| Environment | URL | Purpose |
|-------------|-----|---------|
| Development | localhost:3000 | Local development |
| Staging | staging.flowai.com | Pre-production testing |
| Production | app.flowai.com | Live application |

## 📖 Documentation

### Developer Documentation

- **[API Reference](docs/api.md)** - Complete API documentation
- **[Agent Development Guide](docs/agents.md)** - Creating custom agents
- **[Workflow Builder Guide](docs/workflows.md)** - Building n8n workflows
- **[Mobile Development](docs/ios.md)** - iOS app development
- **[Deployment Guide](docs/deployment.md)** - Production deployment

### User Documentation

- **[Getting Started](docs/getting-started.md)** - User onboarding guide
- **[Agent Configuration](docs/agent-config.md)** - Setting up agents
- **[Integration Setup](docs/integrations.md)** - Connecting business tools
- **[Troubleshooting](docs/troubleshooting.md)** - Common issues and solutions

## 🤝 Contributing

We welcome contributions! Please read our [Contributing Guide](CONTRIBUTING.md) before submitting pull requests.

### Development Process

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

### Code Standards

- **Backend**: Black formatting, 80% test coverage, type hints
- **Frontend**: ESLint/Prettier, 80% test coverage, TypeScript strict mode
- **iOS**: SwiftLint, 80% test coverage, Swift 5.9+
- **Documentation**: Clear README updates for new features

## 💬 Community

### Get Help

- **📖 Documentation**: [docs.flowai.com](https://docs.flowai.com)
- **💬 Discord**: [Join our community](https://discord.gg/flowai)
- **🐛 Issues**: [GitHub Issues](https://github.com/your-username/flow-ai-platform/issues)
- **📧 Email**: support@flowai.com

### Stay Updated

- **🐦 Twitter**: [@FlowAIPlatform](https://twitter.com/FlowAIPlatform)
- **📰 Blog**: [blog.flowai.com](https://blog.flowai.com)
- **📱 Newsletter**: [Subscribe](https://flowai.com/newsletter)

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **GitHub Spec Kit** - Spec-driven development methodology
- **n8n.io** - Workflow automation platform
- **OpenAI & Anthropic** - AI model providers
- **React & Next.js** - Frontend framework
- **FastAPI** - Backend framework

---

<div align="center">

**[⭐ Star this repo](https://github.com/your-username/flow-ai-platform) if you find Flow AI Platform useful!**

*Built with ❤️ by the Flow AI team*

</div>