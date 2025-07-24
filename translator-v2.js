function translate() {

  const DEBUG_MODE = false;

  if (DEBUG_MODE) {
    if (!document.querySelector('#translation-debug-style')) {
      const style = document.createElement('style');
      style.id = 'translation-debug-style';
      style.innerHTML = `
                .translation-debug-highlight {
                    outline: 2px solid rgba(255, 87, 51, 0.7) !important;
                    background-color: rgba(255, 87, 51, 0.05) !important;
                }
            `;
      document.head.appendChild(style);
    }
  }

  const processedNodes = new WeakSet();

  const translations = [
    ['City', 'Stadt'],
    ['Paused Subscriptions', 'Pausierte Abonnements'],
    ['Update your delivery address for subscriptions', 'Aktualisiere deine Lieferadresse für Abonnements'],
    ['Street Address', 'Straße und Hausnummer'],
    ['Postal Code', 'Postleitzahl'],
    ['New Subscription', 'Neues Abonnement'],
    ['Delivery Address', 'Lieferadresse'],
    ['Next delivery:', 'Nächste Lieferung:'],
    ['Selected flavors:', 'Ausgewählte Geschmacksrichtungen:'],
    ['flavors for', 'für'],
    ['Started on', 'Gestartet am'],
    ['Skipped until', 'Übersprungen bis'],
    ['Paused until', 'Pausiert bis'],
    ['Edit Address', 'Adresse bearbeiten'],
    ['Subscriptions', 'Abonnements'], // Plural first
    ['Subscription', 'Abonnement'],
    ['Canceled', 'Storniert'],
    ['Skipped', 'Übersprungen'],
    ['Active', 'Aktiv'],
    ['Paused', 'Pausiert'],
    ['weeks', 'Wochen'], // Plural first
    ['week', 'Woche'],
    ['Country', 'Land'],
  ];

  function localizeNode(node) {
    if (!node || node.nodeType !== Node.ELEMENT_NODE || processedNodes.has(node)) {
      return;
    }
    processedNodes.add(node);

    const walker = document.createTreeWalker(node, NodeFilter.SHOW_TEXT, null, false);
    let textNode;

    while (textNode = walker.nextNode()) {
      const originalText = textNode.nodeValue;
      let modifiedText = originalText;

      for (const [key, value] of translations) {
        modifiedText = modifiedText.replace(new RegExp(key, 'gi'), value);
      }

      const dateRegex = /(?:(?:Mon|Tues|Wed|Thurs|Fri|Sat|Sun)day,\s)?(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s(\d{1,2}),\s(\d{4})/g;
      modifiedText = modifiedText.replace(dateRegex, (match) => {
        try {
          return new Date(match).toLocaleDateString('de-DE', {day: '2-digit', month: '2-digit', year: 'numeric'});
        } catch (e) {
          return match;
        }
      });

      const shortDateRegex = /(\d{1,2})\s+(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)(?!,)/g;
      modifiedText = modifiedText.replace(shortDateRegex, '$1. $2.');


      if (originalText !== modifiedText) {
        textNode.nodeValue = modifiedText;
        if (DEBUG_MODE && textNode.parentElement) {
          textNode.parentElement.classList.add('translation-debug-highlight');
        }
      }
    }
  }

  const observer = new MutationObserver((mutationsList) => {
    for (const mutation of mutationsList) {
      mutation.addedNodes.forEach(localizeNode);
    }
  });

  observer.observe(document.body, {childList: true, subtree: true});
  localizeNode(document.body);

  if (DEBUG_MODE) {
    console.log("DEBUG_MODE: ", DEBUG_MODE);
  }
}

translate();
