from collections import defaultdict
from typing import Dict, List

from company_assistant.models import Company
from company_assistant.services.prioritizer import Prioritizer


MAX_COMPANY_SPECIFIC_SCORE = 5


class Evaluator():
    def __init__(
            self,
            company: Company,
            practice_attributes: Dict[str, List[str]]
    ) -> None:
        self.prioritizer = Prioritizer(company=company)
        self.attributes_per_practice = practice_attributes
        self.process_practices = defaultdict(list)
        self._categorize_practices_by_process()
        self.prioritizer.selected_processes = self.process_practices.keys()

        self.prioritized_practices = self.prioritizer.get_sorted_by_practices()
        self.overall_score = 0.
        self.process_scores = dict()
        self.practice_scores = dict()

    def _categorize_practices_by_process(self):
        self.process_practices = defaultdict(list)
        for practice in self.attributes_per_practice:
            process_name, _ = practice.rsplit(".", 1)
            self.process_practices[process_name].append(practice)

    def _eval_practice_level(self, practice: str):
        score = 0
        attributes = self.attributes_per_practice[practice]
        if attributes[0] in ["W", "N", "P"]:
            score = 0
        elif (attributes[1] in ["W", "N", "P"]
            or attributes[2] in ["W", "N", "P"]
            or any([attr != "F" for attr in attributes[:1]])):
            score = 1
        elif (attributes[3] in ["W", "N", "P"]
            or attributes[4] in ["W", "N", "P"]
            or any([attr != "F" for attr in attributes[:3]])):
            score = 2
        elif (attributes[5] in ["W", "N", "P"]
            or attributes[6] in ["W", "N", "P"]
            or any([attr != "F" for attr in attributes[:5]])):
            score = 3
        elif (attributes[7] in ["W", "N", "P"]
            or attributes[8] in ["W", "N", "P"]
            or any([attr != "F" for attr in attributes[:7]])):
            score = 4
        else:
            score = 5

        self.practice_scores[practice] = score
        return score

    def _eval_process_level(
            self,
            process_code: str
        ):
        process_priorities = {
            prior_practices.practice_code: prior_practices.priority
            for prior_practices in self.prioritized_practices
            if prior_practices.process_code == process_code
        }
        sum_priorities = sum(process_priorities.values())
        process_score = 0.
        if sum_priorities:
            coef = len(process_priorities) / sum_priorities
            weighted_process_priorities = [
                priority * coef * self.practice_scores[practice]
                for practice, priority in process_priorities.items()
            ]
            process_score = sum(weighted_process_priorities) / len(weighted_process_priorities)
        self.process_scores[process_code] = process_score
        return process_score

    def _eval_overall_level(self):
        self.overall_score = sum(self.process_scores.values()) / len(self.process_scores)
        return self.overall_score

    def evaluate(self):
        for process, practices in self.process_practices.items():
            for practice in practices:
                self._eval_practice_level(practice=practice)
            self._eval_process_level(process_code=process)
        return self._eval_overall_level()
        

