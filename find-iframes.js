/**
 * Listet alle iframes auf der Seite und ihre Quell-URL auf.
 * Das wird uns zeigen, ob die App gekapselt ist.
 */
function findIframes() {
  const iframes = document.querySelectorAll('iframe');
  if (iframes.length > 0) {
    console.log(`Es wurde(n) ${iframes.length} iframe(s) gefunden!`);
    iframes.forEach((frame, index) => {
      console.log(`iFrame #${index + 1}:`, frame);
      console.log(`   Quelle (src): ${frame.src}`);
    });
    console.log("---");
    console.log("Das bestätigt, dass die App isoliert ist. Unsere Skripte müssen IN der App laufen, nicht außerhalb.");
  } else {
    console.log("Keine iframes gefunden. Das ist sehr unerwartet.");
  }
}

findIframes();
