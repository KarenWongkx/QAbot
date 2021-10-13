# Building Question Answer Agent – Bani Bot (2)

## Description:

This hosts the question answering agent for model creation using Bani. This bot will load faq store files (.pkl) available on the faq_store volume as well as the trained model from the model volume to create the bot to answer queries. To generate files for loading, do refer to the training script.

## Installation/ Setup:

- Ensure docker is available on your machine. </br>
- Ensure volumes were created and contains relevant files from the training. This volume will be used to create the bot. </br>

## Steps to run on local desktop:

- Access to the directory and build the docker image: docker build -t bot . </br>
- Run the image with the created volumes: </br>

```bash
docker run -it --mount source=model_vol_name,target=/model --mount source=faq_vol_name,target=/faq_store -p 8081:8081 -v $(pwd):/bani_training bot
```

$(pwd) - assume there is a local version of this on the machine, if there isn't, look at steps to run on VM.

## Steps to run on VM:

This section document the steps to run on VM, files are taken from docker hub.

- SSH into VM with login credential
- This repo can be pulled from docker hub

```bash
docker pull karenwkx/bot:changeport
```

- Ensure port is open, port used will be 8057 in this example.

```bash
docker run -it --mount source=model_vol,target=/model --mount source=faq_vol,target=/faq_store -p 8057:8057 karenwkx/bot:changeport
```

### Steps to transfer content of volume from local machine to VM

If training is done on another machine and pkl and model files are saved in the volume on the host machine, content in the volume can be transferred over to the VM via the steps below.

Refer to this: https://github.com/fjh1997/docker_named_volume_backup

Local Machine:

1. Copy contents of the backup script to a new folder on local machine (with .sh extension)
2. Follow instruction as provided in the repo readme, need to do in same folder as the script that is saved.
3. Copy file over by:

- create a folder in VM:

```bash
mkdir ~/vol_transfer
```

- Copy content of the volume to VM:

Ensure that this command is ran on the directory of where the .tar is generated on the local machine.

```bash
#scp <.tar file> <ssh address>:<folder where the vol folder is created on VM>
scp ./faqvol.tar karen@ssh address:/local/docker-image/vol_transfer/
```

On VM: 4) Restore volume via script from the repo:
Ensure there is a copy of the restore script on the VM.

```bash
cd /local/docker-image/vol_transfer/
# bash restore_script targeted_vol transferred_volume_file
bash ./restore_docker_volume.sh faq_vol ./faqvol.tar
bash ./restore_docker_volume.sh model_vol ./modelfaq.tar
```

## To note:

If training is initiated when bot is running, the updated files generated will be saved on the shared volume. However, the running process will be required to be restarted to access to those files. </br>

## Dependencies/libraries/tools used:

- This is a flask application that handles the route when there is a query.
  To make a query: </br>
  Localhost: port/answer?question=the question </br>
  e.g http://localhost:8081/answer?question= what is baby bonus hotline? </br>
- This uses uWSGI to host this service, the configuration of the server is in the bot.ini file, it will specific which file to run as well as the port. </br>
