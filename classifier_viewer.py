import json
import os
import pickle

from storyboard_search import load_classifier, load_training_data, evaluate_priority

def display_sorted_directory_values(classifier, training_data):
    directory_values = [(name, evaluate_priority(classifier, name)) for name in training_data]
    sorted_directory_values = sorted(directory_values, key=lambda x: x[1], reverse=True)

    for name, value in sorted_directory_values:
        print(f"{name}: {value:.2f}")

def main():
    classifier_file_path = "classifier.pkl"
    training_data_file_path = "training_data.json"

    if not os.path.exists(classifier_file_path) or not os.path.exists(training_data_file_path):
        print("Error: Classifier or training data file not found.")
    else:
        classifier = load_classifier(classifier_file_path)
        training_data, labels = load_training_data(training_data_file_path)
        training_data = list(set(training_data))
        display_sorted_directory_values(classifier, training_data)

if __name__ == "__main__":
    main()

