#!/usr/bin/env python3
"""Generate a static daily market summary report.

The script is intended to run from GitHub Actions every morning in the
Asia/Seoul timezone. It stores both a latest HTML report and a dated archive
under reports/ so GitHub Pages can publish the generated files.
"""

from __future__ import annotations

import json
import math
import os
from dataclasses import asdict, dataclass
from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

import FinanceDataReader as fdr
from jinja2 import Template

KST = ZoneInfo("Asia/Seoul")
ROOT = Path(__file__).resolve().parents[1]
REPORT_ROOT = ROOT / "reports"
LOOKBACK_DAYS = int(os.environ.get("MARKET_SUMMARY_LOOKBACK_DAYS", "21"))

SECTIONS = [
    {
        "title": "국내",
        "layout": "grid",
        "items": [
            {"name": "코스피", "symbol": "KS11"},
            {"name": "코스닥", "symbol": "KQ11"},
        ],
    },
    {
        "title": "해외",
        "layout": "grid",
        "items": [
            {"name": "다우 산업", "symbol": "DJI"},
            {"name": "나스닥 종합", "symbol": "IXIC"},
            {"name": "S&P 500", "symbol": "US500"},
            {"name": "니케이225", "symbol": "N225"},
        ],
    },
    {
        "title": "환율",
        "layout": "grid",
        "items": [
            {"name": "원/달러", "symbol": "USD/KRW"},
            {"name": "중국 위안/달러", "symbol": "USD/CNY", "precision": 4},
        ],
    },
    {
        "title": "상품",
        "layout": "table",
        "items": [
            {"name": "금", "symbol": "GC=F"},
            {"name": "은", "symbol": "SI=F"},
            {"name": "WTI", "symbol": "CL=F"},
        ],
    },
]

HTML_TEMPLATE = """<!doctype html>
<html lang="ko">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>전일 시장 요약 - {{ generated_date }}</title>
  <style>
    :root {
      color-scheme: light;
      --border: #e8e8e8;
      --border-strong: #d7d7d7;
      --text: #333;
      --muted: #777;
      --up: #cf5f58;
      --down: #2f7eb7;
      --flat: #777;
      --background: #fff;
      --cell: #fbfbfb;
    }
    * { box-sizing: border-box; }
    body {
      margin: 0;
      background: var(--background);
      color: var(--text);
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Noto Sans KR", sans-serif;
      line-height: 1.5;
    }
    main {
      width: min(720px, 100%);
      margin: 0 auto;
      padding: 28px 24px 48px;
    }
    h1 {
      margin: 0 0 28px;
      font-size: clamp(1.8rem, 5vw, 2.6rem);
      font-weight: 800;
      letter-spacing: -0.04em;
    }
    .meta {
      margin: -16px 0 30px;
      color: var(--muted);
      font-size: 0.95rem;
    }
    section { margin: 0 0 34px; }
    h2 {
      margin: 0 0 12px;
      font-size: clamp(1.3rem, 4vw, 1.75rem);
      font-weight: 800;
      letter-spacing: -0.04em;
    }
    .market-grid,
    .commodity-table {
      border-top: 3px solid var(--border-strong);
      border-bottom: 1px solid var(--border);
    }
    .market-grid {
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
    }
    .market-card {
      min-height: 96px;
      display: grid;
      place-items: center;
      padding: 16px 12px;
      text-align: center;
      border-bottom: 1px solid var(--border);
      background: var(--cell);
    }
    .market-card:nth-child(odd) { border-right: 1px solid var(--border); }
    .market-card h3 {
      margin: 0 0 16px;
      font-size: clamp(1rem, 3.5vw, 1.3rem);
      font-weight: 800;
    }
    .value {
      margin: 0;
      font-size: clamp(0.98rem, 3vw, 1.12rem);
      font-weight: 700;
      white-space: nowrap;
    }
    .up { color: var(--up); }
    .down { color: var(--down); }
    .flat { color: var(--flat); }
    .commodity-table {
      width: 100%;
      border-collapse: collapse;
      font-size: clamp(1rem, 3.2vw, 1.15rem);
    }
    .commodity-table th,
    .commodity-table td {
      padding: 15px 18px;
      border-bottom: 1px solid var(--border);
      background: var(--cell);
    }
    .commodity-table th {
      width: 32%;
      text-align: center;
      font-weight: 800;
      border-right: 1px solid var(--border);
    }
    .commodity-table td { font-weight: 700; }
    .notice {
      margin-top: 36px;
      padding-top: 18px;
      border-top: 1px solid var(--border);
      color: var(--muted);
      font-size: 0.88rem;
    }
    .notice ul { margin: 8px 0 0; padding-left: 18px; }
    @media (max-width: 520px) {
      main { padding: 24px 16px 40px; }
      .market-card { min-height: 86px; }
      .commodity-table th,
      .commodity-table td { padding: 13px 12px; }
    }
  </style>
</head>
<body>
  <main>
    <h1>전일 시장 요약</h1>
    <p class="meta">생성 시각: {{ generated_at }} KST</p>

    {% for section in sections %}
    <section aria-labelledby="section-{{ loop.index }}">
      <h2 id="section-{{ loop.index }}">{{ section.title }}</h2>
      {% if section.layout == "table" %}
      <table class="commodity-table">
        <tbody>
        {% for item in section.results %}
          <tr>
            <th scope="row">{{ item.name }}</th>
            <td class="{{ item.direction }}">{{ item.display_value }}</td>
          </tr>
        {% endfor %}
        </tbody>
      </table>
      {% else %}
      <div class="market-grid">
        {% for item in section.results %}
        <article class="market-card">
          <h3>{{ item.name }}</h3>
          <p class="value {{ item.direction }}">{{ item.display_value }}</p>
        </article>
        {% endfor %}
      </div>
      {% endif %}
    </section>
    {% endfor %}

    <aside class="notice">
      <strong>데이터 출처:</strong> FinanceDataReader<br>
      각 항목은 조회 가능한 최근 2개 거래일의 종가 기준으로 계산됩니다.
      <ul>
      {% for item in flat_items %}
        <li>{{ item.name }}({{ item.symbol }}): 기준일 {{ item.data_date or "데이터 없음" }}{% if item.error %} · {{ item.error }}{% endif %}</li>
      {% endfor %}
      </ul>
    </aside>
  </main>
</body>
</html>
"""


