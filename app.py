"""
RegPulse AI

Main Gradio application.

This file integrates:
1. News Retrieval
2. LLM Processing
3. Text-to-Speech
4. Executive results display
"""

import html
import re
from collections import Counter
from datetime import datetime

import gradio as gr

from src.news_fetcher import get_news
from src.llm_processor import process_news
from src.tts_generator import generate_audio


# ============================================================
# APPLICATION DATA
# ============================================================

COUNTRY_OPTIONS = [
    "🇦🇹 Austria",
    "🇧🇪 Belgium",
    "🇧🇬 Bulgaria",
    "🇭🇷 Croatia",
    "🇨🇾 Cyprus",
    "🇨🇿 Czech Republic",
    "🇩🇰 Denmark",
    "🇪🇪 Estonia",
    "🇫🇮 Finland",
    "🇫🇷 France",
    "🇩🇪 Germany",
    "🇬🇷 Greece",
    "🇭🇺 Hungary",
    "🇮🇪 Ireland",
    "🇮🇹 Italy",
    "🇱🇻 Latvia",
    "🇱🇹 Lithuania",
    "🇱🇺 Luxembourg",
    "🇲🇹 Malta",
    "🇳🇱 Netherlands",
    "🇵🇱 Poland",
    "🇵🇹 Portugal",
    "🇷🇴 Romania",
    "🇸🇰 Slovakia",
    "🇸🇮 Slovenia",
    "🇪🇸 Spain",
    "🇸🇪 Sweden",
]

TIMEFRAMES = [
    "Last Week",
    "Last Month",
]


# ============================================================
# APPLICATION STYLES
# ============================================================

