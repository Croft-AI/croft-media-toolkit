"""handles tiktok searches"""
import json
import random
from typing import List, TypedDict
from urllib.parse import quote
import urllib.request
from requests import get, Response, ConnectionError

TIKTOK_REFERER = "https://www.tiktok.com/"


class TikTokDownloadRequest(TypedDict):
    """headers required to download tiktok video"""
    referer: str
    cookie: str
    user_agent: str


with open("./media_secrets/tiktok.json", "r", encoding="utf-8") as json_file:
    TIKTOK_SECRETS: object = json.load(json_file)


def get_offset(count: int) -> int:
    """returns tiktok paginated offset value"""
    if count == 0:
        return 0
    if count == 1:
        return 24
    if count > 1:
        return 12 * (count+1)
    return None


def get_tiktok_search(search_term: str, no_of_pages: int) -> List[object]:
    """returns tiktok search results"""
    all_entries: List[object] = []
    search_term: str = quote(search_term)
    for i in range(no_of_pages):
        offset: str = str(get_offset(i))
        url: str = f"https://www.tiktok.com/api/search/general/full/?aid=1988&app_language=en&browser_language=en-US&history_len=2&is_fullscreen=false&is_page_visible=true&keyword={search_term}&offset={offset}&os=mac&priority_region=&referer=&region=SG&screen_height=1117&screen_width=1728&search_source=normal_search&tz_name=Asia%2FSingapore&web_search_code=%7B%22tiktok%22%3A%7B%22client_params_x%22%3A%7B%22search_engine%22%3A%7B%22mt_search_general_user_live_card%22%3A1%7D%7D%7D%7D&webcast_language=en&msToken=Of4I0bavCWw8OiNiKnSunChUqmSm5r2QvmYzaJkoCEcy77sXFXjUFsnXMx5UUcZR96nNX1nrSHKIlPlebZMvaQfIQliM2rMAsCsbQmK6EnuULz7mo-lURIGx0jRiwnIE31l1UK2Oor9PWeg=&X-Bogus=DFSzxwVO2A2ANJYItJKi/Eok/RQe&_signature=_02B4Z6wo00001OTxm9QAAIDDtIbfL2qjMDjk8Z9AAF2g01"
        response: Response = get(
            url=url, headers=TIKTOK_SECRETS, timeout=10000)
        tiktok_responses = response.json()["data"]
        all_entries += tiktok_responses
    return all_entries


def download_tiktok_video(url: str) -> None:
    """downloads tiktok video from url"""
    try:
        tiktok_video_header: TikTokDownloadRequest = {
            "user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
            "cookie": TIKTOK_SECRETS["cookie"],
            "referer": TIKTOK_REFERER
        }
        random_hash = random.getrandbits(128)
        opener = urllib.request.build_opener()
        headers = [(header_name, header_content)
                   for header_name, header_content in tiktok_video_header.items()]
        print(headers)
        opener.addheaders = headers
        urllib.request.install_opener(opener)
        urllib.request.urlretrieve(url=url, filename=f"{random_hash}.mp4")

    except ConnectionError:
        pass


if __name__ == "__main__":
    # tiktoks = get_tiktok_search("#ukraine", 5)
    # print(len(tiktoks))
    # download_tiktok_video("https://v19-webapp-prime.tiktok.com/video/tos/alisg/tos-alisg-pve-0037c001/o8mIoELrwAb8AVHxIftLpyzANDUNohCymD7wQl/?a=1988&ch=0&cr=0&dr=0&lr=tiktok&cd=0%7C0%7C1%7C0&cv=1&br=3364&bt=1682&cs=0&ds=3&ft=3.u4FZPw0PD12M~Q2t3wUGx15SHEg9N1O-lc&mime_type=video_mp4&qs=0&rc=aDlmZTo1Z2VoODpnOGU1NkBpM2tpbDo6ZnJsbDMzODczNEAxMzQuMWMwNTMxLTQxLzVeYSNoMnNecjRfb2ZgLS1kMS1zcw%3D%3D&btag=e00080000&expire=1689513790&l=20230716072253E91FE0A109CEF9ADA420&ply_type=2&policy=2&signature=5e33c5bb05c54d8b794cce73ef8a66ca&tk=tt_chain_token")
    pass
