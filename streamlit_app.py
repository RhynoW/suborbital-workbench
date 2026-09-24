# -*- coding: utf-8 -*-
"""次軌道載具設計工作單 —— Streamlit 部署外殼。

## 這個檔案做什麼、不做什麼

工作單本體是一個**自給自足的單檔 HTML**(`web/suborbital_workbench.html`),
所有計算與繪圖都在瀏覽器端的 JavaScript 完成。

本檔只是把它包進 Streamlit,讓它能部署到 Streamlit Community Cloud
取得一個公開網址。**它不是原生 Streamlit app** ——
沒有把滑桿改成 `st.slider`,也沒有把圖改成 Plotly。

這是刻意的選擇,理由:

1. **單一來源。** 同一份 HTML 同時作為獨立檔案與 Streamlit app 的內容,
   公式不會有兩套。改寫成原生 Streamlit 會讓兩邊的物理各自演化,
   最後不知道該信哪個 —— 這個專案已經在「一邊用地球平均半徑、
   一邊用赤道半徑」上踩過一次,兩邊算出不同答案比兩邊都錯更糟。
2. **版面。** 工作單的教學效果依賴推導鏈的排版、狀態標籤與三張圖的配置。
3. **零伺服器計算。** 運算都在瀏覽器,伺服器只送靜態檔,
   免費額度不會被計算吃掉。

Streamlit 在這裡提供的實質價值是:公開網址、原始檔下載、以及文件入口。

## 本機執行

    pip install -r requirements.txt
    streamlit run streamlit_app.py

## 部署

Streamlit Community Cloud → New app:

    Repository      <本 repo>
    Branch          main
    Main file path  streamlit_app.py

相依由根目錄的 `requirements.txt` 自動讀取,不需要在 Advanced settings
另行指定。
"""
import pathlib

import streamlit as st

HERE = pathlib.Path(__file__).resolve().parent
PAGE = HERE / "web" / "suborbital_workbench.html"
DOC = HERE / "web" / "設計與計算原理.md"

st.set_page_config(
    page_title="次軌道載具設計工作單",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed",
)


def wrap(body: str) -> str:
    """補上 HTML 骨架。

    工作單原本發佈在會自動包 skeleton 的平台上,所以檔案本身沒有
    `<!doctype>` / `<html>` / `<head>` / `<body>`。這裡補上等效的最小骨架:
    字元編碼、viewport(含 `viewport-fit=cover` 讓手機安全區生效),
    以及原平台提供的那一小段 reset。

    頁面自己的 CSS 會設定 body 背景與深淺主題,所以這裡只給最低限度,
    不覆蓋它的 token。
    """
    return f"""<!doctype html>
<html lang="zh-Hant">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<style>
  :root {{
    color-scheme: light;
    padding-top: env(safe-area-inset-top, 0px);
    padding-bottom: env(safe-area-inset-bottom, 0px);
  }}
  html, body {{ margin: 0; }}
  body {{ font: 14px system-ui, -apple-system, "Segoe UI", sans-serif; }}
  img {{ max-width: 100%; }}
  [hidden] {{ display: none !important; }}
</style>
</head>
<body>
{body}
</body>
</html>"""


if not PAGE.is_file():
    st.error(
        f"找不到工作單檔案:`web/{PAGE.name}`\n\n"
        "請確認 repo 完整 clone,且該檔未被 .gitignore 排除。"
    )
    st.stop()

html = PAGE.read_text(encoding="utf-8")

with st.sidebar:
    st.markdown("### 次軌道載具設計工作單")
    st.caption(
        "互動式教學工作單。移動設計變數,看射程、Δv、質量比與分離時刻"
        "如何一起改變,以及模擬工具的能力邊界在哪裡。"
    )
    st.divider()

    st.markdown("**這些不是設計值**")
    st.caption(
        "全部是一階概念設計層級的解析式,用於建立量級直覺與因子耦合關係。"
        "真實設計需要上升段軌跡最佳化、六自由度再入積分、"
        "氣動係數資料庫與結構熱分析。"
    )
    st.divider()

    st.download_button(
        "下載工作單 HTML",
        data=html.encode("utf-8"),
        file_name="suborbital_workbench.html",
        mime="text/html",
        help="單檔、可離線開啟(離線時字型退回系統預設)",
        use_container_width=True,
    )
    if DOC.is_file():
        st.download_button(
            "下載設計與計算原理",
            data=DOC.read_text(encoding="utf-8").encode("utf-8"),
            file_name="設計與計算原理.md",
            mime="text/markdown",
            help="每一條公式的假設、適用範圍與失準處",
            use_container_width=True,
        )
    st.divider()
    st.caption(
        "頁面高度若不合適,可拉動下方捲軸;"
        "或下載 HTML 在瀏覽器直接開啟,版面會更舒適。"
    )

# Streamlit 的 components 必須給定高度,無法隨內容自動伸縮,
# 因此取一個夠大的值並開啟 iframe 自身捲動。
st.components.v1.html(wrap(html), height=1400, scrolling=True)
