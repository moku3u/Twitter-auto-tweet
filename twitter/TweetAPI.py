import requests
import json
from bs4 import BeautifulSoup
from PIL import Image
from datetime import datetime

from .ErrorClasses import *

class Tweet():
    def __init__(self, auth_token, text, media=None):
        self.cookies = {
            "auth_token": auth_token,
            "ct0": requests.get("https://twitter.com/i/release_notes").cookies.get("ct0")
        }

        self.headers = {
            "accept": "*/*",
            "accept-language": "ja,en-US;q=0.9,en;q=0.8",
            "authorization": "Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA",
            "origin": "https://twitter.com",
            "referer": "https://twitter.com/compose/tweet",
            "sec-ch-ua": "'Chromium';v='106', 'Google Chrome';v='106', 'Not;A=Brand';v='99'",
            "sec-ch-ua-mobile": "?1",
            "sec-ch-ua-platform": "'Android'",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            'x-csrf-token': self.cookies["ct0"],
            'x-twitter-active-user': 'yes',
            'x-twitter-auth-type': 'OAuth2Session',
            'x-twitter-client-language': 'ja',
        }

        self.text = text
        self.media = media

    def upload_image(self):
        GetMediaId = requests.post("https://upload.twitter.com/i/media/upload.json",
                    headers=self.headers,
                    params={
                        "command": "INIT",
                        "total_bytes": len(self.media),
                        "media_type": "image/png",
                        "media_category": "tweet_image",
                        },
                    cookies=self.cookies
                    )
        util.HttpStatusCheck(GetMediaId)
        MediaId = GetMediaId.json()["media_id"]

        AppendImage = requests.post("https://upload.twitter.com/i/media/upload.json",
                            headers=self.headers,
                            params={
                                "command": "APPEND",
                                "media_id": MediaId,
                                "segment_index": "0"
                                },
                            cookies=self.cookies,
                            files={"media": self.media}
                            )
        util.HttpStatusCheck(AppendImage)

        Finalize = requests.post("https://upload.twitter.com/i/media/upload.json",
                            headers=self.headers,
                            params={
                                "command": "FINALIZE",
                                "media_id": MediaId
                                },
                            cookies=self.cookies,
                            )
        util.HttpStatusCheck(Finalize)
        self.media = MediaId

    def post(self):
        endpointquery = util.GetEndpointQuery()["CreateTweet"]["query"]
        data = {
            "variables": {
                "tweet_text": self.text+"\n"+datetime.now().strftime('%m/%d-%H:%M'),
                "media": {
                    "media_entities": [],
                    "possibly_sensitive": False,
                },
                "withDownvotePerspective": False,
                "withReactionsMetadata": False,
                "withReactionsPerspective": False,
                "withSuperFollowsTweetFields": True,
                "withSuperFollowsUserFields": True,
                "semantic_annotation_ids": [],
                "dark_request": False,
            },
            "features": {
                'tweetypie_unmention_optimization_enabled': True,
                'responsive_web_uc_gql_enabled': True,
                'vibe_api_enabled': True,
                'responsive_web_edit_tweet_api_enabled': True,
                'graphql_is_translatable_rweb_tweet_is_translatable_enabled': False,
                'interactive_text_enabled': True,
                'responsive_web_text_conversations_enabled': False,
                'verified_phone_label_enabled': False,
                'standardized_nudges_misinfo': True,
                'tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled': False,
                'responsive_web_graphql_timeline_navigation_enabled': False,
                'responsive_web_enhance_cards_enabled': True,
            },
            "queryId": endpointquery,
        }

        if self.media:
            data["variables"]["media"]["media_entities"] = [{"media_id": self.media,"tagged_users": []}]
        CreateTweet = requests.post(f"https://twitter.com/i/api/graphql/{endpointquery}/CreateTweet", cookies=self.cookies, headers=self.headers, json=data)
        util.HttpStatusCheck(CreateTweet)
        Tweet_Created_at = CreateTweet.json()['data']['create_tweet']['tweet_results']['result']['legacy']['created_at']
        Tweet_ID = CreateTweet.json()['data']['create_tweet']['tweet_results']['result']['legacy']['conversation_id_str']
        print(f"Tweet success\nData:\n \tcreated-at: {Tweet_Created_at}\n\ttweet-id: {Tweet_ID}\n\tcontent: {self.text}")

    def delete(self, tweet_id):
        endpointquery = util.GetEndpointQuery()["DeleteTweet"]["query"]
        data = {
            "variables": {
                "tweet_id": tweet_id,
                "dark_request": False,
            },
            "queryId": endpointquery,
        }

        requests.post(f"https://twitter.com/i/api/graphql/{endpointquery}/DeleteTweet", cookies=self.cookies, headers=self.headers, json=data)

