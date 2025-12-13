import json
import pandas as pd
from pathlib import Path

EXAM_INFO = {
    "industrial": {
        "examName": "산업안전기사"
    },
    "construction": {
        "examName": "건설안전기사"
    }
}

def convert_excel_to_cbt_json(excel_path: Path, json_path: Path, exam_type: str):
    df = pd.read_excel(excel_path)

    subjects = {}

    for _, row in df.iterrows():
        subject_id = int(row["subject"])
        subject_name = f"{subject_id}과목"

        if subject_id not in subjects:
            subjects[subject_id] = {
                "id": subject_id,
                "name": subject_name,
                "questions": []
            }

        question = {
            "id": row["id"],
            "question": row["question"],
            "options": [
                row["option1"],
                row["option2"],
                row["option3"],
                row["option4"],
            ],
            "answer": int(row["answer"])
        }

        subjects[subject_id]["questions"].append(question)

    exam_json = {
        "examType": exam_type,
        "examName": EXAM_INFO[exam_type]["examName"],
        "subjects": list(subjects.values())
    }

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(exam_json, f, ensure_ascii=False, indent=2)

    print(f"✅ 생성 완료: {json_path}")


if __name__ == "__main__":
    root = Path(__file__).resolve().parents[1] / "data"

    convert_excel_to_cbt_json(
        root / "industrial.xlsx",
        root / "industrial.json",
        "industrial"
    )

    convert_excel_to_cbt_json(
        root / "construction.xlsx",
        root / "construction.json",
        "construction"
    )
