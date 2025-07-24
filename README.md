# Case Study: Lokalisierung einer Shopify App

Dieses Repository enthält die Lösung für die technische Case Study von MetaFlow, präsentiert am 24.07.2025.

---

## 🎯 Die Herausforderung

Die Aufgabe bestand darin, ein kritisches Problem in einer Live-Umgebung unter strengen Vorgaben zu lösen.

* 🐛 **Unvollständige Übersetzung:** Die Benutzeroberfläche einer Shopify App (StayAI) war teilweise auf Englisch, obwohl deutsche Übersetzungen hinterlegt waren.

* 📅 **Falsche Formate:** Datums- und Währungsformate wurden nicht korrekt für den deutschen Markt dargestellt.

* 🚫 **Strikte Einschränkungen:** Der App-Support bot keine Hilfe und die Installation einer alternativen App war keine Option.

---

## 🕵️ Vorgehensweise

* **Untersuchung der Seite:**
    * Prüfung, ob bestehende `<script>`-Tags oder `translation keys` für eine Frontend-Übersetzung genutzt werden können. (Ergebnis: Nein ❌)
* **Planänderung:**
    * Entscheidung, die Seite clientseitig per Skript zu überarbeiten, da kein direkter Zugriff möglich war.
* **Entwicklung & Problemlösung:**
    * Identifizierung aller fehlerhaften Texte durch schnelles Prototyping ("Vibecoding").
    * Erstellung eines ersten Skripts mit KI-Unterstützung. 🤖
    * Erstes Ergebis: nicht alle Texte übersetzt. 
      * Dynamisches Rendering über ein Skript? Nein ❌ 
      * Aber: Testing zeigt, dass nur die erste Seite übersetzt wird ✅
    * Implementierung mittels `MutationObserver`
    * Debugging und Erweiterung der Übersetzungsliste.
* **Zwischenfazit:**
    * Eine voll funktionsfähige erste Version stand nach ca. 1,5 Stunden. ✅
    * Deutsche Nutzer können wieder problemlos ihre MetaFlow Subscriptions. ✅
* **Problem:**
  * Sollte das Problem bestehen bleiben, müssen Texte im Skript angepasst/hinzugefügt werden 🚧
* **Ausblick:**
  * Sollte das Problem bestehen bleiben: Backend Service, der eine Translations Datei pflegt
  * Achtung - Zeitgrab! 🚩⛔
* **Ergebnis:**
    * Entwicklungsstopp für Service. Starte Vorbereitung der Präsentation ✅
    * Gesamtdauer (ca. 1 PT)
* **Feedback:**
    * "Erster Kunde hat sich beschwert", dass 2 Übersetzungen fehlen. Ups"
  
### 1. `highlight-texts.js`
Einfaches Skript zum Finden und Kenntlich machen von Texten
### 2. `translator-v1.js`
Erste und einfache Lösung mit Problemen

### 3. `translator-v2.js`
Verbesserte Version mit MutationObserver

---

## Testanleitung

1.  Navigieren Sie zur Test-URL: `https://metaflow-x-casestudy.lovable.app/?name=David`
2.  Öffnen Sie die Entwicklerkonsole Ihres Browsers.
3.  Kopieren Sie den gesamten Inhalt von entweder `solution-einfach.js` oder `solution-refactored.js`.
4.  Fügen Sie das Skript in die Konsole ein und drücken Sie Enter.
5.  Interagieren Sie mit der Seite und beobachten Sie, wie alle relevanten englischen Texte in Echtzeit ins Deutsche übersetzt werden.
