# Policy Test Manifests

Apply these files one by one to verify Gatekeeper policies in the `demo` namespace.

- `deny-latest.yaml`: should be rejected because image tag is `:latest`
- `deny-no-limits.yaml`: should be rejected because `resources.limits` is missing
- `deny-root-user.yaml`: should be rejected because `runAsUser: 0`
- `deny-host-network.yaml`: should be rejected because `hostNetwork: true`
- `allow-valid.yaml`: should be accepted
