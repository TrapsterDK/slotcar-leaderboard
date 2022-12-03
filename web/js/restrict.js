$(document).ready(function() {
    // input restrict for class="input-positive-integer" with only positive integer
    $('.input-positive-integer').on('keydown', function(evt) {
        if(!((evt.keyCode > 95 && evt.keyCode < 106) // numpad
            || (evt.keyCode > 47 && evt.keyCode < 58) // number keys
            || evt.keyCode == 8 // backspace
            || evt.ctrlKey && (evt.keyCode  == 65 || evt.keyCode == 97))) { // Ctrl+A
                evt.preventDefault();
                return false;
        }
    });
});