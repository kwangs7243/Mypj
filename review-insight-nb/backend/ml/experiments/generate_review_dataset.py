from pathlib import Path
import argparse
import csv
import random


BASE_DIR = Path(__file__).resolve().parents[2]
OUTPUT_PATH = BASE_DIR / "data" / "generated" / "generated_reviews_5k.csv"
DEFAULT_ROW_COUNT = 5000
DEFAULT_SEED = 42

PRODUCTS = [
    "이어폰",
    "노트북",
    "키보드",
    "마우스",
    "모니터",
    "의자",
    "책상",
    "가방",
    "운동화",
    "공기청정기",
    "청소기",
    "커피머신",
    "보조배터리",
    "충전기",
    "스피커",
    "태블릿",
    "선풍기",
    "헤드셋",
    "스탠드",
    "물병",
]

TOPICS = [
    ("배송", ["배송이 빠르고", "배송 상태가 깔끔하고", "예상보다 빨리 도착해서"]),
    ("가격", ["가격 대비 만족도가 높고", "할인받아 사서 더 만족스럽고", "이 가격이면 충분히 괜찮고"]),
    ("품질", ["품질이 안정적이고", "마감이 깔끔하고", "전체적인 완성도가 좋고"]),
    ("사용감", ["사용하기 편하고", "처음 써도 적응이 쉽고", "매일 쓰기 부담 없고"]),
    ("응대", ["문의 응대가 친절하고", "교환 안내가 빠르고", "상담이 자세해서"]),
    ("포장", ["포장이 튼튼하고", "박스 손상 없이 와서", "구성품이 빠짐없이 와서"]),
    ("내구성", ["며칠 써보니 튼튼하고", "반복 사용해도 문제 없고", "생각보다 오래 쓸 수 있을 것 같고"]),
]

NEGATIVE_TOPICS = [
    ("배송", ["배송이 너무 늦고", "배송 중 파손이 있었고", "도착 일정이 계속 밀려서"]),
    ("가격", ["가격에 비해 아쉽고", "할인해도 비싸게 느껴지고", "비슷한 제품보다 만족도가 낮고"]),
    ("품질", ["품질이 기대보다 떨어지고", "마감이 거칠고", "전체적인 완성도가 아쉽고"]),
    ("사용감", ["사용하기 불편하고", "처음부터 적응이 어렵고", "매일 쓰기에는 부담스럽고"]),
    ("응대", ["문의 응대가 늦고", "교환 안내가 불친절하고", "상담이 부정확해서"]),
    ("포장", ["포장이 허술하고", "박스가 찌그러져 와서", "구성품이 빠져 있어서"]),
    ("내구성", ["며칠 쓰니 고장나고", "반복 사용하니 문제가 생기고", "생각보다 오래 못 쓸 것 같고"]),
]

POSITIVE_ENDINGS = [
    "전체적으로 만족합니다",
    "다시 구매하고 싶습니다",
    "주변에 추천할 만합니다",
    "기대보다 좋은 선택이었습니다",
    "실사용 만족도가 높습니다",
    "후회 없는 구매였습니다",
    "다음에도 이 제품을 고를 것 같습니다",
]

NEGATIVE_ENDINGS = [
    "전체적으로 실망했습니다",
    "다시 구매하고 싶지 않습니다",
    "주변에 추천하기 어렵습니다",
    "기대보다 아쉬운 선택이었습니다",
    "실사용 만족도가 낮습니다",
    "구매를 후회했습니다",
    "다음에는 다른 제품을 고를 것 같습니다",
]

NOISE_PREFIXES = ["", "", "", "2026년 기준 ", "솔직히 ", "개인적으로 ", "review: "]
NOISE_SUFFIXES = ["", "", "", ".", "!", "!!", "  ", " :)"]
POSITIVE_RATINGS = ["", "", "", " 별점 5점", " score 10"]
NEGATIVE_RATINGS = ["", "", "", " 별점 1점", " score 2"]


def build_review(label: str) -> str:
    product = random.choice(PRODUCTS)

    if label == "positive":
        _, topic_phrases = random.choice(TOPICS)
        topic_phrase = random.choice(topic_phrases)
        ending = random.choice(POSITIVE_ENDINGS)
        rating = random.choice(POSITIVE_RATINGS)
    else:
        _, topic_phrases = random.choice(NEGATIVE_TOPICS)
        topic_phrase = random.choice(topic_phrases)
        ending = random.choice(NEGATIVE_ENDINGS)
        rating = random.choice(NEGATIVE_RATINGS)

    prefix = random.choice(NOISE_PREFIXES)
    suffix = random.choice(NOISE_SUFFIXES)
    spacer = random.choice([" ", "  ", " "])

    return f"{prefix}{product} 제품은 {topic_phrase}{spacer}{ending}{rating}{suffix}"


def generate_reviews(row_count: int, seed: int) -> list[dict[str, str]]:
    if row_count <= 0:
        raise ValueError("row_count must be greater than 0.")

    random.seed(seed)
    positive_count = row_count // 2
    negative_count = row_count - positive_count

    rows = [
        {"text": build_review("positive"), "label": "positive"}
        for _ in range(positive_count)
    ]
    rows.extend(
        {"text": build_review("negative"), "label": "negative"}
        for _ in range(negative_count)
    )

    random.shuffle(rows)
    return rows


def save_reviews(rows: list[dict[str, str]], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["text", "label"])
        writer.writeheader()
        writer.writerows(rows)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate a controlled synthetic Korean review dataset."
    )
    parser.add_argument("--rows", type=int, default=DEFAULT_ROW_COUNT)
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED)
    parser.add_argument("--output", type=Path, default=OUTPUT_PATH)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    rows = generate_reviews(row_count=args.rows, seed=args.seed)
    save_reviews(rows, args.output)

    label_counts = {"positive": 0, "negative": 0}
    for row in rows:
        label_counts[row["label"]] += 1

    print(f"Rows: {len(rows)}")
    print(f"Label counts: {label_counts}")
    print(f"Saved to: {args.output}")


if __name__ == "__main__":
    main()
