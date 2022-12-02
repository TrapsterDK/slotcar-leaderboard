function py_video() {
    eel.video_feed()()
}

function py_stop() {
    eel.stop_feed()()
}

eel.expose(updateImageSrc);
function updateImageSrc(val) {
    let elem = document.getElementById('bg');
    elem.src = "data:image/jpeg;base64," + val
}

function text_set(){
    let elem = document.getElementById('textsetter');
    eel.text_set(elem.value)()
}

eel.expose(add_text);
function add_text(val) {
    let elem = document.getElementById('text');
    elem.innerHTML = val
}