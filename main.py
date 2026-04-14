from base64 import b64encode
from pathlib import Path
from re import sub
from requests import post

# Base64 utilities
def img_to_b64(location: str) -> str:
  with open(str(location), "rb") as image:
      string: bytes = b64encode(image.read())
      return string.decode("utf-8")

def b64_url_encode(b64: str) -> str:
  return b64.replace("-", "%3D").replace("/", "%2F").replace("+", "%2B")

# Headers
headers: dict[str, str] = {
    "POST": "/tracks HTTP/1.1",
    "Host": "www.marblerun.at",
    "Accept": "application/json",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "Referer": "https://www.marblerun.at/tracks/new",
    "Origin": "https://www.marblerun.at",
    "Connection": "keep-alive",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "X-Requested-With": "XMLHttpRequest",
    "Content-type": "application/x-www-form-urlencoded; charset=UTF-8",
}

# Main method
def main():
    # Create directories if they do not exist
    try:
        Path("res/").mkdir()
        Path("tracks/").mkdir()
    except FileExistsError:
        pass
    else:
        print("Directories created. Put data in these folders and rerun this file.")
        return

    # Get image
    img_path: str = "res/" + input("Image file name: ")
    img_data: str = "data:image/png;base64," + b64_url_encode(img_to_b64(img_path))

    # Get track data
    with open("tracks/" + input("Track file name: ")) as f:
        track_json: str = sub(r"\s", "", f.read())

    # Get other data
    username: str = input("Username: ").upper()
    track_name: str = input("Track name: ").upper()

    # Format track data
    track_data: dict[str, str | int] = {
        "track[json]": track_json,
        "track[length]": 9999,
        "track[duration]": 69420000,
        "track[imagedata]": img_data,
        "track[username]": username,
        "track[trackname]": track_name,
    }

    # Send request
    with post("https://www.marblerun.at/tracks", data=track_data, headers=headers) as res:
        print(res.reason)

if __name__ == "__main__":
    main()
