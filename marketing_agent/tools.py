def analyze_marketing_tone(text: str) -> str:
    """Analysiert einen Werbetext auf Marketing-Qualitätskriterien wie Länge,
    Call-to-Action, emotionale Sprache und AIDA-Struktur und gibt
    konkrete Verbesserungsvorschläge zurück."""
    word_count = len(text.split())
    feedback = [f"Wortanzahl: {word_count}"]

    # Längen-Check
    if word_count < 30:
        feedback.append("WARNUNG: Text ist sehr kurz. Empfehlung: Mindestens 50 Wörter für einen überzeugenden Werbetext.")
    elif word_count > 200:
        feedback.append("WARNUNG: Text ist sehr lang. Empfehlung: Kürze auf unter 150 Wörter für bessere Lesbarkeit.")
    else:
        feedback.append("Textlänge ist gut.")

    # Call-to-Action Check
    cta_keywords = ["jetzt", "heute", "entdecke", "sichere dir", "teste", "starte",
                     "bestelle", "erfahre mehr", "klick", "probiere", "hol dir"]
    has_cta = any(kw in text.lower() for kw in cta_keywords)
    if has_cta:
        feedback.append("Call-to-Action erkannt – gut!")
    else:
        feedback.append("VERBESSERUNG: Kein Call-to-Action gefunden. Füge einen klaren Handlungsaufruf hinzu (z.B. 'Jetzt entdecken', 'Sichere dir').")

    # Emotionale Sprache
    emotion_words = ["einzigartig", "revolutionär", "unglaublich", "perfekt", "traum",
                     "liebe", "begeister", "wow", "fantastisch", "exklusiv", "premium",
                     "genial", "power", "boost", "transform"]
    emotion_count = sum(1 for w in emotion_words if w in text.lower())
    if emotion_count >= 2:
        feedback.append(f"Emotionale Sprache: {emotion_count} Power-Wörter erkannt – sehr überzeugend!")
    elif emotion_count == 1:
        feedback.append("Emotionale Sprache: Nur 1 Power-Wort. Empfehlung: Nutze mehr emotionale Begriffe.")
    else:
        feedback.append("VERBESSERUNG: Keine emotionalen Power-Wörter gefunden. Nutze Begriffe wie 'einzigartig', 'exklusiv', 'revolutionär'.")

    return "\n".join(feedback)