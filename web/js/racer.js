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
    setTimeout(function () {
        window.location.href = "leaderboard.html";
    }, 3000);
}
