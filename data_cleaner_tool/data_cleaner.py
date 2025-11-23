import pandas as pd
import re

def normalize_phone(tel: str) -> str:
    """電話番号を数字のみの形式に整形"""
    if pd.isna(tel):
        return ""
    return re.sub(r"\D", "", str(tel))

def extract_email(text: str) -> str:
    """メールアドレスを抽出（正規表現）"""
    if pd.isna(text):
        return ""
    match = re.search(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", str(text))
    return match.group(0) if match else ""

def clean_columns(df: pd.DataFrame) -> pd.DataFrame:
    """列名の統一（小文字化・スペース除去）"""
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]
    return df

def clean_data(input_path: str, output_path: str):
    df = pd.read_csv(input_path)

    df = clean_columns(df)

    if "tel" in df.columns:
        df["tel"] = df["tel"].apply(normalize_phone)

    if "mail" in df.columns:
        df["mail"] = df["mail"].apply(extract_email)

    # 1) メールアドレスが入っている行を優先するために並べ替え
    df = df.sort_values(by=["mail"], ascending=False)

    # 2) 「name + tel + address」が同じものは重複として1つにまとめる
    df = df.drop_duplicates(subset=["name", "tel", "address"])

    df["category"] = "自動付与"

    df.to_csv(output_path, index=False)
    print(f"整形済みデータを {output_path} に出力しました。")


if __name__ == "__main__":
    clean_data("sample_input.csv", "sample_output.csv")
