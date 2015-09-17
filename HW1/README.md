# Provisioning VMs on Digital Ocean and Azure

## Screencast

[YouTube Link](https://youtu.be/yMcCipG_k1w)
[Download Link](screencast/final_screencast.mp4)

## Basic Setup

Please clone the Repo and run the following commands to get all requirements setup [Debian]

```
virtualenv env
source env/bin/activate
pip install -r requirements.txt
```

config.init.template contains the fields needed to run the scripts. Add the values and remove the .template extension


On Ubuntu/Debian also run the following for SSL:

```
sudo apt-get install python-dev libffi-dev libssl-dev
```

## Digital Ocean

This is straightforward. Upload an ssh key to the Digital Ocean console. Get the ssh key id using the commands in this [gist](https://gist.github.com/rchakra3/7788caff59b64b5adb39). Add this id to your config.ini file.


#### To create a VM

```
python app.py -create
```

#### To delete VMs

```
python app.py -del
```


## Azure

Followed the steps detailed in [this link](https://gist.github.com/rchakra3/b6703a9d5c66e6fc9a7d)

#### Create a VM

```
python azureservices.py
```


## Run the ansible playbook to install and run nginx

```
ansible-playbook -i inventory install_start_nginx.yml
```
