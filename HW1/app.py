from digitalocean import DigitalOcean
import time
import sys
import os
from customparser import ConfigReader

config_reader = ConfigReader('config.ini')
config_params = config_reader.get_config_section_map("digitalocean")


access_token = config_params["access_token"]
ssh_keys = [config_params["ssh_key"]]  # config_params["ssh_keys"]
ssh_pub_key_path = config_params["ssh_pub_key_path"]
print ssh_keys
print access_token
print ssh_pub_key_path

ocean_obj = DigitalOcean(access_token, ssh_keys,
                         droplet_file="current_droplets.txt")


def update_inventory():
    with open('inventory', "w") as f:
        for ip_address in ocean_obj.get_all_ips():
            inventory_string = ip_address
            inventory_string += " ansible_ssh_user=root"
            inventory_string += " ansible_ssh_private_key_file="
            inventory_string += ssh_pub_key_path + " \n"
            f.write(inventory_string)

    ocean_obj.writeout_current(filename="current_droplets.txt")

if "-create" in sys.argv:
    droplet_id = ocean_obj.create_droplet("tester")
    tries = 0
    ip_address = None

    # Wait upto 5 seconds to get an ip_address
    while True:
        try:
            tries += 1
            ip_address = ocean_obj.get_droplet_ip(droplet_id)
        except:
            if tries > 5:
                break
            time.sleep(1)
            continue
        else:
            break

    if ip_address is not None:
        print "Droplet Created"
    else:
        sys.exit()

    update_inventory()


if "-update" in sys.argv:
    update_inventory()
    print "Inventory file updated"


if "-del" in sys.argv:
    with open("current_droplets.txt", "r") as f:
        with open("current_droplets_temp.txt", "w") as current_droplets_f:
            line = f.readline()
            while line:
                if line == "\n":
                    line = f.readline()
                    continue
                (droplet_id, unique_id) = line.split("=")
                unique_id = unique_id.split("\n")[0]
                try:
                    ocean_obj.delete_droplet(droplet_id)
                except:
                    print "Could not delete Droplet: %s" % droplet_id
                    print "|%s|" % unique_id
                    droplet_entry = droplet_id + "=" + unique_id
                    print "Droplet entry: |%s|" % droplet_entry
                    current_droplets_f.write(droplet_entry)
                else:
                    print "Droplet Deleted: %s" % droplet_id
                line = f.readline()
    os.remove("current_droplets.txt")
    os.rename("current_droplets_temp.txt", "current_droplets.txt")
    update_inventory()
