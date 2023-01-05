$(document).ready(function () {
    $(".racer").click(function () {
        eel.set_current_racer($(this).attr("id"));
        window.location.href = "racer.html";
    });
});
