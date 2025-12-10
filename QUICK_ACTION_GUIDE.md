# 🚀 Quick Action Guide

**Based on**: [ANALYSIS_REPORT.md](./ANALYSIS_REPORT.md)
**Last Updated**: 2025-12-09

This guide provides immediate, actionable steps to improve your dotfiles codebase based on the comprehensive analysis.

---

## ⚡ Quick Wins (Under 2 Hours)

Start here for immediate improvements:

### 1. Security Scan Setup (30 minutes)

```bash
# Install security scanner
pip install bandit

# Create configuration
cat > .bandit <<EOF
[bandit]
exclude_dirs = ['/tests', '/venv', '/env']
skips = []
EOF

# Run security scan
bandit -r src/ -ll

# Expected output: 2 high-severity issues in tool_installer.py
```

**Action**: Review findings and prioritize fixes

---

### 2. Development Dependencies (15 minutes)

```bash
# Create dev requirements file
cat > requirements-dev.txt <<EOF
# Testing
pytest>=7.4.0
pytest-cov>=4.1.0
pytest-mock>=3.11.1

# Code Quality
black>=23.7.0
mypy>=1.4.1
pylint>=2.17.5
bandit>=1.7.5

# Automation
pre-commit>=3.3.3
EOF

# Install
pip install -r requirements-dev.txt
```

---

### 3. Code Formatting (30 minutes)

```bash
# Format all Python files
black src/ *.py

# Check what would be formatted (dry run)
black --check src/

# Configure black
cat > pyproject.toml <<EOF
[tool.black]
line-length = 100
target-version = ['py38', 'py39', 'py310', 'py311']
include = '\.pyi?$'
exclude = '''
/(
    \.git
  | \.venv
  | env
  | build
  | dist
)/
'''
EOF
```

---

### 4. Add Type Hints to device_detector.py (1 hour)

```bash
# Open device_detector.py and add these imports at the top:
```

```python
from typing import Dict, Optional, Tuple

# Update method signatures:

def is_supported(self) -> Tuple[bool, str]:
    """Check if the current system is supported."""
    # ... implementation

def get_info(self) -> Dict[str, str]:
    """Get all device information as dictionary."""
    # ... implementation

def _detect_os(self) -> str:
    """Detect operating system."""
    # ... implementation

def _detect_architecture(self) -> str:
    """Detect system architecture."""
    # ... implementation

def _detect_distro(self) -> Optional[str]:
    """Detect Linux distribution."""
    # ... implementation

def _detect_package_manager(self) -> Optional[str]:
    """Detect available package manager."""
    # ... implementation

def _command_exists(self, command: str) -> bool:
    """Check if a command exists in PATH."""
    # ... implementation
```

**Verify**:
```bash
mypy src/device_detector.py --ignore-missing-imports
```

---

### 5. Extract Phase Methods in installer.py (1.5 hours)

Current `run()` method is 38 lines. Refactor to:

```python
def run(self):
    """Run the complete installation flow."""
    try:
        self._phase_1_detection()
        profile_type, profile = self._phase_2_configuration()
        conflicts = self._phase_3_conflict_detection(profile)

        if conflicts and not self._confirm_proceed():
            self._cancel_installation()
            return

        self._phase_4_backup(profile, conflicts)
        self._phase_5_tool_installation(profile)
        self._phase_6_config_deployment(profile)
        self._phase_7_completion()

    except KeyboardInterrupt:
        self._handle_interruption()
    except Exception as e:
        self._handle_error(e)

def _phase_1_detection(self):
    """Phase 1: Device detection and system validation."""
    self.print_welcome()
    self.show_device_info()

    if not self.check_system_support():
        sys.exit(1)

    self._show_preflight_checks()

def _phase_2_configuration(self) -> Tuple[str, Dict]:
    """Phase 2: Profile selection and loading."""
    profile_type = self.select_profile_type()
    profile = self.load_profiles(profile_type)
    return profile_type, profile

# ... continue with other phases
```

---

## 🔴 Critical Fixes (Week 1 Priority)

### Fix Shell Injection Vulnerabilities (4 hours)

**File**: `src/tool_installer.py`
**Lines**: 87, 109

#### Issue 1: Oh-My-Zsh Installation

**Before** (VULNERABLE):
```python
# Line 87
f'RUNZSH=no CHSH=no sh -c "$(curl -fsSL {install_script})"'
```

**After** (SECURE):
```python
def install_oh_my_zsh_secure(self) -> bool:
    """Install Oh My Zsh with security validation."""
    import requests
    import hashlib

    install_script_url = "https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh"

    try:
        # 1. Download with SSL verification
        response = requests.get(install_script_url, verify=True, timeout=30)
        response.raise_for_status()
        script_content = response.text

        # 2. Write to temp file
        temp_script = Path("/tmp/oh-my-zsh-install.sh")
        temp_script.write_text(script_content)
        temp_script.chmod(0o755)

        # 3. Execute with controlled environment
        env = os.environ.copy()
        env.update({"RUNZSH": "no", "CHSH": "no"})

        success, output = self.run_command([str(temp_script)])
        temp_script.unlink()  # Cleanup

        if success:
            print("✓ Oh My Zsh installed securely")
        return success

    except Exception as e:
        print(f"✗ Failed to install Oh My Zsh: {e}")
        return False
```

