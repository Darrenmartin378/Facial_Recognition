const video = document.getElementById('video');
const canvas = document.getElementById('canvas');
const statusEl = document.getElementById('status');
const captureBtn = document.getElementById('captureBtn');
const usernameInput = document.getElementById('username');
const registeredInfo = document.getElementById('registeredInfo');

navigator.mediaDevices.getUserMedia({ video: true })
    .then(stream => {
        video.srcObject = stream;
    })
    .catch(err => {
        statusEl.textContent = 'Error accessing webcam: ' + err;
    });

captureBtn.addEventListener('click', async () => {
    const username = usernameInput.value.trim();
    if (!username) {
        statusEl.textContent = 'Please enter a name.';
        statusEl.classList.remove('status-success');
        statusEl.classList.add('status-error');
        return;
    }

    const ctx = canvas.getContext('2d');
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
    const dataUrl = canvas.toDataURL('image/png');

    statusEl.textContent = 'Registering...';
    statusEl.classList.remove('status-success', 'status-error');
    registeredInfo.style.display = 'none';

    try {
        const res = await fetch('/register', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, image: dataUrl })
        });
        const json = await res.json();

        if (json.success) {
            const returnedName = json.username || username;
            const returnedId = json.id;

            statusEl.textContent = json.message;
            statusEl.classList.remove('status-error');
            statusEl.classList.add('status-success');

            if (returnedId !== undefined) {
                registeredInfo.textContent = `Successfully Registered with the ID: ${returnedId} and Name: ${returnedName}`;
            } else {
                registeredInfo.textContent = `Successfully Registered with the Name: ${returnedName}`;
            }
            registeredInfo.style.display = 'block';
        } else {
            statusEl.textContent = json.message || 'Registration failed.';
            statusEl.classList.remove('status-success');
            statusEl.classList.add('status-error');
        }
    } catch (e) {
        statusEl.textContent = 'Error: ' + e;
        statusEl.classList.remove('status-success');
        statusEl.classList.add('status-error');
    }
});
