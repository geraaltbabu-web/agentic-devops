# 04 — Python for DevOps

Goal: write small, testable automation that talks to APIs, files, and CLIs—without turning into an unmaintainable script on a jump host.

Python is the glue: AWS SDK, Kubernetes clients, Jenkins libraries, log parsers, linters, and “one-off” that become production.

## Sequence

0. [Study plan](00-study-plan.md)
1. [Foundations](01-foundations.md)
2. [HTTP, CLI, and files](02-http-cli-files.md)
3. [Testing, packaging, safety](03-quality.md)
4. [Q&A](04-real-world-q-and-a.md)
5. [Labs](labs/README.md)
6. [Capstone](capstone.md)
7. [In the stack](05-in-the-devops-stack.md)

Use Python 3.12+. Prefer stdlib first; add `boto3`/`httpx`/`pytest` when needed. Never log secrets. Virtualenv per project.
