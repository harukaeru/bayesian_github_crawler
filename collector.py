import os
import requests
from datetime import datetime
from dateutil.parser import parse as parse_date

def import_github_access_token():
    home_dir = os.path.expanduser("~")
    token_path = os.path.join(home_dir, ".github/token.py")

    with open(token_path) as f:
        code = compile(f.read(), token_path, 'exec')
        exec(code, globals(), locals())

    return locals()['GITHUB_ACCESS_TOKEN']

def download_main_storyboard_files(query, access_token, target_date, output_folder, page_number=1):
    url = "https://api.github.com/search/code"
    headers = {"Authorization": f"token {access_token}"}

    while True:
        if page_number == 2:
            break
        params = {
            "q": f"{query} filename:Main.storyboard",
            "per_page": 100,
            "page": page_number
        }
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()

        if not data["items"]:
            break

        for item in data["items"]:
            repo = item["repository"]
            print('repo', repo)
            created_at = parse_date(repo["created_at"])
            if created_at < target_date:
                download_url = item["git_url"].replace("git://", f"https://{access_token}@")
                content_response = requests.get(download_url)
                content_response.raise_for_status()
                content_data = content_response.json()

                file_name = f"{repo['owner']['login']}_{repo['name']}_Main.storyboard"
                file_path = os.path.join(output_folder, file_name)

                with open(file_path, "w") as f:
                    f.write(content_data["content"])

        page_number += 1
        print('page:', page_number)

if __name__ == "__main__":
    query = "language:Swift"
    access_token = import_github_access_token()
    target_date = datetime.strptime("2022-04-04", "%Y-%m-%d")
    output_folder = "./downloaded"
    page_number = 1  # 以前のページ番号をここに入力して再開することができます

    download_main_storyboard_files(query, access_token, target_date, output_folder, page_number)
