var interval = null;

var lap = 0;
eel.expose(AddLapTime);
function AddLapTime(ms) {
    var element = document.getElementById("lap-" + lap);
    element.innerHTML = `<p>${lap + 1}</p><p>${(ms / 1000).toFixed(2)}</p>`;
    lap += 1;
}

eel.expose(resetcountup);
function resetcountup() {
    console.log("resetcountup");
    clearInterval(interval);
    startTime = Date.now();
    interval = setInterval(function () {
        var elapsedTime = Date.now() - startTime;
        document.getElementById("timer").innerHTML = (
            elapsedTime / 1000
        ).toFixed(2);
    }, 10);
}

eel.expose(last_lap);
function last_lap(ms) {
    clearInterval(interval);
    document.getElementById("timer").innerHTML = (ms / 1000).toFixed(2);
    $("#racer-restart").attr("disabled", true);
    setTimeout(function () {
        eel.stop_race("leaderboard.html");
    }, 3000);
}

eel.expose(time_run_out);
function time_run_out() {
    clearInterval(interval);
    document.getElementById("timer").innerHTML =
        "Tiden udløb, går til leaderboard om 3 sekunder";
    $("#racer-restart").attr("disabled", true);
    setTimeout(function () {
        eel.stop_race("leaderboard.html");
    }, 3000);
}

$(document).ready(function () {
    $("#racer-back").click(function () {
        eel.stop_race("leaderboard.html");
    });
    $("#racer-restart").click(function () {
        eel.page_loaded("None");
        eel.reset_race("racer.html");
    });
});
