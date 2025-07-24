/**
 * Markiert alle Texte auf der Seite UND gibt den gefundenen Text in der Konsole aus.
 * Dies dient dazu, eine vollständige Liste für die Übersetzung zu erstellen.
 */
function highlightAndLogAllText() {
  console.log("Starte das Markieren und Protokollieren aller Texte...");

  const HIGHLIGHT_CLASS = 'text-marker-highlight';

  // Verhindere das mehrfache Hinzufügen des Styles
  if (!document.querySelector('#highlight-style')) {
    const style = document.createElement('style');
    style.id = 'highlight-style'; // Gib dem Style eine ID
    style.innerHTML = `
      .${HIGHLIGHT_CLASS} {
        outline: 2px solid #E50000;
        background-color: rgba(255, 0, 0, 0.1);
      }
    `;
    document.head.appendChild(style);
  }

  const highlightNode = (node) => {
    if (node.nodeType !== Node.ELEMENT_NODE) {
      return;
    }

    const walker = document.createTreeWalker(node, NodeFilter.SHOW_TEXT, null, false);
    let textNode;
    const nodesToWrap = [];

    while (textNode = walker.nextNode()) {
      const parentIsScriptOrStyle = ['SCRIPT', 'STYLE'].includes(textNode.parentElement.tagName);

      if (textNode.nodeValue.trim() !== '' && !textNode.parentElement.classList.contains(HIGHLIGHT_CLASS) && !parentIsScriptOrStyle) {
        nodesToWrap.push(textNode);
      }
    }

    nodesToWrap.forEach(tNode => {
      const wrapper = document.createElement('span');
      wrapper.classList.add(HIGHLIGHT_CLASS);
      wrapper.textContent = tNode.nodeValue;
      tNode.parentNode.replaceChild(wrapper, tNode);
    });
  };

  const observer = new MutationObserver((mutationsList) => {
    for (const mutation of mutationsList) {
      if (mutation.type === 'childList') {
        mutation.addedNodes.forEach(newNode => {
          highlightNode(newNode);
        });
      }
    }
  });

  observer.observe(document.body, {
    childList: true,
    subtree: true
  });

  highlightNode(document.body);
}

highlightAndLogAllText();
