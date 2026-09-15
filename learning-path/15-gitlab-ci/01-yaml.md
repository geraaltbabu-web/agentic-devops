# Pipeline YAML

Stages, jobs, `script`, `image`, `tags` for runners. Artifacts expire. Cache keyed by lockfile.

`rules: if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH`. MR pipelines vs branch.

Include official templates; pin versions.
