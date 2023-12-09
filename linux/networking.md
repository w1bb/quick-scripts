# Networking

The following represent useful Linux commands when it comes to networking. This is a list of examples that can be adapted to your personal needs.

## IP & routing

We will mostly use the `iproute2` package (the `ip` command).

### Add / delete IP address

To configure the IP `192.168.0.1/24` on interface `veth-red`, we can run:

```bash
# Long version
ip address add 192.168.0.1/24 dev veth-red

# Short version
ip a a 192.168.0.1/24 dev veth-red
```

To confirm the changes, we can run:

```bash
# Long version
ip address show dev veth-red

# Short version
ip a sh veth-red
```

To remove this IP address, it is enough to run:

```bash
# Long version
ip address delete 192.168.0.1/24 dev veth-red

# Short version
ip a d 192.168.0.1/24 dev veth-red
```

You could completely flush the interface instead:

```bash
# Long version
ip address flush dev veth-red

# Short version
ip a f veth-red
```

If you wanted to use IPv6 instead of IPv4, you can run `ip -6` instead of `ip` (`ip -4`).

### Datalink config

To check out the current datalink config of a given interface, you can run:

```bash
# Long version
ip link show dev veth-red

# Short version
ip l sh veth-red
```

Let's now set **up** or **down** this interface:

```bash
# Long version
ip link set dev veth-red up

# Short version
ip l s veth-red up
```

### Routing

To enable routing, we need to run: `sysctl -w net.ipv4.ip_forward=1` (or `sysctl -w net.ipv6.ip_forward=1` for IPv6 routing).

To set a default gateway, it is as simple as:

```bash
# Long version
ip route add default via 10.10.10.1

# Short version
ip r a default via 10.10.10.1
```

We can check the current configuration using:

```bash
# Long version
ip route show

# Short version
ip r sh
```

### ARP table

We can check out the ARP table using:

```bash
# Long version
ip neighbor show

# Short version
ip n sh
```

One way to fill this table could be running the `ping` command.

### TCP dump

To inspect a given interface, say `veth-red`, we could run `tcpdump -n -i veth-red`.