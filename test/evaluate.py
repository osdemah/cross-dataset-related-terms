import requests
import json
import sys
from typing import List
from gensim.models.keyedvectors import KeyedVectors
import numpy as np
import time


def query(api_server, term):
    result = requests.post(api_server, data=json.dumps({"term": term}))
    return [x["relatedTerm"] for x in result.json()]


def check_similarity(model, term, related_term):
    try:
        return model.similarity(term, related_term)
    except KeyError:
        return None


def evaluate(model: KeyedVectors, term: str, related_terms: List[str]):
    similarity_threshold = 0.33
    success_threshold = 3
    similarities = list(filter(lambda x: x is not None,
                          [check_similarity(model, term, related_term) for related_term in related_terms]))
    if len(similarities) == 0:
        raise KeyError()
    print("similarities:", similarities)
    matched_terms = sum([int(similarity >= similarity_threshold) for similarity in similarities])
    return int(matched_terms >= success_threshold)


def main():
    model_path = sys.argv[1]
    dataset = sys.argv[2]
    web_api = sys.argv[3]
    model = KeyedVectors.load_word2vec_format(model_path, binary=True)
    terms = []
    accuracies = []
    latencies = []
    with open(dataset) as dataset_file:
        for line in dataset_file:
            terms.append(line.strip().lower())
    i = 0
    n = len(terms)
    for term in terms:
        start = time.time()
        related_terms = query(web_api, term)
        latencies.append(time.time() - start)
        print(f"{i}/{n}: {term} -> {related_terms}")
        i += 1
        try:
            accuracy = evaluate(model, term, related_terms)
        except KeyError:
            continue
        accuracies.append(accuracy)
    print("average accuracy", np.average(accuracies))
    print("average latency", np.average(latencies))
    print("P90 latency", np.percentile(latencies, 90))


if __name__ == '__main__':
    main()
