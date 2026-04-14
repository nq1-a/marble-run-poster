from base64 import b64encode
import urllib.request

# Base64 utilities
def img_to_b64(location: str) -> str:
  with open(str(location), "rb") as image:
      string: bytes = b64encode(image.read())
      return string.decode("utf-8")

def b64_url_encode(b64: str) -> str:
  return b64.replace("-", "%3D").replace("/", "%2F").replace("+", "%2B")

# Headers
headers = {
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
    "DNT": "1",
}

# Main method
def main():
    # Get image
    img_path: str = "res/" + input("Image file name: ")
    img_data: str = f"data:image/png;base64,{b64_url_encode(img_to_b64(img_path))}"

    # Get track data
    with open("tracks/" + input("Track file name: ")) as f:
        track_json: str = f.read()

    # Get other data
    username: str = input("Username: ").upper()
    track_name: str = input("Track name: ").upper()
    length: int = round(float(input("Length (in meters): ")) * 10)
    duration: int = round(float(input("Duration (in seconds): ")) * 1000)

    # Format track data
    track_data: dict[str, str | int] = {
        "track[json]": track_json,
        "track[length]": length,
        "track[duration]": duration,
        "track[imagedata]": img_data,
        "track[username]": username,
        "track[trackname]": track_name,
    }

    # Send request
    req = urllib.request.Request("https://www.marblerun.at/tracks", headers=headers)
    res = urllib.request.urlopen(req)
    print(res.status_code)

if __name__ == "__main__":
    main()
