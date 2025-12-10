# Task Completion Checklist

## Before Making Changes
- [ ] Read existing code/files to understand patterns
- [ ] Check git status and current branch
- [ ] Create feature branch if modifying core functionality
- [ ] Understand module responsibilities and dependencies

## During Development
- [ ] Follow existing naming conventions (snake_case, PascalCase)
- [ ] Add module docstrings for new files
- [ ] Maintain modular design (each module independently testable)
- [ ] Use rich.Console for user-facing messages
- [ ] Preserve existing error handling patterns

## Testing (No Formal Test Suite)
- [ ] Test module standalone: `python3 src/module_name.py`
- [ ] Test main installer: `python3 install.py` (use with caution)
- [ ] Verify Python syntax: `python3 -m py_compile src/*.py`
- [ ] Test on target OS if cross-platform changes

## Code Quality
- [ ] No linting configured - manual review required
- [ ] No formatting tool configured - follow existing style
- [ ] Check imports: stdlib → third-party → local
- [ ] Ensure backward compatibility with existing profiles

## Before Committing
- [ ] Review changes: `git diff`
- [ ] Verify no sensitive data in configs/
- [ ] Update CLAUDE.md or README.md if architecture changes
- [ ] Test symlink deployment doesn't break existing setups

## Git Workflow
- [ ] Commit with descriptive message
- [ ] Push to feature branch
- [ ] Test on clean environment if possible
- [ ] Merge to main after validation

## Special Considerations
- **Profile YAML**: Changes affect merging logic - test thoroughly
- **Symlinks**: Breaking changes affect user environments immediately
- **Backups**: Backup directory structure is critical for restore
- **Cross-platform**: Test on both macOS and Linux if applicable
