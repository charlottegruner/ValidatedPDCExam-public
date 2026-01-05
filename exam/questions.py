import pprint
import random
import copy
import textwrap
import json

letters = ['a.', 'b.', 'c.', 'd.', 'e.', 'f.', 'g.']

class MultipleChoiceQuestion:
    def __init__(self, id, text, topics=None, is_ordered = False, choices = [], correct_choice_index = None):
        self.id = id
        self.text = text
        self.topics = topics if topics is not None else []
        self.is_ordered = is_ordered
        self.choices = choices
        self.correct_choice_index = correct_choice_index

    def __str__(self):
        return self.to_markdown()

    def to_json(self):
        return json.dumps(self)

    def to_markdown(self, number = None):
        topics_str = " ".join("#" + topic for topic in self.topics)
        print_choices = copy.deepcopy(self.choices)
        if not self.is_ordered:
            random.shuffle(print_choices)
        choices_str = ""
        i = 0
        for c in print_choices:
            choices_str += f"\t{letters[i]} {c}\n"
            if c == self.choices[self.correct_choice_index]:
                answer = letters[i]
            i += 1
        return f"""
Question {number or ''}({self.id}): {self.text}
Topics: {topics_str}
Answer: {answer}
Choices:  \n{choices_str}\n\n
"""

    def to_json(self):
        return json.dumps({
            "id": question.id,
            "text": question.text,
            "topics": question.topics,
            "is_ordered": question.is_ordered,
            "choices": question.choices,
            "correct_choice_index": question.correct_choice_index
        }, indent=4)

def questions_from_json_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        data = json.load(file)

    questions_data = data.get("questions", [])

    questions = []
    for q in questions_data:
        question = MultipleChoiceQuestion(
            id=q["id"],
            text=q["text"],
            topics=q.get("topics", []),
            is_ordered=q.get("is_ordered", False),
            choices=q["choices"],
            correct_choice_index=q["correct_choice_index"]
        )
        questions.append(question)

    return questions


questions = questions_from_json_file("question_bank_v0.1.1.json")


pprint.pprint(f"REPORTS")
pprint.pprint(f"number of questions: {len(questions)}")
topics = [ t for q in questions for t in q.topics ]
topics_unique = set(topics)
question_topic_count = { t:topics.count(t) for t in topics_unique }
pprint.pprint(question_topic_count)

#random.shuffle(questions)
for q in questions:
   print(q)
