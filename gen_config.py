from jinja2 import Environment
from jinja2.loaders import FileSystemLoader

import subprocess 
import os, errno
import uuid
import json

# load template folder 
env = Environment(loader=FileSystemLoader('templates'),line_statement_prefix='%', variable_start_string="${", variable_end_string="}")

# load configs
config_object = json.load(open('config.json'))


# create config folder 
# path : config_outs / config_<unique id>
config_folder = 'config_outs/' + "config_" + str( uuid.uuid4())
os.makedirs(config_folder)

# create hosts folder to be shared on each node
os.makedirs(config_folder + "/shared_hosts");

# iterate nodes
for node in config_object['nodes']:
	print "processing : " + node
	
	# create node folder
	node_path = config_folder + "/" + node 
	try: # check if doublate node names
		os.makedirs( node_path)
	except OSError as e:
		print "dublicate node name! node names should be unique"
		if e.errno != errno.EEXIST:
			raise	
	
	# create network folder for node
	network_path = config_folder + "/" + node + '/' + config_object['network']
	os.makedirs(network_path)
	
	# create priv key
	command_str =  "openssl genpkey -algorithm RSA  -out " +  network_path + "/rsa_key.priv  -pkeyopt rsa_keygen_bits:4096"
	subprocess.call(command_str, shell=True)
	
	# restrict permission to priv key
	command_str = "chmod 600 " +  network_path + "/rsa_key.priv"
	subprocess.call(command_str, shell=True)
	
	# create public key
	path_of_private_key = network_path + "/rsa_key.priv" 
	command_str = "openssl rsa -pubout -in " + path_of_private_key
	pub_key = subprocess.check_output(command_str, shell=True)
	
	# create hostfile
	host = env.get_template('hostfile.tmpl')
	#hostfile = host.render(config_object['nodes'][node],node_name=config_object['nodes'][node],pub_key=pub_key)
	hostfile = host.render(config_object['nodes'][node],pub_key=pub_key)
	
	# write host file into shared_hosts
	# later this folder will be shared into nodes
	hostfile_path = config_folder + "/shared_hosts/" + str(node)
	with open(hostfile_path,'w') as f:
		f.write(hostfile)
	
	# create tinc.conf
	tinc_conf = env.get_template('tinc.conf.tmpl')
	tinc_conf_file = tinc_conf.render(config_object['nodes'][node],node_name=str(node))
	tinc_conf_file_path = network_path + "/tinc.conf"
	with open(tinc_conf_file_path,'w') as f:
		f.write(tinc_conf_file)
	
	# tinc-up
	tincup = env.get_template('tinc-up.tmpl')	
	tincup_file = tincup.render(config_object['nodes'][node])
	tincup_file_path = network_path + "/tinc-up"
	with open(tincup_file_path,'w') as f:
		f.write(tincup_file)							
							
	# tinc-down
	tincdown = env.get_template('tinc-down.tmpl')
	tincdown_file = tincdown.render(config_object['nodes'][node])
	tincdown_file_path = network_path + "/tinc-down"
	with open(tincdown_file_path,'w') as f:
		f.write(tincdown_file)

	# give execute permission to tinc-up and tinc-down
	command_str = "chmod +x " + network_path + "/tinc-*"
	subprocess.call(command_str, shell=True)


# copy share host files	
for node in config_object['nodes']:
	print "copying hosts folder for " + node
	from_shared_hosts_path = config_folder + "/shared_hosts"
	network_path = config_folder + "/" + node + '/' + config_object['network']
	to_node_hosts_path = network_path + "/hosts"
	command_str = "cp -r " + from_shared_hosts_path + " " + to_node_hosts_path
	subprocess.call(command_str, shell=True)

		
print "Config files rest in " + config_folder