#### Issue 2: Oh-My-Posh Installation

**Before** (VULNERABLE):
```python
# Line 109
install_cmd = "curl -s https://ohmyposh.dev/install.sh | bash -s"
self.run_command(["sh", "-c", install_cmd])
```

**After** (SECURE):
```python
def install_oh_my_posh_secure(self) -> bool:
    """Install Oh My Posh securely."""
    import requests

    if self.package_manager == "brew":
        return self.install_package("oh-my-posh")

    # For apt/pacman, download and verify script
    try:
        script_url = "https://ohmyposh.dev/install.sh"
        response = requests.get(script_url, verify=True, timeout=30)
        response.raise_for_status()

        temp_script = Path("/tmp/oh-my-posh-install.sh")
        temp_script.write_text(response.text)
        temp_script.chmod(0o755)

        success, output = self.run_command([str(temp_script)])
        temp_script.unlink()

        if success:
            print("✓ Oh My Posh installed securely")
        return success

    except Exception as e:
        print(f"✗ Failed to install Oh My Posh: {e}")
        return False
```

**Test Your Fixes**:
```bash
# Run security scan again
bandit -r src/tool_installer.py -ll

# Should show 0 high-severity issues
```

---

## 🧪 Testing Setup (Week 2 Priority)

### 1. Create Test Structure (30 minutes)

```bash
# Create test directory structure
mkdir -p tests/integration

# Create test files
touch tests/__init__.py
touch tests/conftest.py
touch tests/test_device_detector.py
touch tests/test_backup_manager.py
touch tests/test_config_manager.py
touch tests/test_tool_installer.py
touch tests/integration/test_full_workflow.py
```

### 2. Configure pytest (15 minutes)

Create `pytest.ini`:
```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts =
    -v
    --cov=src
    --cov-report=term-missing
    --cov-report=html
    --strict-markers
markers =
    integration: Integration tests (slower)
    unit: Unit tests (fast)
```

### 3. Create Test Fixtures (30 minutes)

**File**: `tests/conftest.py`

```python
import pytest
from pathlib import Path

@pytest.fixture
def temp_dotfiles_root(tmp_path):
    """Create temporary dotfiles directory structure."""
    dotfiles = tmp_path / "dotfiles"
    dotfiles.mkdir()

    (dotfiles / "configs").mkdir()
    (dotfiles / "profiles").mkdir()
    (dotfiles / "backups").mkdir()
    (dotfiles / "src").mkdir()

    return dotfiles

@pytest.fixture
def mock_home(tmp_path, monkeypatch):
    """Mock user home directory."""
    home = tmp_path / "home"
    home.mkdir()

    monkeypatch.setenv("HOME", str(home))
    return home

@pytest.fixture
def sample_profile():
    """Provide sample profile dictionary."""
    return {
        "os": "macos",
        "package_manager": "brew",
        "packages": ["neovim", "kitty", "zsh"],
        "config_paths": {
            "nvim": "~/.config/nvim",
            "kitty": "~/.config/kitty",
            "zsh": "~/.zshrc"
        }
    }
```

### 4. Write First Test (1 hour)

**File**: `tests/test_device_detector.py`

```python
import pytest
from unittest.mock import patch
from src.device_detector import DeviceDetector

class TestDeviceDetector:
    """Test suite for DeviceDetector."""

    def test_init_detects_system_info(self):
        """Verify DeviceDetector initializes with system information."""
        detector = DeviceDetector()

        assert detector.os_type in ["macos", "linux"]
        assert detector.architecture in ["x86_64", "arm64"]
        assert detector.hostname

    @patch('platform.system')
    def test_detect_os_macos(self, mock_system):
        """Verify macOS detection."""
        mock_system.return_value = "Darwin"
        detector = DeviceDetector()
        assert detector.os_type == "macos"

    @patch('platform.system')
    def test_detect_os_linux(self, mock_system):
        """Verify Linux detection."""
        mock_system.return_value = "Linux"
        detector = DeviceDetector()
        assert detector.os_type == "linux"

    def test_get_info_returns_complete_dict(self):
        """Verify get_info returns all required fields."""
        detector = DeviceDetector()
        info = detector.get_info()

        required_keys = ["os", "architecture", "distro",
                        "package_manager", "hostname", "python_version"]
        for key in required_keys:
            assert key in info

    def test_is_supported_returns_tuple(self):
        """Verify is_supported returns (bool, str) tuple."""
        detector = DeviceDetector()
        result = detector.is_supported()

        assert isinstance(result, tuple)
        assert len(result) == 2
        assert isinstance(result[0], bool)
        assert isinstance(result[1], str)
```

### 5. Run Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src

# Run specific test
pytest tests/test_device_detector.py

