routeros 设置 容器 （需要代理才能拉取镜像）：
/container/add remote-image=metacubex/mihomo:latest interface=veth.clash2 root-dir=/container/clash2 mounts=clash_2 dns=1.1.1.1 hostname=clash2
Entrypoint: sh -c "ip addr add 10.1.1.2/16 dev eth0; ip route add default via 10.1.1.1; /mihomo"

/container/add remote-image=dreamacro/clash-premium:latest interface=veth.clash3 root-dir=/container/clash3 mounts=clash_3 dns=1.1.1.1 hostname=clash3
Entrypoint: sh -c "ip addr add 10.1.1.3/16 dev eth0; ip route add default via 10.1.1.1; /clash"

/container/add remote-image=metacubex/mihomo:latest interface=veth.clash4 root-dir=/container/clash4 mounts=clash_4 dns=1.1.1.1 hostname=clash4
Entrypoint: sh -c "ip addr add 10.1.1.4/16 dev eth0; ip route add default via 10.1.1.1; /mihomo"

/container/add remote-image=metacubex/mihomo:latest interface=veth.clash5 root-dir=/container/clash5 mounts=clash_5 dns=1.1.1.1 hostname=clash5
Entrypoint: sh -c "ip addr add 10.1.1.5/16 dev eth0; ip route add default via 10.1.1.1; /mihomo"