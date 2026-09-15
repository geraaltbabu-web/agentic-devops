# Releases, GitOps, and CI identity

## Tags and releases

- **Lightweight tag:** name on a commit
- **Annotated tag:** object with message and tagger (prefer this for releases)

```bash
git tag -a v1.2.0 -m "Release 1.2.0"
git push origin v1.2.0
```

GitHub/GitLab Releases wrap a tag plus notes and artifacts. Artifacts that matter for prod are **immutable image digests**, not zip files on a laptop.

Versioning: SemVer when you publish libraries; for apps, Git SHA plus a calendar version is common. Pick one per repo.

## Change catalogs

Keep `CHANGELOG.md` or generate from conventional commits. Incident reviews ask “what shipped?” You need Git SHA + image digest + ticket (module 01 audit triangle).

## GitOps (preview of module 16)

Desired state lives in Git. Argo CD / Flux reconcile the cluster. Rules:

- `main` on the GitOps repo is production-adjacent
- Separate app repo vs env repo **or** folders with CODEOWNERS
- No `kubectl apply` from a laptop as the source of truth
- PR to change replicas, images, and Helm values

If Jenkins also applies the same manifests, you will drift.

## CI as a Git client

The pipeline checks out a **specific SHA**, not `latest` of a branch, for release jobs. `actions/checkout` with `ref: ${{ github.sha }}`.

For deploy jobs:

- OIDC to AWS (module 01)
- Least-privilege Git token to push tags or GitOps commits
- Do not let CI push to `main` without protection

## Signed commits and provenance

SSH or GPG signed commits + verified badge. SLSA provenance is the next layer (module 21). Signing does not replace review.

## Checkpoint

Why is `git checkout main && docker build` in a deploy job weaker than building from the PR SHA?
