import os, json, time, random, asyncio
from instagrapi import Client

if os.path.exists("./cookies.json"):
    cl = Client(json.load(open('./cookies.json')))
else:
    cl = Client()

async def Login():
    try:
        Username = input("Your Instagram Username: ")
        Password = input("\rYour Instagram Password: ")

        print("\rLogging In...")
        cl.login(Username, Password)
        print("\rLogged In", end="      \n")

        json.dump(cl.get_settings(), open('./cookies.json', 'w'))
        print("Saved Cookies")

        return cl.user_id_from_username(Username)
    except Exception as e:
        print(f'An Error Was Found:\n{e}')

async def GetMedia():
    try:
        ids = []

        [ ids.append(m.pk) for m in cl.user_medias_v1(await Login(), 0) ]
        print("Retrieved Media...")

        return ids
    except Exception as e:
        print(f'An Error Was Found:\n{e}')
        return []

async def DeleteMedia():
    deletedMedia = 0
    ids = await GetMedia()

    print("Deleting...")

    for id in ids:
        if(deletedMedia < int(len(ids)) - 5):
            cl.media_delete(id)
            print("\rDeleted ({}/{})".format(deletedMedia, int(len(ids) - 5)), end="           ")
            deletedMedia += 1

asyncio.run(DeleteMedia())