class util():
    @staticmethod
    def check_auth_token(token:str):
        endpointquery = util.GetEndpointQuery()["CreateTweet"]["query"]
        data = {
            "variables": {
                "tweet_text": "test",
                "media": {
                    "media_entities": [],
                    "possibly_sensitive": False,
                },
                "withDownvotePerspective": False,
                "withReactionsMetadata": False,
                "withReactionsPerspective": False,
                "withSuperFollowsTweetFields": True,
                "withSuperFollowsUserFields": True,
                "semantic_annotation_ids": [],
                "dark_request": False,
            },
            "features": {
                "tweetypie_unmention_optimization_enabled": True,
                "responsive_web_uc_gql_enabled": True,
                "vibe_api_enabled": True,
                "responsive_web_edit_tweet_api_enabled": True,
                "graphql_is_translatable_rweb_tweet_is_translatable_enabled": False,
                "interactive_text_enabled": True,
                "responsive_web_text_conversations_enabled": False,
                "verified_phone_label_enabled": False,
                "standardized_nudges_misinfo": True,
                "tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled": False,
                "responsive_web_graphql_timeline_navigation_enabled": False,
                "responsive_web_enhance_cards_enabled": True,
            },
            "queryId": endpointquery,
        }

        cookie = {
            "auth_token": token,
            "ct0": requests.get("https://twitter.com/i/release_notes").cookies.get("ct0")
        }

        headers = {
                "authorization": "Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA",
                "x-csrf-token": cookie["ct0"],
                "x-twitter-active-user": "yes",
                "x-twitter-auth-type": "OAuth2Session",
                "x-twitter-client-language": "ja",
        }

        check = requests.post(f"https://twitter.com/i/api/graphql/{endpointquery}/CreateTweet", cookies=cookie, headers=headers, json=data)

        if check.status_code == 401:
            print("Bad token")
            return False
        elif check.status_code == 200:
            endpointquery = util.GetEndpointQuery()["DeleteTweet"]["query"]
            data = {
                "variables": {
                    "tweet_id": check.json()['data']['create_tweet']['tweet_results']['result']['legacy']['conversation_id_str'],
                    "dark_request": False,
                },
                "queryId": endpointquery,
            }

            requests.post(f"https://twitter.com/i/api/graphql/{endpointquery}/DeleteTweet", cookies=cookie, headers=headers, json=data)
            return True
        else:
            util.HttpStatusCheck(check)
            return False

    @staticmethod
    def GetEndpointQuery():
        access = requests.get("https://twitter.com/compose/tweet")
        util.HttpStatusCheck(access)
        html = BeautifulSoup(access.text, "lxml-html")
        for i in html.find_all("script"):
            if 'src="https://abs.twimg.com/responsive-web/client-web-legacy/main.' in str(i):
                main_js = i.get("src")
        if "main_js" not in locals():
            TwitterJavascriptNotFound("main.js NotFound: Couldn't find main.js from HTML")

        main_js_filename = main_js.split(".")[1]
        read_js = requests.get(main_js)
        util.HttpStatusCheck(read_js)
        QueryDict = {}
        for t in read_js.text.split("{"):
            if 'operationType:"' in t:
                t = t.replace(",metadata:", "").replace("queryId", '"queryId"').replace("operationName", '"operationName"').replace("operationType", '"operationType"')
                t = json.loads("{"+t+"}")
                QueryDict[t["operationName"]] = {"query": t["queryId"], "FullURL": f"https://twitter.com/i/api/graphql/{t['queryId']}/{t['operationName']}"}
        return QueryDict

    @staticmethod
    def HttpStatusCheck(response:requests.Response):
        if response.status_code == 200:
            return False
        elif response.status_code == 400:
            raise TwitterBadRequest(f"Bad request\nLog:\nStatusCode:400\nResponseText:{response.text}")
        elif response.status_code == 403:
            raise TwitterAccessDenied(f"Access denied\nLog:\nStatusCode:403\nResponseText:{response.text}")
        elif response.status_code == 429:
            raise TwitterRateLimit(f"Rate limit\nLog:\nStatusCode:429\nResponseText:{response.text}")
        elif response.status_code > 500:
            raise TwitterInternalServerError(f"Internal Server Error\nLog:\nStatusCode:429\nResponseText:{response.text}")

    @staticmethod
    def limit_input(input_message:str, accept, errortext="Invalid input"):
        if type(accept) == list:
            while True:
                input_value = input(input_message+": ")
                if input_value not in accept:
                    print(errortext)
                elif input_value in accept:
                    break
        elif accept == int:
            while True:
                input_value = input(input_message+": ")
                if input_value.isdigit():
                    break
                else:
                    print(errortext)
        elif accept == str:
            while True:
                input_value = input(input_message+": ")
                if input_value.isalpha():
                    break
                else:
                    print(errortext)
        return input_value

    @staticmethod
    def indention_replace(text):
        return text.replace("\\n", "\n")
