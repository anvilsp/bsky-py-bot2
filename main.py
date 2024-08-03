# This script includes the functions that reply to posts will either perform that routine or create a random post, based on the arguments.
    # random = random post
    # reply = checks and sends replies
# Program by Ava Vazquez

import sys, os
from bsky_core import get_notifications, create_image_reply, create_image_post
from animal_image import check_if_animal, get_random_animal, get_image, get_animal_url

# reply to 'mention' notifications
def do_replies():
    replies, mentions = get_notifications(mark_read = True)
    for mention in mentions:
        # get the contents of the message, removing the handle
        reply_text = mention.record.text.replace(f"@{os.environ.get('BSKY_IDENTIFIER')} ", '').strip()

        mention_uri = mention['uri']
        mention_cid = mention['cid']

        # get the animal, whether it's from text or not
        if check_if_animal(reply_text):
            animal = reply_text
            new_reply = f"Here's your {animal}!"
        else:
            animal = get_random_animal()
            new_reply = f"cool. here's a {animal}"

        # get image data
        img_data = get_image(get_animal_url(animal))
        
        # create the reply
        post = create_image_reply(
            image = img_data,
            uri = mention_uri,
            cid = mention_cid,
            text = new_reply,
            alt_text = f"Random {animal} image."
        )
        print(post)
    
    # reply to 'reply' notifications
    for reply in replies:
        # get the contents of the message
        reply_text = reply.record.text.strip()

        # get the uri and cid of the reply
        reply_uri = reply['uri']
        reply_cid = reply['cid']

        # get the uri and cid of the thread root
        root_uri = reply['record']['reply']['root']['uri']
        root_cid = reply['record']['reply']['root']['cid']

        # get the animal, whether it's from text or not
        if check_if_animal(reply_text):
            animal = reply_text
            new_reply = f"Here's your {animal}!"
        else:
            animal = get_random_animal()
            new_reply = f"cool. here's a {animal}"

        # get image data
        img_data = get_image(get_animal_url(animal))
        
        # create the reply
        post = create_image_reply(
            image = img_data,
            uri = reply_uri,
            cid = reply_cid,
            root_uri = root_uri,
            root_cid = root_cid,
            text = new_reply,
            alt_text = f"Random {animal} image."
        )
        print(post)

if len(sys.argv) > 1:
    if sys.argv[1] == "reply":
        do_replies()
        exit()
    elif sys.argv[1] == "random":
        animal = get_random_animal()
        img_data = get_image(get_animal_url(animal))
        post = create_image_post(
            image = img_data,
            alt_text = f"Random {animal} image."
        )
        print(post)
else:
    print("Usage: [reply] replies to unread mentions and replies, [random] posts a random image.")