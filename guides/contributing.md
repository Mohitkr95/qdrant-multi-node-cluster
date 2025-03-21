# Contributing to Qdrant Multi-Node Cluster

Thank you for your interest in contributing to the Qdrant Multi-Node Cluster project! This document provides guidelines and instructions for contributing.

## Code of Conduct

By participating in this project, you agree to abide by our Code of Conduct, which expects all participants to:

- Be respectful and inclusive
- Exercise consideration and empathy
- Focus on collaborative problem-solving
- Refrain from discriminatory or harassing behavior

## Ways to Contribute

There are many ways to contribute to this project:

1. **Reporting Bugs**: Help improve the project by reporting bugs
2. **Suggesting Enhancements**: Propose new features or improvements
3. **Code Contributions**: Submit pull requests with bug fixes or new features
4. **Documentation**: Improve documentation, fix typos, or add examples
5. **Testing**: Test the project in different environments and report issues
6. **Providing Feedback**: Share your experience using the project

## Getting Started

### Environment Setup

1. **Fork the Repository**
   
   Start by forking the repository to your GitHub account.

2. **Clone Your Fork**
   ```bash
   git clone https://github.com/YOUR_USERNAME/qdrant-multi-node-cluster.git
   cd qdrant-multi-node-cluster
   ```

3. **Set Up Development Environment**
   ```bash
   # Create a virtual environment
   python -m venv env
   
   # Activate the virtual environment
   # On Windows:
   env\Scripts\activate
   # On macOS/Linux:
   source env/bin/activate
   
   # Install dependencies
   pip install -e .
   ```

4. **Create a Feature Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

### Development Workflow

1. **Make Changes**
   - Write your code following the project's style guidelines
   - Add tests for new functionality
   - Update documentation for any changed functionality

2. **Run Tests**
   ```bash
   python -m unittest discover -s tests
   ```

3. **Format Code**
   Ensure your code adheres to PEP 8 style guidelines.

4. **Commit Changes**
   ```bash
   git add .
   git commit -m "Brief description of your changes"
   ```

5. **Push to Your Fork**
   ```bash
   git push origin feature/your-feature-name
   ```

6. **Submit a Pull Request**
   - Go to your fork on GitHub
   - Click "New Pull Request"
   - Select your feature branch
   - Provide a clear description of your changes

## Pull Request Guidelines

When submitting a pull request:

1. **Describe Your Changes**
   - Clearly explain what problem your PR solves
   - Reference any related issues using the GitHub issue number (#123)

2. **Keep PRs Focused**
   - Each PR should address a single concern
   - For multiple unrelated changes, submit separate PRs

3. **Update Documentation**
   - Update relevant documentation to reflect your changes
   - Add comments to complex code sections

4. **Include Tests**
   - Add tests that verify your changes work as expected
   - Ensure all existing tests continue to pass

5. **Be Responsive**
   - Address review comments and feedback promptly
   - Be open to suggestions for improvement

## Style Guidelines

### Code Style

This project follows PEP 8 style guidelines with a few modifications:

- Line length: 100 characters maximum
- Docstrings: Follow Google style docstrings
- Imports: Group and order imports as follows:
  1. Standard library imports
  2. Third-party imports
  3. Local application imports

### Commit Messages

- Use the present tense ("Add feature" not "Added feature")
- Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit the first line to 72 characters or less
- Reference issues and pull requests after the first line

### Documentation Style

- Use Markdown for documentation
- Include code examples where appropriate
- Use clear, concise language
- Organize information logically

## Reporting Bugs

When reporting bugs, please include:

1. **Description**: Clear description of the bug
2. **Steps to Reproduce**: Detailed steps to reproduce the issue
3. **Expected Behavior**: What you expected to happen
4. **Actual Behavior**: What actually happened
5. **Environment**: 
   - Python version
   - Qdrant version
   - Operating system
   - Any other relevant details
6. **Screenshots**: If applicable
7. **Possible Solution**: If you have suggestions

## Feature Requests

For feature requests:

1. **Description**: Clear description of the feature
2. **Rationale**: Why this feature would be beneficial
3. **Example Usage**: How the feature would be used
4. **Alternatives Considered**: Any alternative solutions you've considered

## Community and Communication

- **GitHub Issues**: Use for bug reports and feature requests
- **Pull Requests**: Use for code contributions
- **Discussions**: For general questions and discussions

## Development Setup Tips

### Using Docker for Development

1. **Building Your Development Image**
   ```bash
   docker build -t qdrant-dev -f deployments/docker/Dockerfile.dev .
   ```

2. **Running Development Container**
   ```bash
   docker run -it --rm -v $(pwd):/app qdrant-dev bash
   ```

### Debugging Tips

1. **Enable Debug Logging**
   ```python
   import logging
   logging.basicConfig(level=logging.DEBUG)
   ```

2. **Using Rich for Better Output**
   ```python
   from rich.console import Console
   console = Console()
   console.print("[bold red]Error:[/bold red] Something went wrong")
   ```

## License

By contributing to this project, you agree that your contributions will be licensed under the project's [MIT License](https://github.com/Mohitkr95/qdrant-multi-node-cluster/blob/main/LICENSE).

## Acknowledgments

A big thank you to all contributors who help improve this project! 