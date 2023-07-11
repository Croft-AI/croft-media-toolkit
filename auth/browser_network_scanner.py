"""scans browser network details"""
import json
from playwright.sync_api import Page, Request
from auth.browser_login_typings import TwitterDetails

MEDIA_SECRETS_FOLDER: str = "media_secrets"


def scan_networking(page: Page, site_details: TwitterDetails) -> None:
    """scan outgoing network and their details"""
    page.on("requestfinished", lambda request: get_network_content(
        request=request, site_details=site_details))


def get_network_content(request: Request, site_details: TwitterDetails) -> None:
    """gets headers if all headers present"""
    headers = site_details["collect_headers"]
    request_headers = request.all_headers()
    # print(request_headers)
    total_header_count = len(
        [header for header in headers if header in request_headers])
    if total_header_count == len(headers):
        header_object = {}
        for header in headers:
            header_object[header] = request_headers[header]
        write_to_json(site_details["name"],
                      MEDIA_SECRETS_FOLDER, header_object)


def write_to_json(name: str, secret_folder: str, header_object: object) -> None:
    """creates json header file"""
    with open(f'./{secret_folder}/{name}.json', 'w', encoding='utf-8') as json_file:
        json.dump(header_object, json_file)
