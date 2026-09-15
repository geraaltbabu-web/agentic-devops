# Q&A

**502 vs 504 vs timeout to nowhere?** 502 bad gateway/upstream; 504 gateway timeout; SYN hang is often SG/route/DNS.

**Why health check fails but curl on the box works?** curl to localhost vs instance IP; SG from LB SG missing; wrong path.

**CNAME flattening?** Apex domains. ALIAS on AWS Route 53.

**Should the app redirect HTTP→HTTPS?** Prefer LB/ingress; avoid double redirect loops.
