import requests
import json

timeout = 2  # seconds


class DigitalOceanException(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class DigitalOcean(object):

    current_droplets = {}

    def __init__(self, access_token, ssh_keys, droplet_file=None):

        self.access_token = access_token
        self.headers = {"Authorization": "Bearer " + self.access_token,
                        "Content-Type": "application/json"}
        self.api_url = "https://api.digitalocean.com"

        self.ssh_keys = []
        for key in ssh_keys:
            self.ssh_keys += [key]

        if droplet_file is not None:
            with open(droplet_file, "r") as droplet_file_stream:
                line = droplet_file_stream.readline()
                while line:
                    if line == "\n":
                        line = droplet_file_stream.readline()
                        continue

                    (droplet_id, unique_repr) = line.split("=")
                    self.current_droplets[droplet_id] = unique_repr
                    line = droplet_file_stream.readline()

    def create_droplet(self, droplet_name, image_name="ubuntu-14-04-x64",
                       region="nyc1", size="512mb"):

        unique_repr = region + ":" + droplet_name

        # Uncomment if want to enforce unique names

        # if unique_repr in self.current_droplets.values():
        #     exception_text = "Droplet %s already exists" % unique_repr
        #     raise DigitalOceanException(exception_text)

        payload = {}

        payload["name"] = droplet_name
        payload["region"] = region
        payload["image"] = image_name
        payload["size"] = size
        payload["ssh_keys[]"] = self.ssh_keys
        payload["backups"] = False
        payload["ipv6"] = False
        payload["user_data"] = None
        payload["private_networking"] = None

        droplet_url = self.api_url + "/v2/droplets"

        print "Creating Droplet..."

        res = requests.post(droplet_url, headers=self.headers, params=payload,
                            timeout=timeout)

        try:
            droplet_id = json.loads(res.text)['droplet']['id']
            self.current_droplets[droplet_id] = unique_repr
            return droplet_id

        except Exception as e:
            raise DigitalOceanException(e)

    def get_all_ips(self):

        ip_list = []

        for droplet_id in self.current_droplets:
            droplet_url = self.api_url + "/v2/droplets/" + str(droplet_id)
            res = requests.get(droplet_url, headers=self.headers, timeout=timeout)
            try:
                droplet_dict = json.loads(res.text)["droplet"]
                ip_list += [droplet_dict["networks"]["v4"][0]["ip_address"]]
            except Exception:
                # Droplet doesn't exist. No problemo
                continue

        return ip_list

    def get_droplet_ip(self, droplet_id):

        droplet_url = self.api_url + "/v2/droplets/" + str(droplet_id)

        res = requests.get(droplet_url, headers=self.headers, timeout=timeout)

        try:
            return json.loads(res.text)["droplet"]["networks"]["v4"][0]["ip_address"]
        except Exception as e:
            raise DigitalOceanException(e)

    def delete_droplet(self, droplet_id):

        droplet_url = self.api_url + "/v2/droplets/" + str(droplet_id)

        res = requests.delete(droplet_url, headers=self.headers, timeout=timeout)
        if res.status_code == 204:
            print "Status code is 204"
            self.current_droplets.pop(droplet_id, None)
        else:
            print "Status code is not 204"
            print res.status_code
            exception_text = "Deletion Error"
            raise DigitalOceanException(exception_text)

    def writeout_current(self, filename):
        with open(filename, "w") as f:
            for key in self.current_droplets.keys():
                unique_repr = self.current_droplets[key]
                if not unique_repr.endswith("\n"):
                    unique_repr += "\n"
                f.write(str(key) + "=" + unique_repr)
