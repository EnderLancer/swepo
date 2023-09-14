
specifics = {
    1: "Critical infrastructure",
    2: "Short projects",
    3: "B2B",
    4: "Outsourcing",
    5: "Product company"
}

practices = {
    1: "Requirement Analysis",
    2: "Development",
    3: "Testing",
    4: "Deploying",
    5: "Maintaining",
}

specific_to_practices = {
    (1, 1): 2,
    (1, 2): 1,
    (1, 3): 5,
    (1, 4): 1,
    (1, 5): 3,
    (5, 1): 3,
    (5, 2): 3,
    (5, 3): 3,
    (5, 4): 1,
    (5, 5): 2,
}

def evaluate_importance_score(
        process: int,
        chosen_specifics: list,
        specific_to_process: dict,
    ):
    score = 0.
    for specific in chosen_specifics:
        percent = specific_to_process.get(
            (specific, process),
        )
        if percent:
            score += percent
    return score #/ count


def main():
    # result: {process:importance_percent}
    result = {}
    chosen_specifics = [1, 5]
    sum_score = 0.
    for process_i, process_name in practices.items():
        process_score = evaluate_importance_score(
            process=process_i,
            chosen_specifics=chosen_specifics,
            specific_to_process=specific_to_practices,
        )
        result[process_name] = process_score
        sum_score += process_score
    for process in result:
        result[process] /= sum_score
    print(sorted(result.items(), key=lambda item: item[1], reverse=True))
    print(sum(result.values()))

if __name__ == "__main__":
    main()
