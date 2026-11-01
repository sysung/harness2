# Harness² experiments

Experiment with [Google Research Harness²](https://github.com/google-research/harness2) and assess whether subscription-authenticated Codex can replace its API-backed model roles.

The initial container runs the upstream deterministic demo and includes Codex CLI. It does not adapt the Harness² solver, improver, or judge to subscription authentication yet. No paid model run starts automatically.

## Back up skills

Run on the host before experimenting:

```sh
python3 scripts/backup_skills.py
```

The script snapshots complete skill folders from `~/.codex/skills`, the Codex plugin tree, and `~/.agents/skills`. It follows installed skill links, copies their resources, and verifies SHA-256 hashes against the originals. Each run creates a new timestamped directory under `~/.backup_skills` with a private manifest. This is the state at snapshot time, including any earlier edits. It excludes account authentication and unrelated Codex sessions.

Personal skill copies, backups, credentials, and experiment results are ignored by Git and excluded from Docker builds. Never add these with `git add -f`.

## Build and run

```sh
mkdir -p runs personal_skills
docker compose build
docker compose run --rm lab
```

Expected result: the deterministic demo reports completed tasks and zero failed tasks. Results appear in `runs/demo/demo.json`. The upstream revision and Codex version are pinned in `Dockerfile`.

## Test subscription login separately

```sh
docker compose run --rm lab codex login --device-auth
docker compose run --rm lab codex login status
```

Approve the device login in your browser. Authentication persists in the dedicated `codex-auth` Docker volume. Credentials are never baked into the image or copied from your host account. Subscription calls consume your existing Codex allowance.

To test a model call after login:

```sh
docker compose run --rm lab codex exec --skip-git-repo-check 'Reply with exactly: subscription smoke test'
```

This command consumes model usage. It is separate from the free demo.

## Isolate skill experiments

Copy selected skills into the ignored `personal_skills/` directory. This writable container mount is an experiment copy. The host's live Codex skill directories and backup directory are not mounted. Review any resulting changes before applying them to your actual skills.

## Experiment sequence

1. Verify the deterministic demo and isolated skill mounts.
2. Sign in to Codex inside the container and verify one bounded subscription call.
3. Adapt Harness² model-role calls to the authenticated CLI; its upstream endpoint configuration alone does not do this.
4. Run a small representative task baseline and candidate with the same model and acceptance criteria.
5. Compare success, retries, wall time, input tokens, cached input, output tokens, and optimization overhead separately.

Stop a run when its preset call or time budget is reached. Keep raw runs private. Publish only reviewed, redacted summaries. The current image omits benchmark-specific dependencies, the Vertex bridge, and Docker-in-Docker. Full upstream benchmark setup is a later experiment.

No background process is required. Containers exit after their command completes. No GPU is needed for Codex subscription calls.
