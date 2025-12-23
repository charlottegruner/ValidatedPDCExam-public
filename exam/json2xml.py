import json
import os

## Got help from Gemini on this script 

def generate_moodle_xml(json_file_path, output_file_path="moodle_quiz.xml"):
    """
    Reads multiple-choice questions from a JSON file and converts them
    into Moodle XML format.
    """
    
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

    # XML components
    xml_header = '<?xml version="1.0" encoding="UTF-8"?>\n<quiz>\n'
    xml_footer = '</quiz>'
    question_xml_list = []
    
    questions = questions_file["questions"]

    # 2. Iterate through each question and build the XML
    for q_data in questions:
        # Start the question block
        question_xml = f"""
  <question type="multichoice">
    <name>
      <text>{q_data['id']}</text>
    </name>
    <questiontext format="html">
      <text><![CDATA[<p>{q_data['text']}</p>]]></text>
    </questiontext>
    <single>{'true'}</single>
"""
        
        # Add answer choices
        indx = 0
        correct_indx = q_data['correct_choice_index'];
        for answer in q_data['choices']:
            if indx == correct_indx:
                fraction = 100
            else:
                fraction = 0
            answer_xml = f"""
    <answer fraction="{fraction}">
      <text><![CDATA[<p>{answer}</p>]]></text>
    </answer>
"""
            question_xml += answer_xml
            indx += 1

        # Close the question block
        question_xml += '  </question>\n'
        question_xml_list.append(question_xml)

    # 3. Combine and write the final XML
    final_xml_content = xml_header + "".join(question_xml_list) + xml_footer
    
    try:
        with open(output_file_path, 'w', encoding='utf-8') as f:
            f.write(final_xml_content)
        print(f"\n✅ Successfully generated Moodle XML file at: {os.path.abspath(output_file_path)}")
        print(f"   Total questions converted: {len(questions)}")
    except IOError:
        print(f"Error: Could not write to output file '{output_file_path}'.")


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
    generate_moodle_xml(input_json_file, 'test_question_bankv0.1.0.xml')