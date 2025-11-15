import os
import requests
import pandas as pd


# 環境変数から API キーを読む（推奨）
API_KEY = os.environ.get("GOOGLE_MAPS_API_KEY")

# 直接ベタ書きしたい場合（自己管理できるならOK）
# API_KEY = "ここにあなたのAPIキー"


def search_massage_shops(query="マッサージ 東京 日本", limit=5):
    """
    Google Places API（Text Search）でマッサージ店を検索し、
    指定件数（limit）分の place_id を返す。
    """
    if not API_KEY:
        raise ValueError("APIキーが設定されていません。GOOGLE_MAPS_API_KEY を環境変数で設定してください。")

    url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    params = {
        "query": query,
        "language": "ja",
        "key": API_KEY,
    }

    resp = requests.get(url, params=params, timeout=10)
    resp.raise_for_status()
    data = resp.json()

    results = data.get("results", [])
    # 上位 limit 件だけ使う
    return [r["place_id"] for r in results[:limit]]


def get_place_detail(place_id):
    """
    Place Details API で店の詳細情報を取得する。
    ここでは、店名・住所・電話番号・WebサイトURLを取得。
    """
    url = "https://maps.googleapis.com/maps/api/place/details/json"
    params = {
        "place_id": place_id,
        "language": "ja",
        "fields": "name,formatted_address,formatted_phone_number,website",
        "key": API_KEY,
    }

    resp = requests.get(url, params=params, timeout=10)
    resp.raise_for_status()
    data = resp.json()

    result = data.get("result", {})

    return {
        "店名": result.get("name"),
        "住所": result.get("formatted_address"),
        "電話番号": result.get("formatted_phone_number"),
        "WebサイトURL": result.get("website"),
    }


def main():
    # 1) マッサージ店の place_id を 5件取得
    place_ids = search_massage_shops()

    # 2) 各 place_id について詳細情報を取得
    rows = []
    for pid in place_ids:
        detail = get_place_detail(pid)
        rows.append(detail)

    # 3) CSV に保存
    df = pd.DataFrame(rows)
    output_path = "massage_sample_auto.csv"
    df.to_csv(output_path, index=False, encoding="utf-8-sig")

    print(f"{len(rows)}件のマッサージ店情報を {output_path} に出力しました。")


if __name__ == "__main__":
    main()
