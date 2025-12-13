import json
import pandas as pd
from pathlib import Path

def build_exam_json(excel_path, exam_type, exam_name, output_path):
    df = pd.read_excel(excel_path)

    # 🔥 NaN 제거
    df = df.fillna("")

    subjects = []

    for subject_id in sorted(df["subject"].unique()):
        sdf = df[df["subject"] == subject_id]

        questions = []
        for _, row in sdf.iterrows():
            questions.append({
                "id": row["id"],
                "question": row["question"],
                "options": [
                    row["option1"],
                    row["option2"],
                    row["option3"],
                    row["option4"],
                ],
                "answer": int(row["answer"]),
            })

        subjects.append({
            "id": int(subject_id),
            "name": f"{subject_id}과목",
            "questions": questions,
        })

    exam_json = {
        "examType": exam_type,
        "examName": exam_name,
        "subjects": subjects,
    }

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(exam_json, f, ensure_ascii=False, indent=2)

    print(f"✅ CBT JSON 생성 완료: {output_path}")

if __name__ == "__main__":
    root = Path(__file__).resolve().parents[1] / "data"

    build_exam_json(
        root / "industrial.xlsx",
        "industrial",
        "산업안전기사",
        root / "industrial.json",
    )

    build_exam_json(
        root / "construction.xlsx",
        "construction",
        "건설안전기사",
        root / "construction.json",
    )
