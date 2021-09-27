# Bani Bot

Description:
This host the question answering agent for model created using Bani. Bot.py will load FAQ classes present in the volume of /faq_store and create a masterbot with the loaded FAQ class and trained model. This files are retrieved from the volume: /faq_store and /model.

Execution:

1. Volumes should be created previously and should have content from the bot training.
2. Build image: docker build -t bot .
3. Run image: docker run -it --mount source=bani_model,target=/model --mount source=bani_faq,target=/faq_store -p 8081:8081 -v $(pwd):/bani_training bot
