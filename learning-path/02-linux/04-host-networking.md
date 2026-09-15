# Host networking, DNS, TLS

## Interfaces and addresses

```text
ip -br addr
ip route
ip neigh
```

`ifconfig`/`route` are legacy. Learn `ip`.

Default route missing = “everything except local is unreachable.” Wrong route = packets leave the wrong NIC (cloud: wrong subnet/IGW).

## Ports and sockets

```text
ss -lntup
ss -tnp | grep PID
```

`LISTEN` vs `ESTABLISHED`. Binding `127.0.0.1` vs `0.0.0.0` is why load balancer health checks fail (app only on localhost).

## DNS

Resolution path on systemd systems is often:

```text
app -> libc -> systemd-resolved -> /etc/resolv.conf stub -> upstream
```

```text
getent hosts example.com
resolvectl query example.com
dig +short example.com
```

`/etc/hosts` overrides. Split DNS in enterprises (internal zone vs public) causes “works on my laptop.”

NXDOMAIN vs timeout vs SERVFAIL are different bugs. Timeouts look like a hung app.

## HTTP from the host

```text
curl -vI https://example.com
curl --max-time 5 http://127.0.0.1:8080/health
openssl s_client -connect example.com:443 -servername example.com </dev/null
```

`-v` shows DNS, TCP, TLS, HTTP. That is half of ALB 502 diagnosis from the instance.

## Firewalls

- **nftables** / **iptables**
- **firewalld** (RHEL)
- **ufw** (Ubuntu convenience)
- Cloud **security groups** still apply *in addition*

Opening a port in `ufw` does nothing if the AWS SG blocks it. Always name both layers.

## Time and TLS

Wrong clock breaks TLS and Kerberos. `timedatectl`. NTP/chrony.

TLS: SNI, expired cert, wrong SAN, missing intermediate. `openssl s_client` shows the chain.

## Checkpoint

A curl from the VM to `https://api.internal` hangs. List the checks in order: DNS, route, SG/NACL, host firewall, listening socket, TLS, HTTP.
