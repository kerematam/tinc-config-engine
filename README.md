# Tinc Config Engine
Config Engine creates network configuration for the simple topology depicted on image below which has one master node that has public IP and multiple other tinc client nodes without public IP. This is configuration schematic, on technical background Tinc claims to setup a Mesh VPN Network where nodes directly talk to each other without traffic passing through Master Node [[1](https://www.tinc-vpn.org/)].

![alt text](https://raw.githubusercontent.com/kerematam/tinc-config-engine/master/images/tinc-config-engine-topology.png)

```
.
├── templates/              # tinc config file templates; Jinja2 used as template engine
│   ├── hostfile.tmpl       
│   ├── tinc-down.tmpl
│   ├── tinc-up.tmpl
│   └── tinc.conf.tmpl
├── test/                   # docker-compose files to test tinc setup
│   ├── docker-compose.yml  # test setup with externally mounting config
│   └── tinc.conf.tmpl      # test setup with image with embedded config
├── images/                 # shematics
├── test/                   # test files (alternatively `spec` or `tests`)
├── Dockerfile				      # Dockerfile for config generator script
├── Dockerfile_node	        # Dockerfile to build tinc client image with embedded configuration
├── build_all_nodes.sh		  # Build tinc docker images with embedded configuration
├── config.json				      # configure all networks this json file
├── docker.compose.yml		  # docker-compose file to trigger config generation
├── gen_config.py           # python code to generates configs
├── LICENSE
└── README.md
```
