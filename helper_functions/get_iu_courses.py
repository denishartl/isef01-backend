from itertools import chain
import json
import requests


def main():
    uri = "https://api.iu.org/content/v1/books/getCompetenceAreas"

    token = ""

    authorization = f"Bearer {token}"

    header = {
        "Accept": "application/json, text/plan, */*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "de",
        "Authorization": authorization,
        "Cache-Control": "no-cache",
        "Dnt": "1",
        "Origin": "https://learn.iu.org",
        "Pragma": "no-cache",
        "Referer": "https://learn.iu.org",
        "Sec-Ch-Ua": '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": "macOS",
        "Sec-Fetch-Dest": None,
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
    }

    response = requests.get(uri, headers=header)

    all_courses_dict = json.loads(response.content)
    all_courses_list = list(all_courses_dict.values())
    all_courses = list(chain.from_iterable(all_courses_list))

    for course in all_courses:
        body = {
            "course_shortname": course['sourceId'],
            "course_name": course['title']
        }
        requests.post(
            url='http://localhost:7071/api/CreateDocument',
            json=body
        )
        body = None


if __name__ == "__main__":
    """ This is executed when run from the command line """
    main()
