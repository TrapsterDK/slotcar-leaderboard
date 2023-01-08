$(document).ready(function () {
    $(".racer").click(function () {
        eel.set_current_racer($(this).attr("id"), "racer.html");
    });
});
