def arelogsallright(text):
    messages=text.split("\n")
    publishwas=False
    publishingended=False
    for message in messages:
        if 'publisher_logger' in message and 'state is' in message:
            publishwas=True
        if 'subscriber_logger' in message and 'received message' in message and not(publishwas):
            return False
        else:
            publiswas=False
        if 'Publishing is ended' in message:
            publishingended=True
        if 'ERROR - No messages!' in message and not(publishingended):
            return False
    return True
f = open("my_app.log", 'r')

text=f.read()

f.close()

if arelogsallright(text):
    print("Logs are all right")
else:
    print("There is some problem in logs")
        
