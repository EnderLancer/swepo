
specifics = {
    1: "Critical infrastructure",
    2: "Short projects",
    3: "B2B",
    4: "Outsourcing",
    5: "Product company"
}

processes = {
    1: "Requirement Analysis",
    2: "Development",
    3: "Testing",
    4: "Deploying",
    5: "Maintaining",
}

specific_to_process = {
    (1, 1): 0.2,
    (1, 2): 0.1,
    (1, 3): 0.5,
    (1, 4): 0.1,
    (1, 5): 0.3,
    (5, 1): 0.3,
    (5, 2): 0.3,
    (5, 3): 0.3,
    (5, 4): 0.1,
    (5, 5): 0.2,
}

def evaluate_importance_score(
        process: int,
        chosen_specifics: list,
        specific_to_process: dict,
    ):
    score = 0.
    count = 0
    for specific in chosen_specifics:
        percent = specific_to_process.get(
            (specific, process),
        )
        if percent:
            score += percent
            count += 1
    if count:
        return score / count
    else:
        return 0


def main():
    # result: {process:importance_score}
    result = {}
    chosen_specifics = [1, 5]
    for process_i, process_name in processes.items():
        process_score = evaluate_importance_score(
            process=process_i,
            chosen_specifics=chosen_specifics,
            specific_to_process=specific_to_process,
        )
        result[process_name] = process_score
    print(sorted(result.items(), key=lambda item: item[1], reverse=True))

if __name__ == "__main__":
    main()
