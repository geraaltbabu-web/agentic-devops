# Foundations

Packets: IP → TCP/UDP → TLS → HTTP. Timeouts at each layer look the same to users (“hang”).

**DNS:** A/AAAA, CNAME, MX, TXT, NS, PTR. TTL. NXDOMAIN vs SERVFAIL vs timeout. Split horizon. Search domains. `dig`, `resolvectl`, `getent hosts`.

**Routing:** default gateway, more-specific prefixes, blackhole. Cloud: route table, IGW, NAT, TGW, VPC endpoints.

**Firewall:** stateful SG vs stateless NACL vs iptables/nft vs kube-proxy vs WAF. Always name which layer you opened.

**MTU/VPN:** less common, painful. Don’t start here.