APP_CSS = """
:root {
    --navy-950: #071b31;
    --navy-900: #0a2748;
    --navy-800: #0c3f70;
    --blue-600: #1766b0;
    --blue-500: #2477c8;
    --ink-900: #10233f;
    --ink-700: #40556f;
    --ink-500: #71839a;
    --line: #dbe5ef;
    --canvas: #f4f7fb;
    --success: #1d9b67;
    --success-bg: #eefaf5;
}

.gradio-container {
    max-width: 1440px !important;
    margin: 0 auto !important;
    padding: 0 24px 22px !important;
    background: var(--canvas) !important;
    color: var(--ink-900) !important;
}

/* ---------- Header ---------- */
.regpulse-header {
    position: relative;
    overflow: hidden;
    margin: 0 -24px 22px;
    padding: 30px 42px 28px;
    color: #ffffff;
    border-radius: 0 0 22px 22px;
    background:
        radial-gradient(circle at 88% 18%, rgba(74, 151, 216, 0.30), transparent 27%),
        linear-gradient(120deg, var(--navy-950), var(--navy-800));
    box-shadow: 0 16px 34px rgba(9, 36, 65, 0.20);
}

.regpulse-header::after {
    content: "";
    position: absolute;
    left: 0;
    right: 0;
    bottom: 0;
    height: 2px;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.42), transparent);
}

.header-main {
    position: relative;
    z-index: 2;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 28px;
}

.regpulse-brand {
    display: flex;
    align-items: center;
    gap: 16px;
    min-width: 330px;
}

.regpulse-icon {
    width: 58px;
    height: 58px;
    border: 1px solid rgba(255, 255, 255, 0.46);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 29px;
    background: rgba(255, 255, 255, 0.09);
    box-shadow: inset 0 0 18px rgba(255,255,255,0.05);
}

.regpulse-title {
    margin: 0 !important;
    color: #ffffff !important;
    font-size: 34px !important;
    line-height: 1.05 !important;
    font-weight: 780 !important;
    letter-spacing: -0.6px;
}

.regpulse-subtitle {
    margin: 8px 0 0;
    color: #d9e8f7 !important;
    font-size: 15px;
}

.header-benefits {
    display: grid;
    grid-template-columns: repeat(3, minmax(150px, 1fr));
    gap: 10px;
    max-width: 690px;
}

.header-benefit {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 10px 12px;
    border-left: 1px solid rgba(255,255,255,0.18);
}

.header-benefit-icon {
    width: 34px;
    height: 34px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 50%;
    background: rgba(255,255,255,0.08);
    font-size: 17px;
}

.header-benefit strong {
    display: block;
    color: #ffffff;
    font-size: 13px;
}

.header-benefit span {
    display: block;
    margin-top: 2px;
    color: #c7d8ea;
    font-size: 11px;
    line-height: 1.25;
}

.header-ship {
    position: absolute;
    right: 18px;
    bottom: -15px;
    z-index: 1;
    font-size: 116px;
    opacity: 0.12;
    transform: rotate(-2deg);
    filter: saturate(0.7);
    pointer-events: none;
}

/* ---------- Cards ---------- */
.dashboard-card {
    background: #ffffff !important;
    border: 1px solid var(--line) !important;
    border-radius: 16px !important;
    box-shadow: 0 9px 26px rgba(15, 42, 70, 0.07) !important;
    padding: 20px !important;
}

.control-panel {
    margin-bottom: 16px !important;
}

.control-kicker {
    margin: 0 0 15px;
    color: var(--navy-900);
    font-size: 14px;
    font-weight: 760;
    letter-spacing: 0.02em;
}

.primary-action button {
    min-height: 50px !important;
    border-radius: 10px !important;
    border: none !important;
    background: linear-gradient(135deg, #0b3d70, #0a5a9d) !important;
    color: #ffffff !important;
    font-weight: 760 !important;
    box-shadow: 0 7px 16px rgba(7, 76, 135, 0.24) !important;
    transition: transform 0.16s ease, filter 0.16s ease;
}

.primary-action button:hover {
    transform: translateY(-1px);
    filter: brightness(1.05);
}

.ai-note {
    margin-top: 6px;
    text-align: center;
    color: var(--ink-500);
    font-size: 12px;
}

.result-card {
    min-height: 300px;
}

.media-card {
    min-height: 290px;
}

.section-title {
    display: flex;
    align-items: center;
    gap: 9px;
    margin: 0 0 14px;
    color: var(--navy-900);
    font-size: 18px;
    font-weight: 760;
}

.section-icon {
    width: 34px;
    height: 34px;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    border-radius: 50%;
    background: #edf4fb;
    color: var(--blue-600);
}

.card-subtitle {
    margin: -8px 0 12px;
    color: var(--ink-500);
    font-size: 12px;
}

/* ---------- Status ---------- */
.status-shell {
    margin-bottom: 17px;
}

.status-bar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 18px;
    min-height: 56px;
    padding: 12px 18px;
    border: 1px solid #ccebdc;
    border-left: 5px solid var(--success);
    border-radius: 13px;
    background: var(--success-bg);
    color: #176946;
    box-shadow: 0 6px 18px rgba(29,155,103,0.07);
}

.status-main {
    display: flex;
    align-items: center;
    gap: 11px;
}

.status-dot {
    width: 26px;
    height: 26px;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    border-radius: 50%;
    background: var(--success);
    color: white;
    font-size: 13px;
}

.status-label {
    margin-right: 8px;
    font-size: 12px;
    font-weight: 800;
    letter-spacing: 0.05em;
}

.status-message {
    color: #2b7658;
    font-size: 14px;
}

.status-time {
    white-space: nowrap;
    color: #529077;
    font-size: 12px;
}

.status-bar.processing {
    border-color: #cfe0f3;
    border-left-color: var(--blue-500);
    background: #f1f7fd;
    color: #174f82;
}

.status-bar.processing .status-dot {
    background: var(--blue-500);
    animation: pulse 1.35s ease-in-out infinite;
}

@keyframes pulse {
    0%, 100% { transform: scale(1); opacity: 1; }
    50% { transform: scale(1.10); opacity: 0.72; }
}

/* ---------- Source overview ---------- */
.source-overview {
    padding: 5px 2px 0;
}

.source-row {
    display: grid;
    grid-template-columns: minmax(110px, 1fr) minmax(120px, 2fr) 24px;
    align-items: center;
    gap: 10px;
    margin: 11px 0;
}

.source-name {
    overflow: hidden;
    color: var(--ink-700);
    font-size: 12px;
    text-overflow: ellipsis;
    white-space: nowrap;
}

.source-track {
    height: 10px;
    overflow: hidden;
    border-radius: 999px;
    background: #e8eef5;
}

.source-fill {
    height: 100%;
    border-radius: 999px;
    background: linear-gradient(90deg, var(--navy-800), var(--blue-500));
}

.source-count {
    color: var(--navy-900);
    font-size: 12px;
    font-weight: 760;
    text-align: right;
}

.source-note {
    margin-top: 14px;
    padding: 10px 12px;
    border-radius: 10px;
    background: #f5f8fc;
    color: var(--ink-500);
    font-size: 11px;
    line-height: 1.4;
}

.single-source-summary {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 14px;
    padding: 14px;
    border: 1px solid #e2eaf2;
    border-radius: 12px;
    background: #f8fafc;
}

.single-source-summary strong {
    color: var(--navy-900);
}

.single-source-summary span {
    color: var(--ink-500);
    font-size: 12px;
}

/* ---------- Source traceability ---------- */
.sources-count {
    margin: 14px 0 8px;
    color: var(--ink-700);
    font-size: 13px;
    font-weight: 680;
}

.sources-accordion {
    background: #ffffff !important;
    border: 1px solid var(--line) !important;
    border-radius: 13px !important;
}

.regpulse-footer {
    text-align: center;
    color: var(--ink-500);
    font-size: 12px;
    padding: 20px 0 4px;
}

.gradio-container label {
    color: var(--navy-900) !important;
    font-weight: 680 !important;
}

@media (max-width: 1000px) {
    .header-benefits {
        display: none;
    }

    .header-main {
        justify-content: flex-start;
    }
}

@media (max-width: 800px) {
    .gradio-container {
        padding: 0 12px 18px !important;
    }

    .regpulse-header {
        margin: 0 -12px 18px;
        padding: 24px 20px 22px;
    }

    .regpulse-title {
        font-size: 28px !important;
    }

    .dashboard-card {
        padding: 15px !important;
    }

    .status-bar {
        align-items: flex-start;
        flex-direction: column;
        gap: 6px;
    }

    .status-time {
        padding-left: 37px;
    }
}
"""


