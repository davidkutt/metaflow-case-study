# scraper/management/commands/generate_translation_script.py

import os
import json
import re
import requests
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
from django.core.management.base import BaseCommand

# --- Konfiguration ---
# Die URLs, die analysiert werden sollen.
URLS_TO_SCRAPE = [
    "https://metaflow-x-casestudy.lovable.app/",
    "https://metaflow-x-casestudy.lovable.app/subscriptions",
    "https://metaflow-x-casestudy.lovable.app/history",
    "https://metaflow-x-casestudy.lovable.app/profile",
    "https://metaflow-x-casestudy.lovable.app/settings",
]

# Der Endpunkt der Übersetzungs-API.
TRANSLATE_API_ENDPOINT = "https://libretranslate.de/translate"

# Der Speicherort für die fertige JavaScript-Datei.
OUTPUT_JS_FILE = "static/js/translator.js"

class Command(BaseCommand):
    help = "Scrapt Webseiten, übersetzt Texte und generiert ein JavaScript-Übersetzungsskript."

    def handle(self, *args, **options):
        """
        Die Hauptmethode, die beim Aufruf des Commands ausgeführt wird.
        """
        self.stdout.write(self.style.SUCCESS("🚀 Starte den Prozess zur Generierung des Übersetzungsskripts..."))

        # Schritt 1: Texte von den Webseiten extrahieren.
        unique_texts = self.scrape_texts()
        if not unique_texts:
            self.stdout.write(self.style.ERROR("❌ Keine Texte zum Übersetzen gefunden. Breche ab."))
            return

        # Schritt 2: Extrahierte Texte mit LibreTranslate übersetzen.
        translations = self.translate_texts(unique_texts)
        if not translations:
            self.stdout.write(self.style.ERROR("❌ Übersetzung fehlgeschlagen. Breche ab."))
            return

        # Schritt 3: Das JavaScript-Skript mit den neuen Übersetzungen generieren.
        self.generate_js_file(translations)

        self.stdout.write(self.style.SUCCESS(f"✅ Prozess abgeschlossen! Das Skript wurde in '{OUTPUT_JS_FILE}' gespeichert."))

    def scrape_texts(self) -> set:
        """
        Nutzt Playwright, um die JavaScript-lastigen Seiten zu rendern und alle sichtbaren Texte zu extrahieren.
        """
        self.stdout.write(f"🔎 Scrape {len(URLS_TO_SCRAPE)} URLs, um Texte zu extrahieren...")
        all_texts = set()

        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()

            for url in URLS_TO_SCRAPE:
                try:
                    self.stdout.write(f"   -> Lade {url}")
                    page.goto(url, wait_until="networkidle")
                    content = page.content()
                    soup = BeautifulSoup(content, "html.parser")

                    # Extrahiere Texte aus dem Body und filtere unerwünschte Tags.
                    for element in soup.find_all(['script', 'style']):
                        element.decompose()

                    # Finde alle Textknoten und säubere sie.
                    for text in soup.body.stripped_strings:
                        # Ignoriere rein numerische oder sehr kurze Texte.
                        if not text.isnumeric() and len(text) > 2 and not text.startswith('radix-'):
                             all_texts.add(text)
                except Exception as e:
                    self.stderr.write(self.style.ERROR(f"Fehler beim Scrapen von {url}: {e}"))

            browser.close()

        self.stdout.write(self.style.SUCCESS(f"👍 {len(all_texts)} einzigartige Texte gefunden."))
        return all_texts

    def translate_texts(self, texts_to_translate: set) -> dict:
        """
        Sendet die gesammelten Texte an die LibreTranslate API.
        """
        self.stdout.write(f"🌍 Übersetze {len(texts_to_translate)} Texte via LibreTranslate API...")
        translations = {}
        # LibreTranslate verarbeitet am besten kleinere Batches.
        text_list = list(texts_to_translate)

        try:
            # Sende den gesamten Text als einen String mit Zeilenumbrüchen,
            # da die API so am besten mit Batches umgeht.
            q = "\n".join(text_list)
            payload = {
                'q': q,
                'source': 'en',
                'target': 'de',
                'format': 'text'
            }
            response = requests.post(TRANSLATE_API_ENDPOINT, json=payload)
            response.raise_for_status() # Löst einen Fehler bei HTTP-Status 4xx/5xx aus.

            translated_text_blob = response.json().get('translatedText', '')
            translated_lines = translated_text_blob.split('\n')

            # Ordne die übersetzten Zeilen den Originaltexten zu.
            if len(text_list) == len(translated_lines):
                for i, original_text in enumerate(text_list):
                    translations[original_text] = translated_lines[i]
                self.stdout.write(self.style.SUCCESS("👍 Übersetzung erfolgreich abgeschlossen."))
                return translations
            else:
                self.stderr.write(self.style.ERROR("Fehler: Anzahl der Originaltexte und übersetzten Zeilen stimmt nicht überein."))
                return {}

        except requests.exceptions.RequestException as e:
            self.stderr.write(self.style.ERROR(f"Fehler bei der API-Anfrage: {e}"))
            return {}

    def generate_js_file(self, translations: dict):
        """
        Erstellt die finale JavaScript-Datei basierend auf einem Template und den Übersetzungen.
        """
        self.stdout.write("⚙️ Generiere die finale JavaScript-Datei...")

        # Konvertiere das Python-Dict in einen sauberen JSON-String für JavaScript.
        # `ensure_ascii=False` ist wichtig für Umlaute.
        js_translations_json = json.dumps(translations, indent=4, ensure_ascii=False)

        # JavaScript-Template. Dies ist dein elegantes Skript, gefüttert mit den neuen Daten.
        js_template = f"""
/**
 * Automatisches Übersetzungsskript
 * Generiert am: {self.get_current_timestamp()}
 * Übersetzungen generiert via LibreTranslate API.
 *
 * Dieses Skript wird durch ein Django-Backend automatisch erstellt und gewartet.
 */
(function() {{
    'use strict';

    // 1. Das dynamisch generierte Übersetzungs-Wörterbuch
    const translations = {js_translations_json};

    // 2. Die Logik zur Anwendung der Übersetzungen
    const processedNodes = new WeakSet();

    function localizeNode(node) {{
        if (!node || node.nodeType !== Node.ELEMENT_NODE || processedNodes.has(node)) {{
            return;
        }}
        processedNodes.add(node);

        const walker = document.createTreeWalker(node, NodeFilter.SHOW_TEXT);
        let textNode;

        while (textNode = walker.nextNode()) {{
            const originalText = textNode.nodeValue.trim();
            if (translations[originalText]) {{
                // Ersetze den gefundenen Text mit seiner Übersetzung
                textNode.nodeValue = textNode.nodeValue.replace(originalText, translations[originalText]);
            }}
        }}
    }}

    // 3. MutationObserver, um auf dynamische Inhalte zu reagieren
    const observer = new MutationObserver((mutationsList) => {{
        for (const mutation of mutationsList) {{
            mutation.addedNodes.forEach(localizeNode);
        }}
    }});

    // Starte die Beobachtung und führe eine erste Lokalisierung durch.
    observer.observe(document.body, {{ childList: true, subtree: true }});
    localizeNode(document.body);

    console.log('Automatisch generiertes Übersetzungsskript V1.0 geladen.');
}})();
"""
        # Stelle sicher, dass das Zielverzeichnis existiert.
        os.makedirs(os.path.dirname(OUTPUT_JS_FILE), exist_ok=True)

        # Schreibe das fertige Skript in die Datei.
        with open(OUTPUT_JS_FILE, 'w', encoding='utf-8') as f:
            f.write(js_template)

    def get_current_timestamp(self):
        from datetime import datetime
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

