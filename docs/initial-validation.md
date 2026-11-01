# Initial validation

Validated on November 1, 2026, using Docker Desktop on Apple Silicon.

| Check | Result |
| --- | --- |
| Docker image build | Passed on linux/arm64 |
| Pinned Codex CLI | `codex-cli 0.166.0` |
| Harness² credential-free demo | Two tasks completed, zero failed |
| Skill backup | 1,085 files verified, including 144 SKILL.md files |
| Backup behavior with temporary fixtures | Copied resources and linked downloaded skills; source edits did not alter backup |
| Container skill write | Wrote only to the ignored personal skill copy |
| Host skill path inside container | Absent |
| Isolated Codex authentication | Not logged in, as expected |
| Git exclusion | Personal skill copies, backups, run output, and credential paths ignored |

The backup preserves the skills as they existed before these container experiments. It includes the earlier Poteto and reflect changes from the setup chat. It does not claim to recover every historical version of a skill.

No model-backed benchmark or subscription smoke test has run. The demo uses deterministic local editors and cannot establish model quality, token savings, or subscription compatibility for the full optimizer.

## Subscription integration gap

The pinned upstream revision requires a Responses API URL and key in `harness2/substrate/codex.py`. Benchmark-specific setup also creates a separate Codex home. The improver and judge have their own model routes. Signing into the container's standalone Codex CLI does not replace these routes.

The next experiment is to complete device login and run one bounded CLI call. Then inspect how to route each required Harness² model role through the CLI, preserving structured results, timeouts, failure handling, and usage accounting. Do not forward a ChatGPT session token to an arbitrary API endpoint as an API key.

Sources: [upstream setup](https://github.com/google-research/harness2/blob/1cfe254e8d25b15f37048c3730134686abe60335/docs/SETUP.md), [Codex authentication](https://learn.chatgpt.com/docs/auth).
