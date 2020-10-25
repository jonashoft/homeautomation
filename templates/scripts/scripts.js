async function turnLampOnOff(newState) {
    await fetch(`/background_process?state=${newState}`);

    document.getElementById('result').innerHTML = newState ? "On" : "Off";
}

document.getElementById('TurnOn').addEventListener(async () => {
    await turnLampOnOff(true);
});
document.getElementById('TurnOff').addEventListener(async () => {
    await turnLampOnOff(false);
});