import os

import pydash
from googleapiclient import discovery
from httplib2 import Http
from oauth2client import file, client, tools

ALBUM_TITLE = os.getenv("GPHOTOSYNC_ALBUM_TITLE", "Wallpapers")
DEST_FOLDER = os.path.expanduser(
    os.getenv("GPHOTOSYNC_DEST_FOLDER", "~/Pictures/gphotosync")
)

print(f"GPHOTOSYNC_ALBUM_TITLE={ALBUM_TITLE}")
print(f"GPHOTOSYNC_DEST_FOLDER={DEST_FOLDER}")

assert ALBUM_TITLE, 'set GPHOTOSYNC_ALBUM_TITLE'
assert DEST_FOLDER, 'set DEST_FOLDER'

os.makedirs(DEST_FOLDER, exist_ok=True)

gphotosync_folder = os.path.expanduser("~/.gphotosync/")
os.makedirs(gphotosync_folder, exist_ok=True)

store = file.Storage(os.path.join(gphotosync_folder, "store.json"))
credentials = store.get()
if not credentials or credentials.invalid:
    flow = client.flow_from_clientsecrets(
        filename="credentials.json",
        scope="https://www.googleapis.com/auth/photoslibrary.readonly",
    )
    credentials = tools.run_flow(flow=flow, storage=store)
http = Http()
photos = discovery.build("photoslibrary", "v1", http=credentials.authorize(http))
albums = photos.albums().list().execute()["albums"]


def gen_items(album_id):
    next_page_token = None
    while True:
        items = (
            photos.mediaItems()
            .search(
                body={
                    "albumId": album_id,
                    "pageToken": next_page_token,
                }
            )
            .execute()
        )
        for item in items["mediaItems"]:
            yield item
        next_page_token = items.get("nextPageToken")
        if not next_page_token:
            break


wallpapers_album = pydash.find(albums, {"title": ALBUM_TITLE})
assert wallpapers_album
for item in gen_items(album_id=wallpapers_album["id"]):
    print(item)
    dest_file = os.path.join(DEST_FOLDER, item["filename"])
    if os.path.exists(dest_file):
        continue
    dl_url = f"{item['baseUrl']}=d"
    rsp, bytez = http.request(dl_url)
    with open(dest_file, "wb") as fp:
        fp.write(bytez)
