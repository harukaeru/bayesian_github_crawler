import sys
import os
import requests
import storyboard_search

def import_github_access_token():
    home_dir = os.path.expanduser("~")
    token_path = os.path.join(home_dir, ".github/token.py")

    with open(token_path) as f:
        code = compile(f.read(), token_path, 'exec')
        exec(code, globals(), locals())

    return locals()['GITHUB_ACCESS_TOKEN']

def convert_github_url_to_api(url):
    api_url = url.replace("https://github.com", "https://api.github.com/repos")
    return api_url + "/contents"

def download_and_save(file, access_token):
    headers = {"Authorization": f"token {access_token}"}
    response = requests.get(file["download_url"], headers=headers)

    if response.status_code == 200:
        with open(file["name"], "wb") as f:
            f.write(response.content)
        print(file['name'] + '\n  was downloaded from ' + file['url'])
    else:
        print("Error while downloading file. Status code: ", response.status_code)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 generate.py <github_repo_url>")
    else:
        github_url = sys.argv[1]

        github_access_token = import_github_access_token()

        api_url = convert_github_url_to_api(github_url)

        # Call the function from the imported storyboard_search module
        print('---------Start Search---------')
        storyboard_files = storyboard_search.find_storyboard_files(api_url, github_access_token)
        print('---------End of Search---------')

        if not storyboard_files:
            print("No storyboard files found.")
        else:
            for storyboard_file in storyboard_files:
                download_and_save(storyboard_file, github_access_token)
