eel.expose(go_to_jinja_page);
function go_to_jinja_page(string) {
    document.getElementsByTagName("html")[0].innerHTML = string;
}

function go_to_page(page) {
    eel.go_to_page(page)();
}

eel.expose(stop)
function stop() {
    window.close()
}