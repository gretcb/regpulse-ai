"""
RegPulse AI

Main Gradio application.

This file creates the user interface and will later integrate:

1. News Retrieval
2. LLM Processing
3. Text-to-Speech
4. Final results display
"""

import gradio as gr


# ============================================================
# APPLICATION DATA
# ============================================================
#
# These lists populate the dropdown menus.
# They define the inputs available to the user.
# ============================================================

EU_COUNTRIES = [
    "Austria",
    "Belgium",
    "Bulgaria",
    "Croatia",
    "Cyprus",
    "Czech Republic",
    "Denmark",
    "Estonia",
    "Finland",
    "France",
    "Germany",
    "Greece",
    "Hungary",
    "Ireland",
    "Italy",
    "Latvia",
    "Lithuania",
    "Luxembourg",
    "Malta",
    "Netherlands",
    "Poland",
    "Portugal",
    "Romania",
    "Slovakia",
    "Slovenia",
    "Spain",
    "Sweden",
]

TIMEFRAMES = [
    "Last Week",
    "Last Month",
]


# ============================================================
# MOCK APPLICATION FUNCTION
# ============================================================
#
# For now, this function returns sample data.
#
# Why?
# - It allows us to build and test Gradio independently.
# - We do not need to wait for the other modules.
# - Later, this function will call the real project pipeline.
# ============================================================

def mock_run(
    country: str,
    timeframe: str,
):
    """
    Return simulated outputs for the initial Gradio prototype.

    Args:
        country:
            EU country selected by the user.

        timeframe:
            Time period selected by the user.

    Returns:
        Four outputs:
        - status message;
        - executive summary;
        - business impact;
        - retrieved news.
    """

    # Validate that the user selected both inputs.
    if not country or not timeframe:
        raise gr.Error(
            "Please select both a country and a timeframe."
        )

    # Mocked executive summary.
    summary = f"""
### Executive Summary

This is a sample executive briefing for **{country}**
based on maritime environmental news from **{timeframe.lower()}**.

The final version will summarize real news retrieved by the application.
"""

    # Mocked business impact using Markdown headings and bullet points.
    impact = """
### Affected Stakeholders

- Shipping companies
- Port authorities
- Sustainability teams

### Potential Implications

- Changes in environmental monitoring
- New operational considerations
- Opportunities linked to cleaner port infrastructure
"""

    # Mocked news content.
    retrieved_news = """
ARTICLE 1

Title: Example maritime environmental update  
Source: Example Source  
Published date: 2026-07-15  
URL: https://example.com/article  

Content:  
Example article content used to test the interface.
"""

    # No audio exists yet, so the audio output remains empty.
    audio_path = None

    # Return values in the same order as the Gradio outputs.
    return (
        "Prototype completed successfully.",
        summary,
        impact,
        audio_path,
        retrieved_news,
    )


# ============================================================
# GRADIO INTERFACE
# ============================================================
#
# gr.Blocks allows us to create a more structured and visual layout.
# ============================================================

with gr.Blocks(
    title="RegPulse AI",
    theme=gr.themes.Soft(),
) as demo:

    # Main title and product description.
    gr.Markdown(
        """
# RegPulse AI

### Environmental intelligence for the European shipping industry

Select an EU country and timeframe to generate:

- an executive summary;
- a business impact analysis;
- an AI-generated podcast.
"""
    )

    # Input section.
    with gr.Row():
        country_input = gr.Dropdown(
            choices=EU_COUNTRIES,
            value="Spain",
            label="EU Country",
            info="Select the country used to filter the news search.",
        )

        timeframe_input = gr.Dropdown(
            choices=TIMEFRAMES,
            value="Last Week",
            label="Timeframe",
            info="Select the period used to retrieve recent news.",
        )

    # Main action button.
    generate_button = gr.Button(
        "Generate Executive Brief",
        variant="primary",
    )

    # Status output gives the user feedback after processing.
    status_output = gr.Textbox(
        label="Status",
        value="Ready",
        interactive=False,
    )

    # Results header.
    gr.Markdown("## Executive Brief")

    # Display summary and impact side by side.
    with gr.Row():
        with gr.Column():
            gr.Markdown("### Executive Summary")
            summary_output = gr.Markdown()

        with gr.Column():
            gr.Markdown("### Business Impact")
            impact_output = gr.Markdown()

    # Podcast player.
    gr.Markdown("### Executive Podcast")

    audio_output = gr.Audio(
        label="Generated Podcast",
        type="filepath",
    )

    # Retrieved news is hidden inside an accordion to keep the UI clean.
    with gr.Accordion(
        "Retrieved News and Sources",
        open=False,
    ):
        news_output = gr.Textbox(
            label="Retrieved News",
            lines=14,
            interactive=False,
        )

    # Connect the button to the mocked function.
    generate_button.click(
        fn=mock_run,
        inputs=[
            country_input,
            timeframe_input,
        ],
        outputs=[
            status_output,
            summary_output,
            impact_output,
            audio_output,
            news_output,
        ],
    )


# ============================================================
# APPLICATION START
# ============================================================

if __name__ == "__main__":
    demo.launch()