# Run and generate HTML coverage report
pytest --cov=src --cov-report=html
open htmlcov/index.html  # View coverage report
```

---

## 📊 Progress Tracking

### Week 1 Checklist

- [ ] Security scan setup (bandit)
- [ ] Dev dependencies installed
- [ ] Code formatted with black
- [ ] Type hints added to device_detector.py
- [ ] Shell injection vulnerabilities fixed
- [ ] Security scan passes

**Goal**: Critical security issues resolved

---

### Week 2 Checklist

- [ ] Test structure created
- [ ] pytest configured
- [ ] Test fixtures written
- [ ] device_detector tests (5+ tests)
- [ ] backup_manager tests (5+ tests)
- [ ] config_manager tests (5+ tests)
- [ ] Tests passing, coverage >40%

**Goal**: Testing infrastructure established

---

### Week 3 Checklist

- [ ] installer.py refactored (phases extracted)
- [ ] tool_installer tests written
- [ ] installer tests written
- [ ] All modules have type hints
- [ ] Code coverage >60%
- [ ] mypy passes

**Goal**: Code quality improved, maintainable codebase

---

## 🎯 Success Metrics

Track these metrics weekly:

```bash
# 1. Test Coverage
pytest --cov=src --cov-report=term | grep TOTAL

# 2. Type Coverage
mypy src/ --ignore-missing-imports --strict | grep "Success"

# 3. Code Quality
pylint src/ | grep "Your code has been rated"

# 4. Security Issues
bandit -r src/ -ll | grep "Total issues"
```

**Target Metrics**:
- Test Coverage: >60%
- Pylint Score: >8.0/10
- Security Issues: 0 high/critical
- Type Coverage: 100%

---

## 💡 Tips & Best Practices

### When Writing Tests

1. **Test one thing at a time** - Single assertion per test when possible
2. **Use descriptive names** - `test_backup_creates_timestamped_directory()`
3. **Arrange-Act-Assert** - Clear test structure
4. **Mock external dependencies** - Don't hit real filesystem/network
5. **Test edge cases** - Missing files, invalid input, etc.

### When Adding Type Hints

1. **Start with return types** - Most valuable for understanding
2. **Add parameter types** - Helps catch bugs early
3. **Use Optional[] for nullable** - Be explicit about None
4. **Import from typing** - Dict, List, Tuple, Optional
5. **Run mypy frequently** - Catch errors as you go

### When Refactoring

1. **Write tests first** - Ensure you don't break functionality
2. **Small commits** - One logical change at a time
3. **Run tests after each change** - Immediate feedback
4. **Keep it simple** - Don't over-engineer
5. **Document complex logic** - Help future maintainers

---

## 🆘 Troubleshooting

### Tests Failing

```bash
# Run with verbose output
pytest -v

# Run single test
pytest tests/test_device_detector.py::TestDeviceDetector::test_init_detects_system_info

# Run with print statements visible
pytest -s

# Stop at first failure
pytest -x
```

### Type Checking Errors

```bash
# Show detailed error messages
mypy src/device_detector.py --show-error-codes

# Ignore missing imports
mypy src/ --ignore-missing-imports

# Less strict mode (start here)
mypy src/ --ignore-missing-imports --no-strict-optional
```

### Import Errors in Tests

```bash
# Add src to Python path
export PYTHONPATH="${PYTHONPATH}:${PWD}"

# Or use pytest plugin
pip install pytest-pythonpath

# Add to pytest.ini:
# pythonpath = src
```

---

## 📚 Next Steps

After completing Week 1-3 actions:

1. **Review [ANALYSIS_REPORT.md](./ANALYSIS_REPORT.md)** for detailed recommendations
2. **Implement async package installation** (Week 4)
3. **Add rollback mechanism** (Week 5)
4. **Set up CI/CD** (Week 6)

---

## ✅ Completion Checklist

Mark off as you complete:

### Immediate (Today)
- [ ] Run security scan with bandit
- [ ] Install dev dependencies
- [ ] Format code with black
- [ ] Read ANALYSIS_REPORT.md sections 1-3

### Week 1
- [ ] Fix shell injection in tool_installer.py
- [ ] Add type hints to device_detector.py
- [ ] Run mypy and fix any errors
- [ ] Security scan passes (0 high-severity issues)

### Week 2
- [ ] Create test structure and conftest.py
- [ ] Write tests for device_detector.py (5+ tests)
- [ ] Write tests for backup_manager.py (5+ tests)
- [ ] Write tests for config_manager.py (5+ tests)
- [ ] Achieve 40%+ test coverage

### Week 3
- [ ] Refactor installer.py:run() into phase methods
- [ ] Write tests for tool_installer.py
- [ ] Write tests for installer.py
- [ ] Add type hints to remaining modules
- [ ] Achieve 60%+ test coverage

---

**Questions?** Refer to [ANALYSIS_REPORT.md](./ANALYSIS_REPORT.md) for comprehensive details on any recommendation.

**Need help?** Ask specific questions like:
- "Show me how to write tests for backup_manager.py"
- "How do I implement the secure install_oh_my_zsh function?"
- "Explain the type hints needed for config_manager.py"
