import re
import json
import pandas as pd
from pathlib import Path


LICENSE_INFO = {
    "industrial": "산업안전기사",
    "construction": "건설안전기사",
}


def parse_question_block(block: str):
    block = block.strip()

    id_match = re.search(r'id:\s*"([^"]+)"', block)
    qid = id_match.group(1) if id_match else None

    license_type = (
        "industrial" if "industrial" in block else "construction"
    )

    subject_match = re.search(r'subject:\s*(\d+)', block)
    subject = int(subject_match.group(1)) if subject_match else 1

    difficulty_match = re.search(
        r'difficulty:\s*Difficulty\.([a-zA-Z]+)', block
    )
    difficulty = difficulty_match.group(1) if difficulty_match else None

    q_match = re.search(r'question:\s*"([^"]+)"', block)
    question = q_match.group(1) if q_match else ""

    opt_match = re.search(r'options:\s*\[([^\]]+)\]', block)
    if opt_match:
        options_raw = opt_match.group(1)
        choices = [o.strip().strip('"') for o in options_raw.split(",")]
    else:
        choices = []

    ans_match = re.search(r'answer:\s*(\d+)', block)
    answer = int(ans_match.group(1)) - 1 if ans_match else None

    return {
        "id": qid,
        "subject": subject,
        "question": question,
        "choices": choices,
        "answer": answer,
        "difficulty": difficulty,
        "explanation": "",
    }


def convert_excel_to_exam_json(excel_path, json_path, exam_type):
    df = pd.read_excel(excel_path, header=None)

    subjects = {}
    buffer = ""

    for _, row in df.iterrows():
        line = str(row[0])

        if line.startswith("Question("):
            buffer = line + "\n"
        elif ")" in line and "Question" not in line:
            buffer += line
            q = parse_question_block(buffer)

            subject_no = q["subject"]
            subjects.setdefault(
                subject_no,
                {
                    "code": f"SUBJECT_{subject_no}",
                    "name": f"과목 {subject_no}",
                    "questions": [],
                },
            )

            subjects[subject_no]["questions"].append(q)
            buffer = ""
        else:
            buffer += line + "\n"

    exam = {
        "examType": exam_type,
        "examName": LICENSE_INFO.get(exam_type, exam_type),
        "subjects": list(subjects.values()),
    }

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(exam, f, ensure_ascii=False, indent=2)

    print(f"✓ 변환 완료 → {json_path}")


if __name__ == "__main__":
    root = Path(__file__).resolve().parents[1] / "data"

    convert_excel_to_exam_json(
        root / "industrial.xlsx",
        root / "industrial.json",
        "industrial",
    )

    convert_excel_to_exam_json(
        root / "construction.xlsx",
        root / "construction.json",
        "construction",
    )