# ============================================================
# UI HELPERS
# ============================================================

def clean_country_label(country_option: str) -> str:
    """Remove the flag emoji from the dropdown value."""

    if not country_option:
        return ""

    parts = country_option.split(" ", 1)
    return parts[1] if len(parts) == 2 else country_option


def current_timestamp() -> str:
    """Return a compact local timestamp for the status bar."""

    return datetime.now().strftime("%d %b %Y · %H:%M")


def build_status_html(
    message: str,
    *,
    processing: bool = False,
) -> str:
    """Build a professional status bar."""

    css_class = "status-bar processing" if processing else "status-bar"
    icon = "⏳" if processing else "✓"

    return f"""
<div class="status-shell">
    <div class="{css_class}">
        <div class="status-main">
            <span class="status-dot">{icon}</span>
            <span class="status-label">STATUS</span>
            <span class="status-message">{html.escape(message)}</span>
        </div>
        <div class="status-time">◷ {current_timestamp()}</div>
    </div>
</div>
"""


def extract_sources(news_text: str) -> list[str]:
    """Extract selected article source names from formatted news text."""

    return [
        source.strip()
        for source in re.findall(
            r"^Source:\s*(.+)$",
            news_text,
            flags=re.MULTILINE,
        )
    ]


def build_source_overview(news_text: str) -> str:
    """Build a compact HTML source-distribution overview."""

    sources = extract_sources(news_text)

    if not sources:
        return """
<div class="source-overview">
    <div class="source-note">No source distribution is available.</div>
</div>
"""

    counts = Counter(sources)
    maximum = max(counts.values())

    if len(counts) == 1:
        source_name, article_count = next(iter(counts.items()))
        article_label = "article" if article_count == 1 else "articles"

        return f"""
<div class="source-overview">
    <div class="single-source-summary">
        <div>
            <strong>{html.escape(source_name)}</strong><br>
            <span>Primary source represented in this brief</span>
        </div>
        <div><strong>{article_count}</strong> <span>{article_label}</span></div>
    </div>
    <div class="source-note">
        Shows the number of selected articles by source. It is not a credibility or risk score.
    </div>
</div>
"""

    rows = []

    for source_name, article_count in counts.most_common():
        width = max(8, int((article_count / maximum) * 100))
        rows.append(
            f"""
<div class="source-row">
    <div class="source-name" title="{html.escape(source_name)}">{html.escape(source_name)}</div>
    <div class="source-track"><div class="source-fill" style="width:{width}%"></div></div>
    <div class="source-count">{article_count}</div>
</div>
"""
        )

    return (
        '<div class="source-overview">'
        + "".join(rows)
        + """
<div class="source-note">
    Shows the number of selected articles by source. It is not a credibility or risk score.
</div>
</div>
"""
    )


