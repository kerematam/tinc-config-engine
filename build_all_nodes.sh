#!/bin/bash

# example :
# to test the commands
# ./build_all_nodes.sh config_outs/config_5a2b0956-2201-4128-aba8-49c1fc43ddc3 your-name-here test

# to build all images
# ./build_all_nodes.sh config_outs/config_5a2b0956-2201-4128-aba8-49c1fc43ddc3 your-name-here build

# export images to image_outs folder
# ./build_all_nodes.sh config_outs/config_5a2b0956-2201-4128-aba8-49c1fc43ddc3 your-name-here save 

config_path=$1
node_author=$2
run_mode=$3 # set "test" or "build"

image_name="$(echo $config_name'_'$node_name)"
network_name="$(ls $1/* | sed -n 2p)"

# removes back slash at the end of string if exist
path=${1%/}

for d in $path/* ; do
	node_name="$(echo "$d" | cut -d/ -f 3)"

	if [ $node_name != "shared_hosts" ]
	then
		config_name="$(echo $config_path |cut -d/ -f 2)"
		image_name="$(echo $config_name'_'$node_name)"
		
		if [ $run_mode == "test" ]
		then
			echo "sudo docker build -f Dockerfile_node -t $node_author/$image_name --build-arg node_path=$config_path/$node_name/$network_name ."
		fi

		if [ $run_mode == "build" ]
		then
			sudo docker build -f Dockerfile_node -t $node_author/$image_name --build-arg node_path=$config_path/$node_name/$network_name/ .
		fi

		if [ $run_mode == "save" ]
		then
			sudo docker save -o image_outs/$image_name.img $node_author/$image_name
		fi

	fi
done
