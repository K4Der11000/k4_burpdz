function loadIframe() {
    const url = document.getElementById("iframeUrl").value;
    document.getElementById("targetFrame").src = url;
}

function showSuccess() {
    fetch('/api/status')
        .then(res => res.json())
        .then(data => {
            const successes = data.results.filter(r => r.status === 'Success');
            const table = document.getElementById("resultTable");
            table.innerHTML = '';
            successes.forEach((row, i) => {
                table.innerHTML += `<tr><td>${i + 1}</td><td>${row.username}</td><td>${row.password}</td><td>${row.status}</td></tr>`;
            });
        });
}

function stopAttack() {
    fetch('/api/stop', { method: 'POST' })
        .then(res => res.text())
        .then(msg => console.log(msg));
}

function resumeAttack() {
    fetch('/api/resume', { method: 'POST' })
        .then(res => res.text())
        .then(msg => console.log(msg));
}

function updateStatus() {
    fetch('/api/status')
        .then(res => res.json())
        .then(data => {
            const terminal = document.getElementById("terminalOutput");
            const details = document.getElementById("detailsBox");
            terminal.innerHTML = '';
            details.innerHTML = '';
            data.results.forEach((r, i) => {
                terminal.innerHTML += `[${i}] ${r.username} : ${r.password} => ${r.status}\n`;
                details.innerHTML += `${r.username}:${r.password} => ${r.status}\n`;
            });
        });
}

setInterval(updateStatus, 3000);
