# Marketing Agent – Social Media Content Factory

## Projektbeschreibung & Ziele

Dieses Projekt implementiert eine KI-Agenten-Anwendung mit dem **Google Agent Development Kit (ADK)**, die speziell für Marketingzwecke entwickelt wurde. Ziel ist es, den gesamten Marketing-Workflow, von der Strategieentwicklung über das Copywriting bis hin zu fertigen Social-Media-Posts, mithilfe einer Pipeline aus spezialisierten KI-Agenten zu automatisieren.

Die Anwendung richtet sich an Marketer, Content Creator und Studierende, die schnell und effizient Marketingmaterial generieren möchten, ohne dabei auf strategische Qualität zu verzichten.

## Installation und Ausführung

### Voraussetzungen
- Python 3.12 oder höher
- Ein Google API Key (Gemini API)

### Schritte

1. **Repository klonen:**
   ```bash
   git clone https://github.com/leae1ssler/marketing-agent.git
   cd marketing-agent
   ```

2. **Abhängigkeiten installieren:**
   ```bash
   pip install -r requirements.txt
   ```

3. **API-Key konfigurieren:**
   Erstelle eine `.env`-Datei im Projektverzeichnis:
   ```
   GOOGLE_API_KEY=dein_google_api_key
   ```

4. **Anwendung starten:**
   ```bash
   python3.12 app.py
   ```
   Die Gradio-Oberfläche öffnet sich unter `http://localhost:7860`.

## Agenten-Architektur

Die Anwendung nutzt das **SequentialAgent-Pattern** von Google ADK. Drei spezialisierte Agenten arbeiten in einer Pipeline zusammen, wobei jeder Agent auf die Ergebnisse des vorherigen aufbaut:

```
Nutzereingabe → [Strategy Agent] → [Copywriter Agent] → [Social Media Agent] → Ergebnis
                                         ↓
                               analyze_marketing_tone (Tool)
```

### 1. Strategy Agent
- **Aufgabe:** Analysiert das Produkt und die Zielgruppe
- **Output:** Zielgruppenanalyse, 3 USPs, Tonalität-Empfehlung und Kernbotschaft
- **Warum:** Bildet die strategische Grundlage für alle weiteren Inhalte

### 2. Copywriter Agent
- **Aufgabe:** Erstellt einen überzeugenden Werbetext nach dem AIDA-Prinzip (Attention, Interest, Desire, Action)
- **Tool:** Nutzt `analyze_marketing_tone` zur automatischen Qualitätsprüfung des Textes (Länge, Call-to-Action, emotionale Sprache)
- **Warum:** Verbindet kreatives Schreiben mit datenbasierter Qualitätssicherung

### 3. Social Media Agent
- **Aufgabe:** Transformiert den Werbetext in plattformspezifische Posts
- **Output:** Je ein Post für Instagram (visuell/Emojis), LinkedIn (professionell) und X/Twitter (280 Zeichen)
- **Warum:** Unterschiedliche Plattformen erfordern unterschiedliche Formate und Tonalitäten

### Kommunikation zwischen Agenten
Die Agenten teilen Daten über den **State** des Google ADK. Jeder Agent schreibt sein Ergebnis in einen `output_key` (z.B. `strategy`, `ad_copy`, `social_posts`), der für den nächsten Agenten im State verfügbar ist. Der `InMemoryRunner` verwaltet Sessions und orchestriert die Ausführung.

## Funktionen der Applikation

Die **Gradio-Benutzeroberfläche** bietet folgende Features:

- **Eingabe:** Textfelder für Produktbeschreibung und Zielgruppe mit Platzhalter-Beispielen
- **Generierung:** Ein Klick startet die gesamte Pipeline und generiert Strategie, Werbetext und Social-Media-Posts
- **Tab-Ansicht:** Ergebnisse werden übersichtlich in drei Tabs dargestellt (Strategie, Werbetext, Social Media)
- **Verfeinerung:** Ein separater Bereich erlaubt es, Feedback einzugeben (z.B. "lockerer Ton", "mehr Fokus auf Preis") und die Ergebnisse iterativ zu verbessern
- **Fehlerbehandlung:** Validierung der Eingaben, Fehlermeldungen bei fehlendem API-Key oder leeren Feldern, und Abfangen von API-Fehlern mit nutzerfreundlichem Feedback

## Reflexion über Herausforderungen und Lerneffekte

### Herausforderungen

**Qualitätssicherung der Texte:** Eine besondere technische Herausforderung war die Qualitätssicherung der Texte. Dafür haben wir ein Custom Tool entwickelt, die Funktion analyze_marketing_tone. Sie prüft automatisch, ob der Werbetext einen Call-to-Action enthält, ob emotionale Power-Wörter verwendet werden und ob die Textlänge angemessen ist. Der Copywriter-Agent nutzt dieses Tool aktiv und optimiert seinen Text basierend auf dem Feedback.

**Konsistenter Tonfall über mehrere Agenten:** Außerdem war es eine Herausforderung, sicherzustellen, dass alle drei Agenten einen konsistenten Tonfall und eine einheitliche Markenstimme beibehalten. Da jeder Agent unabhängig generiert, konnte es vorkommen, dass die Strategie einen professionellen Ton vorgab, der Social-Media-Agent aber zu informell wurde. Die Lösung war, die Agenten-Instructions so zu gestalten, dass jeder Agent explizit auf die Ergebnisse des vorherigen Schritts referenziert.


### Lerneffekte

**Agenten-Architektur:** Das Projekt hat gezeigt, wie man durch die Zerlegung einer komplexen Aufgabe in spezialisierte Agenten bessere Ergebnisse erzielen kann als mit einem einzelnen, monolithischen Prompt. Jeder Agent kann sich auf seine Kernkompetenz konzentrieren.

**Prompt Engineering:** Die Qualität der Agent-Instructions hat einen direkten Einfluss auf die Qualität der Ergebnisse. Detaillierte, strukturierte Prompts mit klaren Anweisungen liefern deutlich bessere Ergebnisse als vage Beschreibungen.

**Tool-Calling als Erweiterung:** Durch die Integration des `analyze_marketing_tone`-Tools wurde klar, wie man LLM-Fähigkeiten durch externe Logik erweitern kann. Das Konzept von Tool-Calling: Das LLM entscheidet selbst, wann es ein Tool aufruft, ist ein mächtiges Pattern für praxisnahe Anwendungen.

**Iterative Verfeinerung:** Die Implementierung der Verfeinerungs-Funktion hat verdeutlicht, wie wichtig es ist, Nutzern Kontrolle über KI-generierte Inhalte zu geben. Ein einmaliger Output reicht in der Praxis selten aus. Iterative Anpassung ist der Schlüssel zu guten Ergebnissen.