def build_sources_count(news_text: str) -> str:
    """Return a dynamic count displayed above the source accordion."""

    article_count = len(
        re.findall(
            r"^ARTICLE\s+\d+",
            news_text,
            flags=re.MULTILINE,
        )
    )

    noun = "article" if article_count == 1 else "articles"

    return (
        f'<div class="sources-count">📄 {article_count} {noun} retrieved · '
        "Expand below to review source traceability</div>"
    )


# ============================================================
# COMPLETE APPLICATION PIPELINE
# ============================================================

def run_pipeline(
    country_option: str,
    timeframe: str,
):
    """Run the complete RegPulse AI workflow with live status updates."""

    country = clean_country_label(country_option)

    if not country or not timeframe:
        raise gr.Error(
            "Please select both a country and a timeframe."
        )

    empty_values = (
        "",
        "",
        None,
        "",
        "",
        "",
    )

    try:
        yield (
            build_status_html(
                "Retrieving maritime regulatory news...",
                processing=True,
            ),
            *empty_values,
        )

        news_text = get_news(
            country=country,
            timeframe=timeframe,
        )

        if not news_text:
            raise ValueError(
                "No relevant regulatory maritime news was found. "
                "Try selecting 'Last Month' or another EU country."
            )

        yield (
            build_status_html(
                "Analyzing selected sources with AI...",
                processing=True,
            ),
            *empty_values,
        )

        analysis = process_news(
            news_text=news_text,
            country=country,
            timeframe=timeframe,
        )

        yield (
            build_status_html(
                "Generating the executive podcast...",
                processing=True,
            ),
            *empty_values,
        )

        clean_script = (
            analysis["podcast_script"]
            .replace("*", "")
            .replace("#", "")
            .strip()
        )

        audio_path = generate_audio(clean_script)

        if not audio_path:
            raise ValueError(
                "The executive podcast could not be generated."
            )

        source_overview = build_source_overview(news_text)
        sources_count = build_sources_count(news_text)

        yield (
            build_status_html(
                "Executive brief ready.",
                processing=False,
            ),
            analysis["summary"],
            analysis["impact"],
            audio_path,
            source_overview,
            sources_count,
            news_text,
        )

    except Exception as error:
        raise gr.Error(str(error)) from error


# ============================================================
# GRADIO INTERFACE
# ============================================================

