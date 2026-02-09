import gradio as gr
import asyncio
import os
from dotenv import load_dotenv
from google.genai import types

try:
    from marketing_agent.agent import marketing_runner
    print("Marketing Runner erfolgreich geladen.")
except Exception as e:
    print(f"Fehler beim Laden des Runners: {e}")

load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")

# Globaler Zustand für die aktuelle Session
_current_session_id = None


async def run_pipeline_async(product, audience, refinement=""):
    global _current_session_id

    if not API_KEY:
        return "Fehler: Kein GOOGLE_API_KEY in der .env Datei gefunden.", "", ""

    if not product.strip():
        return "Bitte gib eine Produktbeschreibung ein.", "", ""

    try:
        session = await marketing_runner.session_service.create_session(
            user_id="student_lea",
            app_name="marketing_factory"
        )
        _current_session_id = session.id
    except Exception:
        _current_session_id = f"session_{hash(product) % 10000}"

    # Eingabe zusammenbauen
    if refinement.strip():
        user_input = (
            f"Produkt: {product}. Zielgruppe: {audience}.\n\n"
            f"Bitte berücksichtige folgendes Feedback zur Verfeinerung: {refinement}"
        )
    else:
        user_input = f"Produkt: {product}. Zielgruppe: {audience}."

    user_content = types.Content(
        role="user",
        parts=[types.Part(text=user_input)]
    )

    results = {}
    async for event in marketing_runner.run_async(
        user_id="student_lea",
        session_id=_current_session_id,
        new_message=user_content
    ):
        if event.actions and event.actions.state_delta:
            delta = event.actions.state_delta
            if "strategy" in delta:
                results["strategy"] = delta["strategy"]
            if "ad_copy" in delta:
                results["ad_copy"] = delta["ad_copy"]
            if "social_posts" in delta:
                results["social_posts"] = delta["social_posts"]

    return (
        results.get("strategy", "Fehler: Strategie konnte nicht generiert werden."),
        results.get("ad_copy", "Fehler: Werbetext konnte nicht generiert werden."),
        results.get("social_posts", "Fehler: Social-Media-Posts konnten nicht generiert werden.")
    )


def generate(product, audience):
    """Erstmalige Generierung der Marketing-Kampagne."""
    if not product.strip():
        gr.Warning("Bitte gib eine Produktbeschreibung ein.")
        return "", "", ""
    return asyncio.run(run_pipeline_async(product, audience))


def refine(product, audience, refinement, current_strategy, current_copy, current_social):
    """Verfeinert die bestehenden Ergebnisse basierend auf Nutzer-Feedback."""
    if not refinement.strip():
        gr.Warning("Bitte gib Feedback zur Verfeinerung ein.")
        return current_strategy, current_copy, current_social
    return asyncio.run(run_pipeline_async(product, audience, refinement))


# --- Gradio UI ---
with gr.Blocks(title="Marketing Agent Factory", theme=gr.themes.Soft()) as demo:
    gr.Markdown("# AI Marketing Agent Factory")
    gr.Markdown("Generiere eine komplette Marketing-Kampagne mit KI – von der Strategie bis zum Social-Media-Post.")

    with gr.Row():
        with gr.Column(scale=1):
            product_input = gr.Textbox(
                label="Produktbeschreibung",
                placeholder="z.B. Nachhaltige Trinkflasche aus Edelstahl mit integriertem Temperaturanzeiger",
                lines=3
            )
            audience_input = gr.Textbox(
                label="Zielgruppe",
                placeholder="z.B. Umweltbewusste Berufstätige zwischen 25-40 Jahren",
                lines=2
            )
            generate_btn = gr.Button("Kampagne generieren", variant="primary")

    # Ergebnis-Tabs
    with gr.Tabs():
        with gr.Tab("1. Strategie"):
            strategy_out = gr.Markdown(value="*Warte auf Eingabe...*")
        with gr.Tab("2. Werbetext"):
            copy_out = gr.Markdown(value="*Warte auf Eingabe...*")
        with gr.Tab("3. Social Media"):
            social_out = gr.Markdown(value="*Warte auf Eingabe...*")

    # Verfeinerungs-Bereich
    gr.Markdown("---")
    gr.Markdown("### Ergebnisse verfeinern")
    gr.Markdown("Du bist nicht zufrieden? Gib Feedback und lass die KI die Ergebnisse anpassen.")
    with gr.Row():
        refinement_input = gr.Textbox(
            label="Feedback zur Verfeinerung",
            placeholder="z.B. Der Ton soll lockerer sein, mehr Emojis verwenden, Fokus auf Nachhaltigkeit stärken",
            lines=2,
            scale=3
        )
        refine_btn = gr.Button("Verfeinern", variant="secondary", scale=1)

    # Events
    generate_btn.click(
        fn=generate,
        inputs=[product_input, audience_input],
        outputs=[strategy_out, copy_out, social_out]
    )
    refine_btn.click(
        fn=refine,
        inputs=[product_input, audience_input, refinement_input,
                strategy_out, copy_out, social_out],
        outputs=[strategy_out, copy_out, social_out]
    )

if __name__ == "__main__":
    demo.launch()
