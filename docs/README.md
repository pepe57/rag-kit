# RAG Facile Documentation

Welcome to the RAG Facile documentation hub! Whether you're setting up your environment, deploying to production, or contributing to the project, you'll find guides and references here.

## Getting Started

### Installation

- **[Windows Setup Guide](guides/windows-setup.md)** — Install on Windows (PowerShell or Git Bash) ⭐ **Start here on Windows**
- **Main README** — [See main installation in README.md](../README.md#1-install-the-cli)

### First Steps

1. **[Install the CLI](../README.md#1-install-the-cli)** — One command to install everything
2. **[Setup Your Workspace](../README.md#2-setup-your-workspace)** — Create your first RAG app
3. **[Running Your App](../README.md#running-your-app)** — Start the development server

## Setup Guides

| Guide | Purpose | Audience |
|-------|---------|----------|
| **[Windows Setup](guides/windows-setup.md)** | Install and troubleshoot on Windows (PowerShell/Git Bash) | Windows users |
| **[Developer Setup (Windows)](guides/developer-setup-windows.md)** | Contribute to RAG Facile on Windows | Contributors on Windows |
| **[Proxy & Network Setup](guides/proxy-setup.md)** | Install behind corporate proxies and VPNs | Enterprise/restricted networks |

## Troubleshooting

| Guide | Problem | Solution |
|-------|---------|----------|
| **[Proxy Troubleshooting](troubleshooting/proxy.md)** | SSL/network errors, corporate proxy issues | Behind a proxy? Start here |

## Advanced Topics

| Guide | Purpose | Audience |
|-------|---------|----------|
| **[CI/CD Testing (Complete)](.github/workflows/test-install.yml)** | Full workflow testing installers on Linux, macOS, Windows | DevOps/maintainers |
| **[CI/CD Linux Testing](guides/ci-cd-linux.md)** | Test installation on Linux/Ubuntu | DevOps/maintainers |
| **[CI/CD macOS Testing](guides/ci-cd-macos.md)** | Test installation on macOS (Intel & Apple Silicon) | DevOps/maintainers |
| **[CI/CD Windows Testing](guides/ci-cd-windows.md)** | Test installation on Windows (PowerShell & Git Bash) | DevOps/maintainers |

## Architecture & Contributing

- **[CONTRIBUTING.md](../CONTRIBUTING.md)** — How to contribute to RAG Facile
- **[AGENTS.md](../AGENTS.md)** — System design and architecture overview

## Reference Documentation

### Tools & Technologies

- **Proto** — https://moonrepo.dev/docs/proto
- **Moon** — https://moonrepo.dev/
- **Uv** — https://docs.astral.sh/uv/
- **Just** — https://just.systems/
- **Ruff** — https://docs.astral.sh/ruff/
- **Chainlit** — https://docs.chainlit.io/
- **Reflex** — https://reflex.dev/docs/

### Sovereign AI & French Government

- **Albert API** — https://albert.sites.beta.gouv.fr/
- **Service-public.fr** — https://www.service-public.fr/

## FAQ

### I'm on Windows. Where do I start?

👉 **[Windows Setup Guide](guides/windows-setup.md)**

We provide native PowerShell installer and Git Bash support.

### I'm behind a corporate proxy and getting SSL errors.

👉 **[Proxy & Network Setup](guides/proxy-setup.md)** and **[Proxy Troubleshooting](troubleshooting/proxy.md)**

Both installers detect and configure proxy support automatically. Manual configuration is also documented.

### I want to contribute to RAG Facile.

👉 **[Developer Setup (Windows)](guides/developer-setup-windows.md)** (for Windows) or **[CONTRIBUTING.md](../CONTRIBUTING.md)** (general)

### How do I test RAG Facile on Windows in GitHub Actions?

👉 **[CI/CD Windows Testing](guides/ci-cd-windows.md)**

Complete examples for testing PowerShell and Git Bash installers in CI/CD.

### Where is the main README?

👉 **[README.md](../README.md)** in the project root

## Quick Links

- **Report an issue:** https://github.com/etalab-ia/rag-facile/issues
- **Source code:** https://github.com/etalab-ia/rag-facile
- **Releases:** https://github.com/etalab-ia/rag-facile/releases

---

**Last updated:** February 6, 2026  
**Latest version:** See [CHANGELOG](../CHANGELOG.md) for changes
