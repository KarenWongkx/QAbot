# Building Question Answer Agent – Bani Bot (2)

## Description:

This hosts the question answering agent for model creation using Bani. This bot will load faq store files (.pkl) available on the faq_store volume as well as the trained model from the model volume to create the bot to answer queries. To generate files for loading, do refer to the training script.

## Installation/ Setup:

- Ensure docker is available on your machine. </br>
- Ensure volumes were created and contains relevant files from the training. This volume will be used to create the bot. </br>

## Steps:

- Access to the directory and build the docker image: docker build -t bot . </br>
- Run the image with the created volumes: </br>

```bash
docker run -it --mount source=model_vol_name,target=/model --mount source=faq_vol_name,target=/faq_store -p 8081:8081 -v $(pwd):/bani_training bot
```

## To note:

If training is initiated when bot is running, the updated files generated will be saved on the shared volume. However, the running process will be required to be restarted to access to those files. </br>

## Dependencies/libraries/tools used:

- This is a flask application that handles the route when there is a query.
  To make a query: </br>
  Localhost: port/answer?question=the question </br>
  e.g http://localhost:8081/answer?question= what is baby bonus hotline? </br>
- This uses uWSGI to host this service, the configuration of the server is in the bot.ini file, it will specific which file to run as well as the port. </br>


