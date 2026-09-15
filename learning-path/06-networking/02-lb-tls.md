# Load balancing and TLS

**L4 (NLB/TCP):** bytes, source IP preservation options, no HTTP routes.

**L7 (ALB/nginx/Ingress):** host/path, headers, HTTP/2, gRPC, WAF.

Health: protocol, path, code, timeout, interval, unhealthy threshold. App must bind the address the LB uses.

TLS: SNI, cert SAN vs hostname, chain, expiry, clock skew, ciphers. Terminate at LB or pass-through. mTLS for service-to-service in mesh.

Enterprise: ACM (AWS) or cert-manager (K8s/OCP). Rotate before expiry alerts fire.
