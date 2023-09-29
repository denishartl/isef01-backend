import json
import requests
import time


def send_document_to_azure(title, doctype, course):
    body = {
        "document_title": title,
        "document_doctype": doctype,
        "document_course": course
    }
    requests.post(
        url='http://localhost:7071/api/CreateDocument',
        json=body
    )


def main():
    response = requests.get(
        url="https://iu-isef01-functionapp2.azurewebsites.net/api/getcourses")
    all_courses = json.loads(response.content)

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
    i = 0
    for course in all_courses:
        try:
            time.sleep(5)
            print(
                f"Processing course {course['shortname']} ({i}/{len(all_courses)})")
            # Get content summary
            uri = f"https://api.iu.org/content/v2/courses/{course['shortname']}"
            response = requests.get(url=uri, headers=header)
            if response.status_code != 403:
                course_content = json.loads(response.content)

                if course_content['content']['bookCount'] > 0:
                    uri = f"https://api.iu.org/content/v3/books/{course['shortname']}/latest"
                    response = requests.get(url=uri, headers=header)
                    if response.status_code != 403:
                        course_book = json.loads(response.content)
                        send_document_to_azure(
                            course_book['title'], "Skript", course['id'])

                if course_content['content']['videoCount'] > 0:
                    uri = f"https://api.iu.org/content/v1/videos/playlists/{course['shortname']}"
                    response = requests.get(url=uri, headers=header)
                    course_playlists = json.loads(response.content)
                    for playlist in course_playlists['playlists']:
                        uri = f"https://api.iu.org/content/v1/videos/playlist/{playlist['kalturaId']}"
                        response = requests.get(url=uri, headers=header)
                        if response.status_code != 403:
                            playlist_videos = (json.loads(response.content))[
                                'videos']
                            for video in playlist_videos:
                                send_document_to_azure(
                                    video['name'], "Video", course['id'])

                if course_content['content']['audioCount'] > 0:
                    pass
        except Exception as ex:
            print(ex)
        finally:
            i = i+1


if __name__ == "__main__":
    """ This is executed when run from the command line """
    main()
