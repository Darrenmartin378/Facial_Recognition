# Facial_Recognition


commands for python to enable facial recognition:
```
pip install flask opencv-python numpy
```
venv\Scripts\activate
```
python app.py


<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Face Registration</title>
    <style>
        body {
            margin: 0;
            font-family: Arial, Helvetica, sans-serif;
            background-color: #f5f5f5;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
        }

        .card {
            background-color: #ffffff;
            padding: 24px 32px;
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
            max-width: 420px;
            width: 100%;
        }

        h1 {
            margin-top: 0;
            font-size: 22px;
            text-align: center;
        }

        label {
            display: block;
            font-size: 14px;
            margin-bottom: 4px;
        }

        input[type="text"] {
            width: 100%;
            padding: 8px 10px;
            border-radius: 4px;
            border: 1px solid #ccc;
            margin-bottom: 12px;
            box-sizing: border-box;
        }

        .video-container {
            display: flex;
            justify-content: center;
            margin-bottom: 12px;
        }

        video {
            border-radius: 4px;
            background-color: #333;
            transform: scaleX(-1);
        }

        button {
            width: 100%;
            padding: 10px 0;
            border: none;
            border-radius: 4px;
            background-color: #2563eb;
            color: #ffffff;
            font-weight: 600;
            cursor: pointer;
            margin-bottom: 8px;
        }

        button:hover {
            background-color: #1d4ed8;
        }

        #status {
            font-size: 13px;
            margin: 4px 0 8px;
            min-height: 18px;
        }

        .status-success {
            color: #16a34a;
        }

        .status-error {
            color: #dc2626;
        }

        #registeredInfo {
            margin-top: 8px;
            padding: 8px 10px;
            border-radius: 4px;
            background-color: #ecfdf5;
            border: 1px solid #bbf7d0;
            font-size: 14px;
            display: none;
        }
    </style>
</head>
<body>
    <div class="card">
        <h1>Register with Face</h1>

        <label for="username">Full name</label>
        <input type="text" id="username" placeholder="Enter your name">

        <div class="video-container">
            <video id="video" width="300" height="220" autoplay muted playsinline></video>
        </div>

        <button id="captureBtn">Capture &amp; Register</button>

        <p id="status"></p>

        <div id="registeredInfo"></div>

        <canvas id="canvas" width="320" height="240" style="display:none;"></canvas>
    </div>

    <script src="/static/register.js"></script>
</body>
</html>
