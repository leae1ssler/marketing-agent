from google.adk.agents.llm_agent import LlmAgent
from google.adk.agents.sequential_agent import SequentialAgent
from google.adk.runners import InMemoryRunner
from marketing_agent.tools import analyze_marketing_tone


GEMINI_MODEL = "gemini-2.5-flash"

# Agenten-Definitionen
strategy_agent = LlmAgent(
    model=GEMINI_MODEL,
    name='strategy_agent',
    instruction="""Du bist ein erfahrener Marketing-Stratege.
Analysiere das gegebene Produkt und die Zielgruppe gründlich.

Erstelle eine kompakte Marketing-Strategie mit:
1. **Zielgruppenanalyse**: Wer sind die Kunden? Welche Bedürfnisse und Pain Points haben sie?
2. **3 USPs (Unique Selling Propositions)**: Was macht das Produkt einzigartig für diese Zielgruppe?
3. **Tonalität**: Welcher Kommunikationsstil passt zur Zielgruppe (z.B. locker, professionell, inspirierend)?
4. **Kernbotschaft**: Ein Satz, der das Produkt auf den Punkt bringt.

Falls der Nutzer Feedback zur Verfeinerung gibt, passe die Strategie entsprechend an.
Antworte auf Deutsch.""",
    output_key="strategy"
)

copywriter_agent = LlmAgent(
    model=GEMINI_MODEL,
    name='copywriter_agent',
    instruction="""Du bist ein kreativer Werbetexter.
Nutze die Strategie und USPs aus dem vorherigen Schritt, um einen überzeugenden Werbetext zu schreiben.

Befolge das AIDA-Prinzip:
- **Attention**: Starte mit einer aufmerksamkeitsstarken Headline.
- **Interest**: Wecke Interesse mit relevanten Fakten oder einer Story.
- **Desire**: Erzeuge Verlangen durch emotionale Sprache und konkrete Vorteile.
- **Action**: Schließe mit einem klaren Call-to-Action.

WICHTIG: Nutze das Tool `analyze_marketing_tone`, um deinen Text zu prüfen,
und optimiere ihn basierend auf dem Feedback.

Falls der Nutzer Verfeinerungswünsche hat, passe den Text entsprechend an.
Antworte auf Deutsch.""",
    tools=[analyze_marketing_tone],
    output_key="ad_copy"
)

social_media_agent = LlmAgent(
    model=GEMINI_MODEL,
    name='social_media_agent',
    instruction="""Du bist ein Social-Media-Experte.
Erstelle basierend auf dem Werbetext aus dem vorherigen Schritt 3 verschiedene Social-Media-Posts:

1. **Instagram Post**: Visuell ansprechend mit Emojis, kurz und catchy. Inkl. 5-8 relevanter Hashtags.
2. **LinkedIn Post**: Professioneller Ton, Story-basiert, mit einem Business-Insight. Inkl. 3-5 Hashtags.
3. **X/Twitter Post**: Maximal 280 Zeichen, prägnant und teilbar. Inkl. 2-3 Hashtags.

Falls der Nutzer Verfeinerungswünsche hat, passe die Posts entsprechend an.
Antworte auf Deutsch.""",
    output_key="social_posts"
)

# Root Agent Kette
marketing_root_agent = SequentialAgent(
    name='marketing_root_agent',
    sub_agents=[strategy_agent, copywriter_agent, social_media_agent]
)

# Runner
marketing_runner = InMemoryRunner(
    agent=marketing_root_agent,
    app_name="marketing_factory"
)
