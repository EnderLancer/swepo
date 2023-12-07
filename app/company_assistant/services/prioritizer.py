from typing import NamedTuple

from company_assistant.models import Company, CompanySpecific, ProcessPractice


MAX_COMPANY_SPECIFIC_SCORE = 5


class PriorityOrderedPracticeDTO(NamedTuple):
    practice_code: str
    process_code: str
    priority: float

class Prioritizer():
    def __init__(
            self,
            company: Company
    ) -> None:
        self.company = company
        self.prioritized_practices = list()

    def prioritize(self) -> None:
        all_practices = ProcessPractice.objects.select_related("process").prefetch_related("specificpracticeweightrelation_set__specific__companyspecific_set").all()
        for practice in all_practices:
            values = []
            specifics_weights = practice.specificpracticeweightrelation_set.only("specific", "weight")
            for specifics_weight in specifics_weights:
                try:
                    company_score = specifics_weight.specific.companyspecific_set.get(company=self.company).score
                except CompanySpecific.DoesNotExist:
                    continue
                weight = specifics_weight.weight
                values.append(company_score*float(weight)/MAX_COMPANY_SPECIFIC_SCORE)

            result_priority = sum(values) / len(values) if values else 0.
            self.prioritized_practices.append(
                PriorityOrderedPracticeDTO(
                    practice_code=practice.code,
                    process_code=practice.process.code,
                    priority=result_priority,
                )
            )
    
    def get_sorted_by_practices(self):
        if not self.prioritized_practices:
            self.prioritize()
        return sorted(
            self.prioritized_practices,
            key=lambda x: x.priority,
            reverse=True
        )