# Pipelines

Jenkinsfile in Git. Stages: checkout, test, build, scan, push, deploy. `options { timestamps(); timeout() }`. `post { always { junit } }`.

Agents: labels, Kubernetes agent pods. Don’t build on the controller.

Credentials: `withCredentials` / bindings. Masking. Never `echo $PASSWORD`.

Shared library: versioned; pin. Scripted Groovy only when declarative cannot express it.
