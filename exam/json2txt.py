import json
import os

## modified from json2xml.py to output the questions in a plain text format
##   Question
##      A)  First choice
##      B)  Second choice
##      etc.
#   correct choice: 

def generate_text(json_file_path, output_file_path="moodle_quiz.txt"):
    """
    Reads multiple-choice questions from a JSON file and converts them
    into txt format.
    """
    
    letter_labels = ['A)', 'B)', 'C)', 'D)', 'E)', 'F)']
    
    # 1. Read the JSON data
    try:
        with open(json_file_path, 'r', encoding='utf-8') as f:
            questions_file = json.load(f)
    except FileNotFoundError:
        print(f"Error: Input file not found at '{json_file_path}'")
        return
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from '{json_file_path}'. Check your file format.")
        return
    
    outfile = open(output_file_path, "w")

    questions = questions_file["questions"]
    for q_data in questions:
        outfile.write("question: " + q_data['text'] + '\n')
        indx = 0
        for choice in q_data['choices']:
            outfile.write('\t' + letter_labels[indx] + ' ' + choice + '\n')
            indx += 1
        
        correct_indx = q_data['correct_choice_index'];
        
        outfile.write("correct choice: " + letter_labels[correct_indx] + '\n\n\n')
        
    outfile.close()
        

if __name__ == "__main__":
    # Specify the path to your JSON input file
    input_json_file = "question_bank_v0.1.0.json" 
    
    # Ensure the example JSON file exists for testing
    if not os.path.exists(input_json_file):
        print(f"Creating example JSON file: {input_json_file}")
        example_data = {
            "title": "Parallel & Distributed Computing Exam Question Bank",
            "version": "0.1.0",
            "questions": [
                {
                    "id": 5,
                    "text": "In _________ computing a program's statements are run in order, one at a time.",
                    "topics": [
                        "parallel-computing",
                        "vocabulary"
                    ],
                    "is_ordered": false,
                    "choices": [
                        "sequential",
                        "shared-memory",
                        "core",
                        "parallel"
                    ],
                    "correct_choice_index": 3
                }
                ]
            }
        with open(input_json_file, 'w', encoding='utf-8') as f:
            json.dump(example_data, f, indent=2)
        print(f"Please review and modify the {input_json} file before running the script again.")

    # Run the conversion
    generate_text(input_json_file, 'test_question_bankv0.1.0.txt')