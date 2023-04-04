import json
import os
import requests
import pickle

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline

def train_classifier(training_data, labels):
    classifier = Pipeline([
        ('vectorizer', CountVectorizer(analyzer='word', token_pattern=r'\w+')),
        ('classifier', MultinomialNB())
    ])
    classifier.fit(training_data, labels)
    return classifier

def save_training_data(training_data, labels, file_path="training_data.json"):
    with open(file_path, "w") as f:
        json.dump([{"name": name, "value": value} for name, value in zip(training_data, labels)], f)

def load_training_data(file_path="training_data.json"):
    initial_data = [
        {"name": "Base.lproj", "value": 1},
        {"name": "en.lproj", "value": 1},
        {"name": "Assets", "value": 0},
        {"name": "Supporting Files", "value": 0},
        {"name": "Other", "value": 0}
    ]

    if not os.path.exists(file_path):
        created = [item["name"] for item in initial_data], [item["value"] for item in initial_data], file_path
        save_training_data(created[0], created[1])
        return created

    else:
        with open(file_path, "r") as f:
            data = json.load(f)
        return [item["name"] for item in data], [item["value"] for item in data]

def save_classifier(classifier, file_path="classifier.pkl"):
    with open(file_path, "wb") as f:
        pickle.dump(classifier, f)

def load_classifier(file_path="classifier.pkl"):
    if not os.path.exists(file_path):
        classifier = train_classifier(training_data, labels)
        save_classifier(classifier, file_path)
        return classifier
    else:
        with open(file_path, "rb") as f:
            classifier = pickle.load(f)
        return classifier

def evaluate_priority(classifier, directory_name):
    return classifier.predict_proba([directory_name])[0][1]

def should_explore(classifier, directory_name, threshold):
    priority = evaluate_priority(classifier, directory_name)
    print('priority', directory_name, priority)
    return priority >= threshold

threshold = 0.2

training_data, labels = load_training_data()
classifier = load_classifier()

def update_training_data(training_data, labels, new_label, new_value):
    training_data.append(new_label)
    labels.append(new_value)

def find_storyboard_files(api_url, access_token):
    global classifier
    found_files = []

    headers = {"Authorization": f"token {access_token}"}

    def explore_directory(url, parent_dir):
        nonlocal found_files
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            contents = json.loads(response.text)
            found_storyboards_in_current_dir = False

            for item in contents:
                if item["type"] == "dir":
                    if should_explore(classifier, item["name"], threshold):
                        explore_directory(item["url"], item["name"])
                elif item["type"] == "file" and item["name"].endswith(".storyboard"):
                    found_files.append(item)
                    found_storyboards_in_current_dir = True

                    dir_name = os.path.dirname(item["path"])
                    names = dir_name.split('/')
                    for name in names:
                        update_training_data(training_data, labels, name, 1)

            # storyboardファイルが見つからなかったときは、ネガティブ情報を更新する
            if not found_storyboards_in_current_dir and parent_dir is not None:
                update_training_data(training_data, labels, parent_dir, 0)

        else:
            print("Error while accessing GitHub API. Status code: ", response.status_code)

    explore_directory(api_url, None)

    # 学習データを保存する
    classifier = train_classifier(training_data, labels)
    save_training_data(training_data, labels)
    save_classifier(classifier)

    return found_files
