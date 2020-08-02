
# cumulusfabric-ibgp
1 spine 2 leaf 1 border demo ibgp fabric

              [spine]


[leaf-1]    [leaf-2]      [border-1]

Requirement
===========
1. Ansible

Quick Start
===========
Download cumulus-vx
-------------------
1. Build the topology accordingly

Clone this directory
-------------------
1. git clone [git_url]

Running the playbook
-------------------
1. Define the switch host and mgmt ip in host
2. Define the fabric parameter in validate_fabric.py
3. Make sure you can reach all switch via OOB/Mgmt/eth0
4. Make sure you can ansible ping all host
  - ansible -i host -m ping all
  - 
5. Play the cumulusfabric-ibgp.yml playbook to initialize the fabric
  - basically the playbook will : clear config, configure hostname,interface,snmp,lldp,ospf,ibgp and evpn
6. Play additional code for additional service


