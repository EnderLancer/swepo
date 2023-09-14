from company_assistant.models import (
    Company,
    SpecificPracticeWeightRelation,
    ProcessCategory,
    SwdProcess,
    ProcessPractice,
    Specific,
    CompanySpecific
)

spec_to_create = {
    1: "Critical infrastructure",
    2: "Short projects",
    3: "B2B",
    4: "Outsourcing",
    5: "Product company"
}
# spec_for_bulk = [Specific(name=name) for name in spec_to_create.values()]
# Specific.objects.bulk_create(spec_for_bulk)
specifics = Specific.objects.all()

# dummy_process_category = ProcessCategory.objects.create(name="Dummy Category", code="DUMMY")
# dummy_process = SwdProcess.objects.create(name="Dummy Process", category=dummy_process_category)

prac_to_create = {
    1: "Requirement Analysis",
    2: "Development",
    3: "Testing",
    4: "Deploying",
    5: "Maintaining",
}
# prac_for_bulk = [
#     ProcessPractice(
#         name=name,
#         process=dummy_process
#     ) 
#     for name in prac_to_create.values()
# ]
# ProcessPractice.objects.bulk_create(prac_for_bulk)
practices = ProcessPractice.objects.all()

spec_prac_mapping_to_create = {
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
# for spec_prac in spec_prac_mapping_to_create:
#     spec_name = spec_to_create[spec_prac[0]]
#     prac_name = prac_to_create[spec_prac[1]]

#     spec_obj = Specific.objects.get(name=spec_name)
#     prac_obj = ProcessPractice.objects.get(name=prac_name)

#     SpecificPracticeWeightRelation.objects.create(
#         specific=spec_obj,
#         practice=prac_obj,
#         weight=spec_prac_mapping_to_create[spec_prac]
#     )

# company_spec_to_create = [1, 5]
# for comp_spec in company_spec_to_create:
#     spec_obj = Specific.objects.get(name=spec_to_create[comp_spec])
#     company = Company.objects.get(name="Test 1 again")
#     CompanySpecific.objects.create(
#         specific=spec_obj,
#         company=company
#     )


def evaluate_importance_score(
        practice: int,
        chosen_specifics: list,
    ):
    score = 0.
    for specific in chosen_specifics.values("specific_id"):
        try:
            weight = SpecificPracticeWeightRelation.objects.get(
                specific_id=specific["specific_id"],
                practice=practice
            ).weight
        except SpecificPracticeWeightRelation.DoesNotExist:
            weight = 0.
        score += float(weight)
    return score


def main():
    # result: {process:importance_percent}
    result = {}
    chosen_specifics = CompanySpecific.objects.all()
    for process in SwdProcess.objects.all():
        result[process.name] = {}
        sum_score = 0.
        for practice in process.practices.all():
            score = evaluate_importance_score(
                practice=practice,
                chosen_specifics=chosen_specifics,
            )
            result[process.name][practice.name] = score
            sum_score += score
        for practice in result[process.name]:
            result[process.name][practice] /= sum_score
        result[process.name] = dict(sorted(result[process.name].items(), key=lambda item: item[1], reverse=True))
    return result

if __name__ == "__main__":
    main()