@dataclass
class MarketResult:
    name: str
    symbol: str
    value: float | None
    previous_value: float | None
    change: float | None
    change_rate: float | None
    direction: str
    data_date: str | None
    display_value: str
    error: str | None = None


def format_number(value: float, precision: int = 2) -> str:
    return f"{value:,.{precision}f}"


def format_display(value: float, change_rate: float, direction: str, precision: int = 2) -> str:
    icon = {"up": "▲", "down": "▼", "flat": "-"}[direction]
    return f"{format_number(value, precision)} {icon} {abs(change_rate):.2f}%"


def empty_result(item: dict[str, object], message: str) -> MarketResult:
    return MarketResult(
        name=str(item["name"]),
        symbol=str(item["symbol"]),
        value=None,
        previous_value=None,
        change=None,
        change_rate=None,
        direction="flat",
        data_date=None,
        display_value="데이터 없음",
        error=message,
    )


def fetch_item(item: dict[str, object], now: datetime) -> MarketResult:
    end = (now + timedelta(days=1)).date().isoformat()
    start = (now - timedelta(days=LOOKBACK_DAYS)).date().isoformat()
    symbol = str(item["symbol"])
    precision = int(item.get("precision", 2))

    try:
        frame = fdr.DataReader(symbol, start, end)
    except Exception as exc:  # External market data can fail independently per symbol.
        return empty_result(item, f"조회 실패: {exc}")

    if frame is None or frame.empty or "Close" not in frame.columns:
        return empty_result(item, "종가 데이터 없음")

    close = frame["Close"].dropna()
    if len(close) < 2:
        return empty_result(item, "최근 2개 거래일 데이터 부족")

    latest = close.iloc[-1]
    previous = close.iloc[-2]
    if not all(math.isfinite(float(v)) for v in (latest, previous)) or float(previous) == 0:
        return empty_result(item, "유효하지 않은 가격 데이터")

    value = float(latest)
    previous_value = float(previous)
    change = value - previous_value
    change_rate = change / previous_value * 100
    if change > 0:
        direction = "up"
    elif change < 0:
        direction = "down"
    else:
        direction = "flat"

    data_date = close.index[-1].date().isoformat()
    return MarketResult(
        name=str(item["name"]),
        symbol=symbol,
        value=value,
        previous_value=previous_value,
        change=change,
        change_rate=change_rate,
        direction=direction,
        data_date=data_date,
        display_value=format_display(value, change_rate, direction, precision),
    )


def build_report(now: datetime) -> dict[str, object]:
    sections: list[dict[str, object]] = []
    flat_items: list[MarketResult] = []

    for section in SECTIONS:
        results = [fetch_item(item, now) for item in section["items"]]
        flat_items.extend(results)
        sections.append(
            {
                "title": section["title"],
                "layout": section["layout"],
                "results": results,
            }
        )

    return {
        "generated_at": now.strftime("%Y-%m-%d %H:%M:%S"),
        "generated_date": now.strftime("%Y-%m-%d"),
        "sections": sections,
        "flat_items": flat_items,
    }


def write_report(report: dict[str, object]) -> None:
    generated_date = str(report["generated_date"])
    date_path = datetime.strptime(generated_date, "%Y-%m-%d")
    archive_dir = REPORT_ROOT / date_path.strftime("%Y") / date_path.strftime("%m") / date_path.strftime("%d")
    archive_dir.mkdir(parents=True, exist_ok=True)
    REPORT_ROOT.mkdir(exist_ok=True)

    html = Template(HTML_TEMPLATE).render(**report)
    serializable = {
        "generated_at": report["generated_at"],
        "generated_date": report["generated_date"],
        "sections": [
            {
                "title": section["title"],
                "layout": section["layout"],
                "items": [asdict(item) for item in section["results"]],
            }
            for section in report["sections"]
        ],
    }

    (archive_dir / "index.html").write_text(html, encoding="utf-8")
    (archive_dir / "data.json").write_text(
        json.dumps(serializable, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    (REPORT_ROOT / "latest.html").write_text(html, encoding="utf-8")


def main() -> None:
    now = datetime.now(KST)
    report = build_report(now)
    write_report(report)
    print(f"Generated market summary for {report['generated_date']} at {report['generated_at']} KST")


if __name__ == "__main__":
    main()
