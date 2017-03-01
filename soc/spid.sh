#/bin/sh
mkdir -p /var/run/tessel
ln -sf /var/run/tessel1 /var/run/tessel/port_a
ln -sf /var/run/tessel2 /var/run/tessel/port_b
# exec spid /dev/spidev32766.1 2 1 /var/run/tessel
