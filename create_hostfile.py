from jinja2 import Environment, FileSystemLoader
import os

#This parameter is required to be adjusted
#Default Value :
# Spine RID start 1.1.0.1
# Leaf  RID start 1.2.0.1
spine_net      = '1.1.0.0'
leaf_net       = '1.2.0.0'
spine_start_id = 1
leaf_start_id  = 1
spine_hostsuff = 'SPINE-'
leaf_hostsuff  = 'LEAF-' 
spine_as_start = 65001
leaf_as_start  = 65201

#List will be converted to string on j2, then revert to list again in playbook (ansible parsing workaround)
#spine parameter : IP(IP address management of SPINE node), ISL(Fabric Interface, interface facing leaf)
spines = [
   {'ip':'1.1.10.10','isl':['swp1','swp2','swp3']},
]

#leaf parameter : IP(IP address management of LEAF node), MID(MLAG ID, is pair of MLAG switch, each pair has identical ID, add flag m-master or b-backup), IPL(inter peer link, interface facing MLAG pair)
#if it standalone leaf, just dont defien mid parameter 
#Master priority will set to 1000, and backup to 1100
leafs  = [
   {'ip':'1.1.10.11','mid':'1-m','ipl':['swp2'],'isl':['swp1']},
   {'ip':'1.1.10.12','mid':'1-b','ipl':['swp2'],'isl':['swp1']},
   {'ip':'1.1.10.13','isl':['swp1']},
]
#Still on development :
#- Can not use hostname, IP will directly used as command
#-----------------------------------------
#net comp is network address 1.1.1.x
net_used = (spine_net,leaf_net)
spine_net_comp = spine_net.split(".")[:3]
leaf_net_comp = leaf_net.split(".")[:3]

#Handle all parameter error, Iterate the AS Number
for spine in spines:
   #If IP is not in IP format
   #If ISL is empty
   spine.update({'hostname':spine_hostsuff+str(spine_start_id),'as':spine_as_start,'rid':'.'.join([str(s) for s in spine_net_comp])+'.'+str(spine_start_id)})
   spine_as_start += 1
   spine_start_id += 1

for leaf in leafs:
   #If IP is not in IP format
   #If mid have no pair
   #if IPL is empty when mid is not empty vice versa
   #If ISL is empty
   ip_pair=''
   if leaf.get('mid'):
      mid_id = leaf.get('mid').split("-")[0]
      mid_rl = leaf.get('mid').split("-")[1]
      is_pair = 0
      if mid_rl == 'm':
        for leaf_i in leafs:
           if leaf_i.get('mid'):
              mid_i_id =  leaf_i.get('mid').split("-")[0]
              mid_i_rl =  leaf_i.get('mid').split("-")[1]
              if mid_i_id == mid_id and mid_i_rl == 'b':
                 is_pair = 1
                 ip_pair = leaf_i.get('ip')
           
      elif mid_rl == 'b':
        for leaf_i in leafs:
            if leaf_i.get('mid'):
               mid_i_id =  leaf_i.get('mid').split("-")[0]
               mid_i_rl =  leaf_i.get('mid').split("-")[1]
               if mid_i_id == mid_id and mid_i_rl == 'm':
                  is_pair = 1
                  ip_pair = leaf_i.get('ip')
      else: 	 
         print ('IP '+leaf.get('ip')+' Error, MID attribute should be either "m" or "b" ')
         quit()
      if is_pair == 0:
         print ('IP '+leaf.get('ip')+' Error, No MLAG Pair')
         quit()
   
   leaf.update({'hostname':leaf_hostsuff+str(leaf_start_id),'as':leaf_as_start,'rid':'.'.join([str(s) for s in leaf_net_comp])+'.'+str(leaf_start_id),'pair_ip':ip_pair})
   leaf_as_start += 1
   leaf_start_id += 1

#This line uses the current directory
file_loader = FileSystemLoader('.')

# Load the enviroment
env = Environment(loader=file_loader)
template = env.get_template('fabric_host.j2')

#Add the varibles
output = template.render(spinedata=spines,leafdata=leafs,network=net_used)

#Print the output
file_dir= os.getcwd()+"/fabric_host"

file = open (file_dir,'w')
file.write(output)
file.close
print(output)
print('.'.join([str(s) for s in spine_net_comp]))