import re
import json
import pandas as pd
from pathlib import Path


def parse_question_block(block: str):
    """Question(...) 형태 텍스트를 JSON dict로 변환"""
    block = block.strip()

    id_match = re.search(r'id:\s*"([^"]+)"', block)
    qid = id_match.group(1) if id_match else None

    # 산업 / 건설 자동 판단
    license_type = "industrial" if "industrial" in block else "construction"

    subject_match = re.search(r'subject:\s*(\d+)', block)
    subject = int(subject_match.group(1)) if subject_match else None

    difficulty_match = re.search(r'difficulty:\s*Difficulty\.([a-zA-Z]+)', block)
    difficulty = difficulty_match.group(1) if difficulty_match else None

    q_match = re.search(r'question:\s*"([^"]+)"', block)
    question = q_match.group(1) if q_match else ""

    opt_match = re.search(r'options:\s*\[([^\]]+)\]', block)
    if opt_match:
        options_raw = opt_match.group(1)
        options = [o.strip().strip('"') for o in options_raw.split(",")]
    else:
        options = []

    ans_match = re.search(r'answer:\s*(\d+)', block)
    answer = int(ans_match.group(1)) if ans_match else None

    return {
        "id": qid,
        "license": license_type,
        "subject": subject,
        "difficulty": difficulty,
        "question": question,
        "options": options,
        "answer": answer,
    }


def convert_excel_to_json(excel_path, json_path):
    df = pd.read_excel(excel_path, header=None)

    questions = []
    buffer = ""

    for _, row in df.iterrows():
        line = str(row[0])

        if line.startswith("Question("):
            buffer = line + "\n"
        elif ")" in line and "Question" not in line:
            buffer += line
            q = parse_question_block(buffer)
            questions.append(q)
            buffer = ""
        else:
            buffer += line + "\n"

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(questions, f, ensure_ascii=False, indent=2)

    print(f"✓ 변환 완료 → {json_path} (총 {len(questions)}문제)")


if __name__ == "__main__":
    root = Path(__file__).resolve().parents[1] / "data"

    convert_excel_to_json(root / "industrial.xlsx", root / "industrial.json")
    convert_excel_to_json(root / "construction.xlsx", root / "construction.json")
