# Q&A

**Why not Bash for this parser?** JSON, errors, tests, Windows+Linux.

**subprocess shell=True?** Injection and quoting hell. List args.

**Where do AWS keys go?** Nowhere in code. SSO/OIDC/role. boto3 default chain.

**How do you test a CLI?** `main(argv=["plan","--json"])` returning int; assert stdout JSON.

**Exception with a URL query token?** Log exception type + sanitized message.

**Editable install vs copying files to /opt?** Packaging wins for rollback and versions.
