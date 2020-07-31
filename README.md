
# cumulusfabric-ibgp
1 spine 2 leaf 1 border demo ibgp fabric

              [spine]

[leaf-1] [leaf-2]  [border-1]

Requirement
===========
1. Ansible
2. Python
  - pip install ansible

Quick Start
===========
1. Define the switch host and reachable mgmt ip in host
2. Define the fabric parameter in validate_fabric.py
3. Play the playbook

Quick Guide
===========
1. Output file will created in cfg/ directory relatively

validate_fabric.py
==================
Start from here, this file will create the neccessary switch configuration file and host file as well

Create the initial configuration file, also validate existing config for multiple or single switch

Specify parameter on fabric_params.cfg

add_service.py
==================
Adding L2 Service to specific switch-port


