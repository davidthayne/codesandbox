# Test HTML/CSS Generation
def create_test_page():
    html_content = """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Test HTML Page</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%);
            margin: 0;
            padding: 20px;
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .container {
            background: rgba(255,255,255,0.95);
            padding: 40px;
            border-radius: 20px;
            box-shadow: 0 15px 35px rgba(0,0,0,0.1);
            text-align: center;
            max-width: 500px;
        }
        h1 {
            color: #2c3e50;
            margin-bottom: 20px;
        }
        .btn {
            background: linear-gradient(45deg, #3498db, #2980b9);
            color: white;
            padding: 15px 30px;
            border: none;
            border-radius: 10px;
            cursor: pointer;
            font-size: 16px;
            margin: 10px;
            transition: transform 0.3s ease;
        }
        .btn:hover {
            transform: translateY(-2px);
        }
        .feature {
            background: #ecf0f1;
            padding: 15px;
            margin: 15px 0;
            border-radius: 10px;
            border-left: 4px solid #3498db;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🎉 HTML/CSS Support Added!</h1>
        <p>The Python sandbox now supports creating interactive web interfaces!</p>
        
        <div class="feature">
            <strong>✨ Features:</strong><br>
            • Beautiful CSS styling<br>
            • Interactive elements<br>
            • Responsive design<br>
            • Real-time preview
        </div>
        
        <button class="btn" onclick="alert('HTML/CSS is working! 🚀')">
            Test Interactivity
        </button>
        
        <button class="btn" onclick="document.body.style.background='linear-gradient(45deg, #667eea, #764ba2)'">
            Change Background
        </button>
    </div>
</body>
</html>"""
    return html_content

# Generate and display the test page
test_page = create_test_page()
print(test_page)