with gr.Blocks(
    title="RegPulse AI",
    css=APP_CSS,
) as demo:

    gr.HTML(
        """
<div class="regpulse-header">
    <div class="header-main">
        <div class="regpulse-brand">
            <div class="regpulse-icon">⚓</div>
            <div>
                <h1 class="regpulse-title">RegPulse AI</h1>
                <p class="regpulse-subtitle">
                    Environmental intelligence for the European shipping industry
                </p>
            </div>
        </div>

        <div class="header-benefits">
            <div class="header-benefit">
                <div class="header-benefit-icon">📄</div>
                <div><strong>Executive Summary</strong><span>Key regulatory insights</span></div>
            </div>
            <div class="header-benefit">
                <div class="header-benefit-icon">📊</div>
                <div><strong>Business Impact</strong><span>Risks, opportunities and actions</span></div>
            </div>
            <div class="header-benefit">
                <div class="header-benefit-icon">🎧</div>
                <div><strong>AI Podcast</strong><span>Listen to your briefing</span></div>
            </div>
        </div>
    </div>

    <div class="header-ship">🚢</div>
</div>
"""
    )

    with gr.Group(
        elem_classes=["dashboard-card", "control-panel"]
    ):
        gr.HTML('<div class="control-kicker">SEARCH PARAMETERS</div>')

        with gr.Row(equal_height=True):
            country_input = gr.Dropdown(
                choices=COUNTRY_OPTIONS,
                value="🇪🇸 Spain",
                label="EU Country",
                info="Select the market used to guide the news search.",
                scale=3,
            )

            timeframe_input = gr.Dropdown(
                choices=TIMEFRAMES,
                value="Last Month",
                label="Timeframe",
                info="Select the recent period to analyze.",
                scale=3,
            )

            with gr.Column(scale=2):
                generate_button = gr.Button(
                    "✨ Generate Executive Brief",
                    variant="primary",
                    elem_classes=["primary-action"],
                )
                gr.HTML(
                    '<div class="ai-note">◈ Analysis powered by AI</div>'
                )

    status_output = gr.HTML(
        value=build_status_html(
            "Ready to generate an executive brief.",
            processing=True,
        )
    )

    with gr.Row(equal_height=True):
        with gr.Column(
            elem_classes=["dashboard-card", "result-card"]
        ):
            gr.HTML(
                '<div class="section-title"><span class="section-icon">📄</span>'
                "Executive Summary</div>"
            )
            summary_output = gr.Markdown()

        with gr.Column(
            elem_classes=["dashboard-card", "result-card"]
        ):
            gr.HTML(
                '<div class="section-title"><span class="section-icon">📊</span>'
                "Business Impact</div>"
            )
            impact_output = gr.Markdown()

    with gr.Row(equal_height=True):
        with gr.Column(
            elem_classes=["dashboard-card", "media-card"]
        ):
            gr.HTML(
                '<div class="section-title"><span class="section-icon">🎧</span>'
                "Executive Podcast</div>"
            )
            gr.HTML(
                '<div class="card-subtitle">AI-generated audio briefing</div>'
            )
            audio_output = gr.Audio(
                label="Listen to briefing",
                type="filepath",
            )

        with gr.Column(
            elem_classes=["dashboard-card", "media-card"]
        ):
            gr.HTML(
                '<div class="section-title"><span class="section-icon">📈</span>'
                "Sources Represented</div>"
            )
            gr.HTML(
                '<div class="card-subtitle">Distribution of selected articles by source</div>'
            )
            source_overview_output = gr.HTML()

        with gr.Column(
            elem_classes=["dashboard-card", "media-card"]
        ):
            gr.HTML(
                '<div class="section-title"><span class="section-icon">🔎</span>'
                "Retrieved News and Sources</div>"
            )
            gr.HTML(
                '<div class="card-subtitle">Review the source material used for this brief</div>'
            )
            sources_count_output = gr.HTML(
                value='<div class="sources-count">📄 No articles retrieved yet</div>'
            )

            with gr.Accordion(
                "Open source traceability",
                open=False,
                elem_classes=["sources-accordion"],
            ):
                news_output = gr.Textbox(
                    label="Selected source material",
                    lines=12,
                    interactive=False,
                )

    gr.HTML(
        """
<div class="regpulse-footer">
    ⚓ RegPulse AI &nbsp;·&nbsp; Built with Gradio &nbsp;·&nbsp; AI-powered intelligence
</div>
"""
    )

    generate_button.click(
        fn=run_pipeline,
        inputs=[
            country_input,
            timeframe_input,
        ],
        outputs=[
            status_output,
            summary_output,
            impact_output,
            audio_output,
            source_overview_output,
            sources_count_output,
            news_output,
        ],
    )


# ============================================================
# APPLICATION START
# ============================================================

if __name__ == "__main__":
    demo.launch(
    theme=gr.themes.Soft(
        primary_hue="blue",
    ),
    share=True,
    )