"""handles twitter searches"""
import json
from typing import TypedDict, NotRequired, List
from urllib.parse import quote
from requests import get, Response


# example_url = """https://twitter.com/i/api/graphql/L1VfBERtzc3VkBBT0YAYHA/SearchTimeline?variables={"rawQuery":"bye","count":20,"querySource":"typed_query","product":"Latest"}&features={"rweb_lists_timeline_redesign_enabled":true,"responsive_web_graphql_exclude_directive_enabled":true,"verified_phone_label_enabled":false,"creator_subscriptions_tweet_preview_api_enabled":true,"responsive_web_graphql_timeline_navigation_enabled":true,"responsive_web_graphql_skip_user_profile_image_extensions_enabled":false,"tweetypie_unmention_optimization_enabled":true,"responsive_web_edit_tweet_api_enabled":true,"graphql_is_translatable_rweb_tweet_is_translatable_enabled":true,"view_counts_everywhere_api_enabled":true,"longform_notetweets_consumption_enabled":true,"responsive_web_twitter_article_tweet_consumption_enabled":false,"tweet_awards_web_tipping_enabled":false,"freedom_of_speech_not_reach_fetch_enabled":true,"standardized_nudges_misinfo":true,"tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled":true,"longform_notetweets_rich_text_read_enabled":true,"longform_notetweets_inline_media_enabled":true,"responsive_web_media_download_video_enabled":false,"responsive_web_enhance_cards_enabled":false}&fieldToggles={"withArticleRichContentState":false}"""

TWITTER_FIELD_TOGGLES: str = quote("""{"withArticleRichContentState":false}""")

TWITTER_FEATURES: str = quote("""{"rweb_lists_timeline_redesign_enabled":true,"responsive_web_graphql_exclude_directive_enabled":true,"verified_phone_label_enabled":false,"creator_subscriptions_tweet_preview_api_enabled":true,"responsive_web_graphql_timeline_navigation_enabled":true,"responsive_web_graphql_skip_user_profile_image_extensions_enabled":false,"tweetypie_unmention_optimization_enabled":true,"responsive_web_edit_tweet_api_enabled":true,"graphql_is_translatable_rweb_tweet_is_translatable_enabled":true,"view_counts_everywhere_api_enabled":true,"longform_notetweets_consumption_enabled":true,"responsive_web_twitter_article_tweet_consumption_enabled":false,"tweet_awards_web_tipping_enabled":false,"freedom_of_speech_not_reach_fetch_enabled":true,"standardized_nudges_misinfo":true,"tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled":true,"longform_notetweets_rich_text_read_enabled":true,"longform_notetweets_inline_media_enabled":true,"responsive_web_media_download_video_enabled":false,"responsive_web_enhance_cards_enabled":false}""")

with open("./media_secrets/twitter.json", "r", encoding="utf-8") as json_file:
    TWITTER_SECRETS: object = json.load(json_file)


class TwitterRequestVariables(TypedDict):
    """twitter search input dictionary"""
    rawQuery: str
    count: int
    querySource: str
    product: str
    cursor: NotRequired[str]


def get_twitter_searches(search_term: str, return_count: int, no_of_pages: int) -> List[object]:
    """get search results for twitter"""
    all_entries = []
    cursor = ""
    for i in range(no_of_pages):
        request_variables: TwitterRequestVariables = {"rawQuery": search_term, "count": return_count,
                                                      "querySource": "typed_query", "product": "Latest", "cursor": cursor}
        json_string: str = json.dumps(request_variables)
        variable_encoded: str = quote(string=json_string, encoding="utf-8")
        url: str = f"https://twitter.com/i/api/graphql/L1VfBERtzc3VkBBT0YAYHA/SearchTimeline?variables={variable_encoded}&features={TWITTER_FEATURES}&fieldToggles={TWITTER_FIELD_TOGGLES}"
        response: Response = get(
            url=url, headers=TWITTER_SECRETS, timeout=10000).json()
        response_entries: List[object] = response["data"]["search_by_raw_query"][
            "search_timeline"]["timeline"]["instructions"][0]["entries"]
        if i == 0:
            entries = response_entries
            new_cursor = entries[-1]["content"]["value"]
        else:
            entries = response_entries[:-1]
            new_cursor = response["data"]["search_by_raw_query"]["search_timeline"][
                "timeline"]["instructions"][-1]["entry"]["content"]["value"]
        cursor = new_cursor
        all_entries += entries

    return all_entries


if __name__ == "__main__":
    # url_to_decode = """https://twitter.com/i/api/graphql/L1VfBERtzc3VkBBT0YAYHA/SearchTimeline?variables=%7B%22rawQuery%22%3A%22bye%22%2C%22count%22%3A20%2C%22querySource%22%3A%22typed_query%22%2C%22product%22%3A%22Latest%22%7D&features=%7B%22rweb_lists_timeline_redesign_enabled%22%3Atrue%2C%22responsive_web_graphql_exclude_directive_enabled%22%3Atrue%2C%22verified_phone_label_enabled%22%3Afalse%2C%22creator_subscriptions_tweet_preview_api_enabled%22%3Atrue%2C%22responsive_web_graphql_timeline_navigation_enabled%22%3Atrue%2C%22responsive_web_graphql_skip_user_profile_image_extensions_enabled%22%3Afalse%2C%22tweetypie_unmention_optimization_enabled%22%3Atrue%2C%22responsive_web_edit_tweet_api_enabled%22%3Atrue%2C%22graphql_is_translatable_rweb_tweet_is_translatable_enabled%22%3Atrue%2C%22view_counts_everywhere_api_enabled%22%3Atrue%2C%22longform_notetweets_consumption_enabled%22%3Atrue%2C%22responsive_web_twitter_article_tweet_consumption_enabled%22%3Afalse%2C%22tweet_awards_web_tipping_enabled%22%3Afalse%2C%22freedom_of_speech_not_reach_fetch_enabled%22%3Atrue%2C%22standardized_nudges_misinfo%22%3Atrue%2C%22tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled%22%3Atrue%2C%22longform_notetweets_rich_text_read_enabled%22%3Atrue%2C%22longform_notetweets_inline_media_enabled%22%3Atrue%2C%22responsive_web_media_download_video_enabled%22%3Afalse%2C%22responsive_web_enhance_cards_enabled%22%3Afalse%7D&fieldToggles=%7B%22withArticleRichContentState%22%3Afalse%7D"""
    print(len(get_twitter_searches("bye", 20, 10)))
