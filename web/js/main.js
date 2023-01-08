eel.expose(stop);
function stop() {
    window.close();
}

eel.expose(change_page);
function change_page(page) {
    window.location.href = page;
}

eel.page_loaded(window.location.href);
