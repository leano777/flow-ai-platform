# Contributing to Flow AI Platform

Thank you for your interest in contributing to Flow AI Platform! This document provides guidelines and information for contributors.

## 🎯 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Process](#development-process)
- [Code Standards](#code-standards)
- [Testing Requirements](#testing-requirements)
- [Submitting Changes](#submitting-changes)
- [AI Agent Development](#ai-agent-development)

## Code of Conduct

By participating in this project, you agree to abide by our Code of Conduct:

- **Be respectful** and inclusive in all interactions
- **Be collaborative** and help others learn and grow
- **Be constructive** in feedback and discussions
- **Be patient** with new contributors and questions

## Getting Started

### Prerequisites

- **Git** - Version control
- **Docker & Docker Compose** - Container orchestration
- **Node.js 18+** - Frontend development
- **Python 3.11+** - Backend development
- **Xcode 15+** - iOS development (macOS only)

### Setting Up Development Environment

1. **Fork and clone the repository**:
   ```bash
   git clone https://github.com/your-username/flow-ai-platform.git
   cd flow-ai-platform
   ```

2. **Copy environment configuration**:
   ```bash
   cp .env.example .env
   # Edit .env with your API keys and configuration
   ```

3. **Start development environment**:
   ```bash
   docker-compose up -d
   ```

4. **Install dependencies**:
   ```bash
   # Frontend
   cd frontend && npm install

   # Backend
   cd backend && poetry install

   # iOS (macOS only)
   cd ios && open FlowAI.xcodeproj
   ```

## Development Process

### Branch Strategy

We use a **Git Flow** approach:

- **`main`** - Production-ready code
- **`develop`** - Integration branch for features
- **`feature/`** - Feature development branches
- **`hotfix/`** - Critical production fixes
- **`release/`** - Release preparation branches

### Creating a Feature Branch

```bash
# Start from develop branch
git checkout develop
git pull origin develop

# Create feature branch
git checkout -b feature/your-feature-name

# Make your changes and commit
git add .
git commit -m "feat: add amazing new feature"

# Push and create PR
git push origin feature/your-feature-name
```

### Commit Message Format

We follow **Conventional Commits** specification:

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

**Types**:
- `feat` - New feature
- `fix` - Bug fix
- `docs` - Documentation changes
- `style` - Code style changes
- `refactor` - Code refactoring
- `test` - Adding or updating tests
- `chore` - Maintenance tasks

**Examples**:
```bash
feat(backend): add user authentication API
fix(frontend): resolve chat message rendering issue
docs(readme): update installation instructions
test(ios): add unit tests for chat view model
```

## Code Standards

### Backend (Python)

- **Formatting**: Use `black` and `isort`
- **Linting**: Use `flake8` and `mypy`
- **Type Hints**: Required for all functions
- **Documentation**: Docstrings for all public functions

```python
from typing import Optional

def calculate_score(user_id: str, context: Optional[dict] = None) -> float:
    """Calculate user engagement score.

    Args:
        user_id: Unique identifier for the user
        context: Optional context data for calculation

    Returns:
        Calculated score between 0.0 and 1.0

    Raises:
        ValueError: If user_id is invalid
    """
    pass
```

**Run quality checks**:
```bash
cd backend
poetry run black .
poetry run isort .
poetry run flake8 .
poetry run mypy .
```

### Frontend (TypeScript/React)

- **Formatting**: Use `prettier`
- **Linting**: Use `eslint`
- **TypeScript**: Strict mode enabled
- **Components**: Use functional components with hooks

```typescript
interface ChatMessageProps {
  message: Message;
  isOwn: boolean;
  onReply?: (messageId: string) => void;
}

export const ChatMessage: React.FC<ChatMessageProps> = ({
  message,
  isOwn,
  onReply
}) => {
  const handleReply = useCallback(() => {
    onReply?.(message.id);
  }, [message.id, onReply]);

  return (
    <div className={`message ${isOwn ? 'message--own' : 'message--other'}`}>
      {/* Component implementation */}
    </div>
  );
};
```

**Run quality checks**:
```bash
cd frontend
npm run lint
npm run type-check
npm run format
```

### iOS (Swift)

- **Formatting**: Use `SwiftLint`
- **Architecture**: MVVM with Combine
- **Documentation**: Swift DocC comments

```swift
/// Manages chat conversation state and interactions
@MainActor
class ChatViewModel: ObservableObject {
    @Published var messages: [Message] = []
    @Published var isLoading = false

    private let chatService: ChatService

    /// Initialize with chat service dependency
    /// - Parameter chatService: Service for chat operations
    init(chatService: ChatService) {
        self.chatService = chatService
    }

    /// Send a message to the current conversation
    /// - Parameter content: Message content to send
    func sendMessage(_ content: String) async {
        // Implementation
    }
}
```

**Run quality checks**:
```bash
cd ios
swiftlint
```

## Testing Requirements

### Test Coverage Requirements

- **Unit Tests**: 80% minimum coverage
- **Integration Tests**: 70% coverage for critical paths
- **E2E Tests**: 90% coverage for user journeys

### Backend Testing

```python
# tests/test_user_service.py
import pytest
from src.services.user_service import UserService

class TestUserService:
    @pytest.fixture
    def user_service(self):
        return UserService()

    async def test_create_user_success(self, user_service):
        # Given
        user_data = {"email": "test@example.com", "name": "Test User"}

        # When
        result = await user_service.create_user(user_data)

        # Then
        assert result.email == "test@example.com"
        assert result.id is not None
```

**Run tests**:
```bash
cd backend
poetry run pytest --cov=src --cov-report=html
```

### Frontend Testing

```typescript
// __tests__/ChatMessage.test.tsx
import { render, screen, fireEvent } from '@testing-library/react';
import { ChatMessage } from '../ChatMessage';

describe('ChatMessage', () => {
  const mockMessage = {
    id: '1',
    content: 'Hello world',
    timestamp: new Date(),
    senderType: 'user' as const
  };

  it('renders message content', () => {
    render(<ChatMessage message={mockMessage} isOwn={true} />);

    expect(screen.getByText('Hello world')).toBeInTheDocument();
  });

  it('calls onReply when reply button clicked', () => {
    const onReply = jest.fn();
    render(<ChatMessage message={mockMessage} isOwn={false} onReply={onReply} />);

    fireEvent.click(screen.getByRole('button', { name: /reply/i }));

    expect(onReply).toHaveBeenCalledWith('1');
  });
});
```

**Run tests**:
```bash
cd frontend
npm run test
npm run test:coverage
```

### iOS Testing

```swift
// FlowAITests/ChatViewModelTests.swift
import XCTest
@testable import FlowAI

class ChatViewModelTests: XCTestCase {
    var viewModel: ChatViewModel!
    var mockChatService: MockChatService!

    override func setUp() {
        super.setUp()
        mockChatService = MockChatService()
        viewModel = ChatViewModel(chatService: mockChatService)
    }

    func testSendMessage() async {
        // Given
        let messageContent = "Test message"

        // When
        await viewModel.sendMessage(messageContent)

        // Then
        XCTAssertEqual(mockChatService.sentMessages.count, 1)
        XCTAssertEqual(mockChatService.sentMessages.first?.content, messageContent)
    }
}
```

**Run tests**:
```bash
cd ios
xcodebuild test -project FlowAI.xcodeproj -scheme FlowAI -destination 'platform=iOS Simulator,name=iPhone 15 Pro'
```

## Submitting Changes

### Pull Request Process

1. **Create feature branch** from `develop`
2. **Make your changes** following code standards
3. **Add tests** for new functionality
4. **Update documentation** if needed
5. **Run all tests** and quality checks
6. **Create pull request** with descriptive title and description

### Pull Request Template

```markdown
## Description
Brief description of changes and motivation.

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Unit tests added/updated
- [ ] Integration tests added/updated
- [ ] E2E tests added/updated
- [ ] Manual testing completed

## Quality Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Comments added for complex logic
- [ ] Documentation updated
- [ ] No breaking changes (or marked as such)

## Screenshots (if applicable)
Add screenshots for UI changes.
```

### Review Process

1. **Automated Checks**: All CI/CD checks must pass
2. **Code Review**: At least one approval required
3. **Testing**: All tests must pass
4. **Documentation**: Updates reviewed for clarity
5. **Security**: Security implications assessed

## AI Agent Development

### Creating New Agents

Flow AI Platform uses a specialized agent architecture. To create new agents:

1. **Use Agent Builder**: The recommended approach
   ```typescript
   // Example: Request new agent via Agent Builder
   const newAgent = await agentBuilder.createAgent({
     name: "Customer Support Agent",
     description: "Handles customer inquiries and support tickets",
     capabilities: ["ticket_classification", "knowledge_search"],
     industry: "general"
   });
   ```

2. **Manual Agent Creation**: For custom implementations
   ```python
   # backend/src/agents/custom_agent.py
   from src.agents.base import BaseAgent

   class CustomAgent(BaseAgent):
       def __init__(self):
           super().__init__(
               name="Custom Agent",
               description="Handles specific custom tasks",
               capabilities=["custom_capability"]
           )

       async def process_message(self, message: str, context: dict) -> str:
           # Agent implementation
           pass
   ```

### Agent Testing

All agents must include comprehensive tests:

```python
# tests/agents/test_custom_agent.py
class TestCustomAgent:
    async def test_agent_responds_correctly(self):
        agent = CustomAgent()
        response = await agent.process_message("test input", {})
        assert response is not None
        assert len(response) > 0
```

### Agent Documentation

Document your agent's capabilities:

```yaml
# agents/custom_agent.yaml
name: Custom Agent
description: Detailed description of agent capabilities
version: 1.0.0
capabilities:
  - capability_1: Description of what this does
  - capability_2: Description of another capability
examples:
  - input: "Example user input"
    output: "Expected agent response"
```

## Help and Support

### Getting Help

- **Documentation**: Check [docs](./docs/) directory
- **Issues**: Search existing [GitHub Issues](https://github.com/your-username/flow-ai-platform/issues)
- **Discussions**: Join [GitHub Discussions](https://github.com/your-username/flow-ai-platform/discussions)
- **Discord**: Join our [Discord server](https://discord.gg/flowai)

### Reporting Bugs

Use the bug report template:

```markdown
**Bug Description**
Clear description of the bug.

**Steps to Reproduce**
1. Go to '...'
2. Click on '....'
3. See error

**Expected Behavior**
What you expected to happen.

**Environment**
- OS: [e.g. macOS, Windows, Linux]
- Browser: [if applicable]
- Version: [e.g. 1.0.0]
```

### Feature Requests

Use the feature request template:

```markdown
**Problem Statement**
What problem does this solve?

**Proposed Solution**
Describe your proposed solution.

**Alternatives Considered**
Other solutions you've considered.

**Additional Context**
Screenshots, mockups, etc.
```

## Recognition

Contributors will be recognized in:

- **README.md** - Contributors section
- **CHANGELOG.md** - Release notes
- **GitHub** - Contributor graphs and statistics
- **Discord** - Special contributor role

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to Flow AI Platform! 🚀