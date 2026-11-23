// Prognose's one optional script (AD-11). Every page works without it.

// Safari restores a page from its back/forward cache even when the server said
// no-store, so Back after «Logg ut» would show the company's page again. A
// restored page asks the server instead, which sends a visitor without a login
// to the login page (AD-6, NFR-10).
window.addEventListener("pageshow", (event) => {
  if (event.persisted) {
    window.location.reload();
  }
});
