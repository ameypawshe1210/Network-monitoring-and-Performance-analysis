async function loadData() {
    try {
        const response = await fetch("network_data.json");
        const data = await response.json();

        const table = document.getElementById("networkTable");
        // Clear old rows except for the header
        table.innerHTML = "<tr><th>Host</th><th>Status</th><th>Speed (Latency)</th></tr>";

        let active = 0;

        data.forEach(device => {
            let statusClass = device.status === "Active" ? "status-up" : "status-down";
            if (device.status === "Active") active++;

            let row = `
                <tr>
                    <td>${device.host}</td>
                    <td class="${statusClass}">${device.status}</td>
                    <td>${device.latency}</td>
                </tr>`;
            table.innerHTML += row;
        });

        document.getElementById("deviceCount").innerText = data.length;
        document.getElementById("activeCount").innerText = active;
        document.getElementById("downCount").innerText = data.length - active;

    } catch (error) {
        console.error("Waiting for JSON file update...", error);
    }
}

// Check for updates every 3 seconds
setInterval(loadData, 3000);
loadData();