# Tinc Config Engine
Config Engine generates network configurations for all nodes of VPN Mesh network from a single **config.json** file. This is time saving approach when you need to deploy Tinc for numerous remote nodes. So you can share config folders directly or you can create docker images for each configs (using provided scripts) to disribute and directly connect to VPN network.

For now; it only supports simple topology depicted on schematic below which has one node with a public IP (namely master node) and multiple other Tinc client nodes without public IP. Tinc claims to setup a Mesh VPN Network where nodes directly talk to each other without traffic passing through Master Node "regardless of how you set up the tinc daemons to connect to each other" [[1](https://www.tinc-vpn.org/)].

![alt text](https://raw.githubusercontent.com/kerematam/tinc-config-engine/master/images/tinc-config-engine-topology.png)


### Directory Structure

```
├── templates/              # tinc config file templates; Jinja2 used as template engine
│   ├── hostfile.tmpl       
│   ├── tinc-down.tmpl
│   ├── tinc-up.tmpl
│   └── tinc.conf.tmpl
├── test/                   # docker-compose files to test tinc setup
│   ├── docker-compose.yml  # test setup with externally mounting config
│   └── tinc.conf.tmpl      # test setup with image with embedded config
├── images/                 # shematics
├── test/                   # test files
├── Dockerfile              # Dockerfile for config generator script
├── Dockerfile_node         # Dockerfile to build tinc client image with embedded configuration
├── build_all_nodes.sh      # Build tinc docker images with embedded configuration
├── config.json             # configure all networks this json file
├── docker.compose.yml      # docker-compose file to trigger config generation
├── gen_config.py           # python code to generates configs
├── LICENSE
└── README.md
```
