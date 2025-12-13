import json
import pandas as pd
from pathlib import Path
from collections import defaultdict

def build_exam_json(exam_type, exam_name, excel_path, output_path):
    df = pd.read_excel(excel_path)

    subjects = defaultdict(list)

    for _, row in df.iterrows():
        q = {
            "id": row["id"],
            "question": row["question"],
            "options": [
                str(row["option1"]),
                str(row["option2"]),
                str(row["option3"]),
                str(row["option4"]),
            ],
            "answer": int(row["answer"]),
        }
        subjects[int(row["subject"])].append(q)

    result = {
        "examType": exam_type,
        "examName": exam_name,
        "subjects": []
    }

    for subject_id in sorted(subjects.keys()):
        result["subjects"].append({
            "id": subject_id,
            "name": f"{subject_id}과목",
            "questions": subjects[subject_id]
        })

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"✅ 생성 완료: {output_path}")

if __name__ == "__main__":
    root = Path(__file__).resolve().parents[1] / "data"

    build_exam_json(
        exam_type="industrial",
        exam_name="산업안전기사",
        excel_path=root / "industrial.xlsx",
        output_path=root / "industrial.json",
    )

    build_exam_json(
        exam_type="construction",
        exam_name="건설안전기사",
        excel_path=root / "construction.xlsx",
        output_path=root / "construction.json",
    )
