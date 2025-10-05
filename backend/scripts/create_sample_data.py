"""
Script to populate the database with sample notes and data
"""

import asyncio
from sqlalchemy.orm import Session
from pkm_backend.db.database import SessionLocal, create_tables
from pkm_backend.models.database import Workspace, Note, Tag


def create_sample_data():
    """Create sample workspaces, notes, and tags for testing"""
    
    # Ensure tables exist
    create_tables()
    
    db = SessionLocal()
    
    try:
        # Create sample workspaces
        workspaces = [
            Workspace(
                name="Computer Science",
                description="CS coursework, algorithms, and programming notes",
                color="#3B82F6"
            ),
            Workspace(
                name="Mathematics",
                description="Math concepts, proofs, and problem-solving",
                color="#8B5CF6"
            ),
            Workspace(
                name="Personal Projects",
                description="Ideas and documentation for side projects",
                color="#10B981"
            ),
            Workspace(
                name="Research",
                description="Academic research notes and papers",
                color="#F59E0B"
            ),
            Workspace(
                name="Learning Journal",
                description="Daily learning and reflection notes",
                color="#EF4444"
            )
        ]
        
        for workspace in workspaces:
            existing = db.query(Workspace).filter(Workspace.name == workspace.name).first()
            if not existing:
                db.add(workspace)
        
        db.commit()
        
        # Create sample tags
        tags = [
            Tag(name="algorithms", color="#3B82F6"),
            Tag(name="data-structures", color="#8B5CF6"),
            Tag(name="web-development", color="#10B981"),
            Tag(name="machine-learning", color="#F59E0B"),
            Tag(name="personal", color="#EF4444"),
            Tag(name="important", color="#DC2626"),
            Tag(name="project-idea", color="#059669"),
            Tag(name="study-notes", color="#7C3AED"),
            Tag(name="research", color="#B45309"),
            Tag(name="todo", color="#374151")
        ]
        
        for tag in tags:
            existing = db.query(Tag).filter(Tag.name == tag.name).first()
            if not existing:
                db.add(tag)
        
        db.commit()
        
        # Get workspace IDs
        cs_workspace = db.query(Workspace).filter(Workspace.name == "Computer Science").first()
        math_workspace = db.query(Workspace).filter(Workspace.name == "Mathematics").first()
        projects_workspace = db.query(Workspace).filter(Workspace.name == "Personal Projects").first()
        research_workspace = db.query(Workspace).filter(Workspace.name == "Research").first()
        journal_workspace = db.query(Workspace).filter(Workspace.name == "Learning Journal").first()
        
        # Get tag objects
        algo_tag = db.query(Tag).filter(Tag.name == "algorithms").first()
        ds_tag = db.query(Tag).filter(Tag.name == "data-structures").first()
        web_tag = db.query(Tag).filter(Tag.name == "web-development").first()
        ml_tag = db.query(Tag).filter(Tag.name == "machine-learning").first()
        important_tag = db.query(Tag).filter(Tag.name == "important").first()
        
        # Create sample notes
        notes = [
            # Computer Science Notes
            {
                "title": "Big O Notation Fundamentals",
                "content": """# Big O Notation

## What is Big O?
Big O notation describes the performance or complexity of an algorithm in terms of the size of the input data.

## Common Time Complexities
- **O(1)** - Constant time
- **O(log n)** - Logarithmic time
- **O(n)** - Linear time  
- **O(n log n)** - Linearithmic time
- **O(n²)** - Quadratic time
- **O(2^n)** - Exponential time

## Examples
```python
# O(1) - Constant time
def get_first_element(arr):
    return arr[0]

# O(n) - Linear time
def find_max(arr):
    max_val = arr[0]
    for num in arr:
        if num > max_val:
            max_val = num
    return max_val
```

## Key Points
- Focus on worst-case scenario
- Drop constants and lower-order terms
- Used for comparing algorithm efficiency""",
                "workspace_id": cs_workspace.id,
                "tags": [algo_tag, important_tag]
            },
            
            {
                "title": "Binary Search Tree Implementation",
                "content": """# Binary Search Tree (BST)

## Properties
1. Left subtree contains nodes with keys less than parent
2. Right subtree contains nodes with keys greater than parent
3. Both left and right subtrees are also BSTs

## Implementation in Python
```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class BST:
    def __init__(self):
        self.root = None
    
    def insert(self, val):
        if not self.root:
            self.root = TreeNode(val)
        else:
            self._insert_recursive(self.root, val)
    
    def _insert_recursive(self, node, val):
        if val < node.val:
            if not node.left:
                node.left = TreeNode(val)
            else:
                self._insert_recursive(node.left, val)
        else:
            if not node.right:
                node.right = TreeNode(val)
            else:
                self._insert_recursive(node.right, val)
    
    def search(self, val):
        return self._search_recursive(self.root, val)
    
    def _search_recursive(self, node, val):
        if not node or node.val == val:
            return node
        
        if val < node.val:
            return self._search_recursive(node.left, val)
        else:
            return self._search_recursive(node.right, val)
```

## Time Complexity
- **Search**: O(log n) average, O(n) worst case
- **Insertion**: O(log n) average, O(n) worst case
- **Deletion**: O(log n) average, O(n) worst case""",
                "workspace_id": cs_workspace.id,
                "tags": [ds_tag, algo_tag]
            },
            
            # Mathematics Notes
            {
                "title": "Calculus: Derivatives and Applications",
                "content": """# Derivatives

## Definition
The derivative of a function f(x) at point x is:
$$f'(x) = \\lim_{h \\to 0} \\frac{f(x+h) - f(x)}{h}$$

## Basic Rules
1. **Power Rule**: $(x^n)' = nx^{n-1}$
2. **Product Rule**: $(uv)' = u'v + uv'$
3. **Chain Rule**: $(f(g(x)))' = f'(g(x)) \\cdot g'(x)$
4. **Quotient Rule**: $\\left(\\frac{u}{v}\\right)' = \\frac{u'v - uv'}{v^2}$

## Common Derivatives
- $(\\sin x)' = \\cos x$
- $(\\cos x)' = -\\sin x$
- $(e^x)' = e^x$
- $(\\ln x)' = \\frac{1}{x}$

## Applications
1. **Finding critical points**: Set f'(x) = 0
2. **Optimization problems**: Max/min values
3. **Rate of change**: Velocity, acceleration
4. **Curve sketching**: Increasing/decreasing intervals

## Example Problem
Find the maximum area of a rectangle inscribed in a semicircle of radius r.

**Solution:**
Let the rectangle have width 2x and height y.
Then $x^2 + y^2 = r^2$, so $y = \\sqrt{r^2 - x^2}$

Area = $A = 2x \\cdot y = 2x\\sqrt{r^2 - x^2}$

$A'(x) = 2\\sqrt{r^2 - x^2} + 2x \\cdot \\frac{-x}{\\sqrt{r^2 - x^2}} = \\frac{2(r^2 - 2x^2)}{\\sqrt{r^2 - x^2}}$

Setting $A'(x) = 0$: $r^2 - 2x^2 = 0 \\Rightarrow x = \\frac{r}{\\sqrt{2}}$

Maximum area = $r^2$""",
                "workspace_id": math_workspace.id,
                "tags": [important_tag]
            },
            
            # Personal Projects
            {
                "title": "PKM System Architecture",
                "content": """# Personal Knowledge Management System

## Project Vision
Build a privacy-focused, student-friendly knowledge management system that:
- Stores all data locally for privacy
- Uses AI for text enhancement and search
- Supports Markdown with rich editing
- Exports to PDF and other formats

## Tech Stack
### Backend
- **FastAPI**: Modern Python web framework
- **SQLAlchemy**: Database ORM
- **SQLite**: Local database storage
- **Ollama**: Local LLM integration
- **Pydantic**: Data validation

### Frontend (Planned)
- **Next.js 14**: React framework with App Router
- **TypeScript**: Type-safe JavaScript
- **Tailwind CSS**: Utility-first styling
- **Monaco Editor**: Code/markdown editing
- **React Query**: Data fetching

## Key Features
1. **Notes Management**: CRUD operations for markdown notes
2. **Workspaces**: Organize notes by subject/project
3. **AI Integration**: 
   - Text cleanup and improvement
   - Semantic search
   - Chat with notes
4. **Export System**: PDF, DOCX, HTML export
5. **Privacy-First**: No cloud dependencies

## Database Schema
```sql
-- Workspaces for organization
CREATE TABLE workspaces (
    id INTEGER PRIMARY KEY,
    name VARCHAR(255) UNIQUE,
    description TEXT,
    color VARCHAR(7),
    created_at TIMESTAMP
);

-- Notes with markdown content
CREATE TABLE notes (
    id INTEGER PRIMARY KEY,
    title VARCHAR(500),
    content TEXT,
    workspace_id INTEGER REFERENCES workspaces(id),
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

-- Tags for categorization
CREATE TABLE tags (
    id INTEGER PRIMARY KEY,
    name VARCHAR(100) UNIQUE,
    color VARCHAR(7)
);
```

## Next Steps
1. ✅ Complete backend API
2. 🚧 Build React frontend
3. 📝 Add rich markdown editor
4. 🤖 Enhance AI features
5. 📄 Implement export system
6. 🚀 Package for distribution""",
                "workspace_id": projects_workspace.id,
                "tags": [web_tag, important_tag]
            },
            
            # Research Notes
            {
                "title": "Machine Learning Study Plan",
                "content": """# Machine Learning Study Roadmap

## Phase 1: Foundations (4-6 weeks)
### Mathematics Prerequisites
- **Linear Algebra**: Vectors, matrices, eigenvalues
- **Statistics**: Probability, distributions, hypothesis testing
- **Calculus**: Derivatives, optimization, gradients

### Programming Skills
- **Python**: NumPy, Pandas, Matplotlib
- **Jupyter Notebooks**: Interactive development
- **Git**: Version control basics

## Phase 2: Core ML Concepts (6-8 weeks)
### Supervised Learning
1. **Linear Regression**
   - Cost functions
   - Gradient descent
   - Regularization (L1/L2)

2. **Classification**
   - Logistic regression
   - Decision trees
   - Random forests
   - Support Vector Machines

3. **Model Evaluation**
   - Cross-validation
   - Metrics: Accuracy, Precision, Recall, F1
   - ROC curves, AUC

### Unsupervised Learning
- **Clustering**: K-means, hierarchical
- **Dimensionality Reduction**: PCA, t-SNE
- **Association Rules**: Market basket analysis

## Phase 3: Deep Learning (8-10 weeks)
### Neural Networks
- **Perceptrons**: Basic building blocks
- **Backpropagation**: Learning algorithm
- **Activation Functions**: ReLU, Sigmoid, Tanh

### Deep Architectures
- **Convolutional Neural Networks (CNNs)**
  - Image classification
  - Computer vision applications
- **Recurrent Neural Networks (RNNs)**
  - LSTM, GRU
  - Sequence modeling
  - Natural Language Processing

### Frameworks
- **TensorFlow/Keras**: Industry standard
- **PyTorch**: Research-friendly
- **Scikit-learn**: Traditional ML

## Phase 4: Specialization (6-8 weeks)
Choose one or more areas:
- **Computer Vision**: Object detection, segmentation
- **Natural Language Processing**: Transformers, BERT, GPT
- **Reinforcement Learning**: Q-learning, policy gradients
- **MLOps**: Model deployment, monitoring

## Resources
### Books
- "Hands-On Machine Learning" by Aurélien Géron
- "Pattern Recognition and Machine Learning" by Christopher Bishop
- "Deep Learning" by Ian Goodfellow

### Online Courses
- Andrew Ng's ML Course (Coursera)
- Fast.ai Practical Deep Learning
- CS231n Stanford (Computer Vision)

### Practice Platforms
- Kaggle competitions
- Google Colab for experimentation
- Papers With Code for latest research

## Projects to Build
1. **Housing Price Prediction** (Linear Regression)
2. **Image Classifier** (CNN)
3. **Sentiment Analysis** (NLP)
4. **Recommendation System** (Collaborative Filtering)
5. **Time Series Forecasting** (RNN/LSTM)

## Success Metrics
- Complete 3+ end-to-end projects
- Achieve top 50% in Kaggle competition
- Understand and implement algorithms from scratch
- Build and deploy a real ML application""",
                "workspace_id": research_workspace.id,
                "tags": [ml_tag, important_tag]
            },
            
            # Learning Journal
            {
                "title": "Daily Learning - FastAPI and Modern Python",
                "content": """# Today's Learning: FastAPI and Modern Python Development

## Date: October 5, 2025

## What I Learned Today

### FastAPI Testing
- Discovered that FastAPI has excellent testing support with pytest
- Used `TestClient` from `starlette.testclient` for API testing
- Learned about dependency injection for database testing
- SQLAlchemy can use in-memory SQLite for fast tests

### UV Package Manager
- UV is incredibly fast compared to pip
- `uv sync` installs dependencies from pyproject.toml
- `uv run` executes commands in the virtual environment
- `--extra dev` flag installs optional development dependencies

### Key Commands I Used
```bash
# Install dependencies
uv sync --extra dev

# Run tests with verbose output
uv run pytest -v

# Run specific test file
uv run pytest tests/test_main.py -v

# Run tests with coverage
uv run pytest --cov=pkm_backend
```

## Challenges Faced
1. **Test Fixtures**: Had to properly set up database fixtures for testing
2. **SQLAlchemy Issues**: Some deprecation warnings with declarative_base
3. **Test Isolation**: Making sure each test has a clean database state

## Solutions Found
- Used `@pytest.fixture` for database setup and teardown
- Created separate test database configuration
- Learned about FastAPI dependency overrides for testing

## Tomorrow's Goals
1. Add more comprehensive API tests
2. Set up automated testing with GitHub Actions
3. Add sample data population script
4. Start planning the frontend architecture

## Useful Resources
- [FastAPI Testing Docs](https://fastapi.tiangolo.com/tutorial/testing/)
- [UV Documentation](https://github.com/astral-sh/uv)
- [pytest Documentation](https://docs.pytest.org/)

## Code Snippets That Worked
```python
# FastAPI test client setup
@pytest.fixture
def client(db_session):
    with TestClient(app) as c:
        yield c

# Database dependency override
app.dependency_overrides[get_db] = override_get_db
```

## Reflection
Testing is crucial for maintaining code quality, especially for APIs that will be used by a frontend. The combination of FastAPI + pytest + UV makes for a very smooth development experience. The testing framework is intuitive and the error messages are helpful.

Next week I want to focus on the frontend development and see how the React app will integrate with this backend.""",
                "workspace_id": journal_workspace.id,
                "tags": [web_tag]
            }
        ]
        
        # Add notes to database
        for note_data in notes:
            existing = db.query(Note).filter(Note.title == note_data["title"]).first()
            if not existing:
                tags = note_data.pop("tags", [])
                note = Note(**note_data)
                db.add(note)
                db.commit()
                db.refresh(note)
                
                # Add tags
                for tag in tags:
                    if tag:
                        note.tags.append(tag)
                
                db.commit()
        
        print("✅ Sample data created successfully!")
        print(f"Created {len(workspaces)} workspaces")
        print(f"Created {len(tags)} tags") 
        print(f"Created {len(notes)} notes")
        
    except Exception as e:
        print(f"❌ Error creating sample data: {e}")
        db.rollback()
        
    finally:
        db.close()


if __name__ == "__main__":
    create_sample_data()