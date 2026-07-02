async function scanNetwork() {
    const loading = document.getElementById('loading');
    const devicesDiv = document.getElementById('devices');
    
    loading.style.display = 'block';
    devicesDiv.innerHTML = '';

    try {
        const response = await fetch('/api/scan');
        const data = await response.json();
        
        if (data.devices && data.devices.length > 0) {
            devicesDiv.innerHTML = '';
            data.devices.forEach(device => {
                const card = document.createElement('div');
                card.className = 'device-card';
                card.innerHTML = `
                    <h3>${device.hostname}</h3>
                    <div class="ip">📡 ${device.ip}</div>
                    <div class="status-${device.status.toLowerCase()}">${device.status}</div>
                `;
                devicesDiv.appendChild(card);
            });
        } else {
            devicesDiv.innerHTML = '<p>No se encontraron dispositivos activos en la red.</p>';
        }
    } catch (error) {
        devicesDiv.innerHTML = `<p>❌ Error al escanear: ${error.message}</p>`;
    } finally {
        loading.style.display = 'none';
    }
}
