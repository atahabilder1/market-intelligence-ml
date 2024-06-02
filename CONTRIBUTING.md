# Contributing to Market Intelligence ML

Thank you for your interest in contributing to this project! This document provides guidelines for contributing.

## Development Setup

1. **Fork and Clone**
   ```bash
   git clone https://github.com/yourusername/market-intelligence-ml.git
   cd market-intelligence-ml
   ```

2. **Create Virtual Environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   make install
   # OR
   pip install -r requirements.txt
   pip install -e .
   ```

## Code Standards

### Python Style
- Follow PEP 8 guidelines
- Use type hints where appropriate
- Maximum line length: 100 characters
- Use docstrings for all functions and classes

### Formatting
```bash
# Format code
make format

# Check linting
make lint
```

### Testing
- Write unit tests for new features
- Maintain test coverage above 80%
- Run tests before submitting PR

```bash
make test
```

## Contribution Workflow

1. **Create a Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make Changes**
   - Write clean, documented code
   - Add tests for new functionality
   - Update documentation if needed

3. **Commit**
   ```bash
   git add .
   git commit -m "Add feature: description"
   ```

4. **Push and Create PR**
   ```bash
   git push origin feature/your-feature-name
   ```

## Areas for Contribution

### High Priority
- [ ] Additional feature engineering techniques
- [ ] Alternative model architectures
- [ ] Enhanced backtesting metrics
- [ ] Performance optimizations

### Medium Priority
- [ ] Additional data sources integration
- [ ] Visualization improvements
- [ ] Documentation enhancements
- [ ] Code refactoring

### Low Priority
- [ ] Example notebooks
- [ ] Deployment scripts
- [ ] CI/CD improvements

## Questions?

Open an issue or reach out via GitHub discussions.

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
