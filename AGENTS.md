# AGENTS.md

## Project Overview

This is a collection of AI agent skills focused on testing, development, and engineering tasks. The project provides specialized knowledge and workflows for AI coding agents to help with E2E testing, systematic learning, and code quality.

**Key Components:**
- Skills repository with markdown-based skill definitions
- Integration with skills.sh for agent skill management
- Focus on Playwright extension testing, lesson decision records, and API documentation fetching
- Git-based distribution and versioning

**Architecture:**
- `skills/`: Contains individual skill packages
- Each skill has `SKILL.md` (core skill definition) and `README.md` (documentation)
- No build process - pure markdown files
- Works with any agent supporting the Agent Skills spec

## Development Workflow

**Adding New Skills:**
1. Create new directory under `skills/`
2. Add `SKILL.md` with skill definition and supporting files
3. Add `README.md` with skill documentation
4. Update main README.md with new skill
5. Test skill integration with agents

**Modifying Existing Skills:**
1. Edit `SKILL.md` files directly
2. Update documentation in corresponding `README.md`
3. Test changes with agent integration
4. Commit changes with descriptive messages

**File Organization:**
- Skills are organized by function in `skills/` directory
- Each skill is self-contained with its own documentation
- Use descriptive directory names for skills
- Keep skill definitions focused and modular

## Testing Instructions

**Skill Validation:**
- Test skills with multiple AI agents that support Agent Skills spec
- Verify skill triggers work correctly for intended tasks
- Check that skill documentation matches implementation
- Ensure skill descriptions are accurate and helpful

**Integration Testing:**
- Test installation via `npx skills` CLI
- Verify git submodule installation method
- Test direct copy installation method
- Validate skill loading and recognition by agents

**Documentation Testing:**
- Verify all markdown files render correctly
- Check that code examples are accurate
- Test that installation instructions work
- Validate links and references

## Code Style Guidelines

**Markdown Standards:**
- Use standard markdown formatting
- Include proper headings hierarchy (# ## ###)
- Use code blocks for commands and code examples
- Maintain consistent formatting across skills

**Skill Structure:**
- Each skill must have `SKILL.md` with skill definition
- Include `README.md` with human-readable documentation
- Use consistent naming conventions for directories
- Keep skill descriptions concise but comprehensive

**File Naming:**
- Use kebab-case for skill directory names
- Use uppercase for `SKILL.md` (skill definition)
- Use standard case for `README.md` (documentation)
- Keep names descriptive and functional

## Build and Deployment

**No Build Process:**
- This is a pure markdown repository
- No compilation or build steps required
- Direct file serving and distribution
- Git-based versioning and distribution

**Distribution Methods:**
1. **CLI Install**: `npx skills add ZenStudioLab/skills`
2. **Git Clone**: Direct repository cloning
3. **Git Submodule**: Submodule integration
4. **Direct Copy**: Manual file copying

**Repository Management:**
- Use git for version control
- Tag releases for stable versions
- Maintain clean commit history
- Use descriptive commit messages

## Project-Specific Context

**Skill Integration:**
- Skills integrate via skills.sh infrastructure
- Agents automatically recognize and load skills
- Skills provide specialized knowledge for specific tasks
- Multiple skills can be active simultaneously

**Target Audience:**
- AI coding agents and their users
- Developers working with AI assistants
- Teams implementing AI-powered workflows
- Contributors to the Agent Skills ecosystem

**Common Patterns:**
- Skills trigger based on task recognition
- Each skill provides domain-specific expertise
- Skills are self-contained and modular
- Documentation serves both humans and agents

## Contributing Guidelines

**For Agents:**
- When adding skills, follow existing patterns
- Test skills thoroughly before submission
- Include comprehensive documentation
- Ensure skills work with multiple agent types

**For Humans:**
- Follow standard git workflow
- Use descriptive pull requests
- Test installation methods
- Update documentation as needed

**Quality Standards:**
- Skills must be functional and well-tested
- Documentation must be clear and accurate
- Code examples must work as documented
- Follow existing project conventions
