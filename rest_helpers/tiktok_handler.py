"""handles tiktok searches"""
import json
from typing import List
from urllib.parse import quote
from requests import get, Response


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


if __name__ == "__main__":
    tiktoks = get_tiktok_search("#ukraine", 5)
    print(len(tiktoks))
