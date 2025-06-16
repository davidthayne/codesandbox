#!/usr/bin/env python3
"""
Test script to verify the Apps functionality end-to-end
"""
import requests
import json
import time

BASE_URL = "http://localhost:7111"

def test_apps_workflow():
    print("🧪 Testing Apps Workflow...")
    
    # Create a session
    session = requests.Session()
    
    # 1. Login first
    print("1. Testing login...")
    login_response = session.post(f"{BASE_URL}/login", data={
        'username': 'test_user',
        'password': 'test_pass'
    })
    
    if login_response.status_code != 200:
        print(f"❌ Login failed: {login_response.status_code}")
        return False
    
    print("✅ Login successful")
    
    # 2. Test listing apps (should be empty initially)
    print("2. Testing apps list...")
    apps_response = session.get(f"{BASE_URL}/apps")
    
    if apps_response.status_code != 200:
        print(f"❌ Apps list failed: {apps_response.status_code}")
        return False
    
    apps_data = apps_response.json()
    print(f"✅ Apps list successful: {len(apps_data.get('apps', []))} apps found")
    
    # 3. Test saving a new app
    print("3. Testing app save...")
    test_app = {
        'name': 'Test Calculator',
        'description': 'A simple calculator app',
        'code': '''# Simple Calculator
def add(a, b):
    return a + b

def multiply(a, b):
    return a * b

# Test calculations
print(f"2 + 3 = {add(2, 3)}")
print(f"4 * 5 = {multiply(4, 5)}")

# Create a simple HTML output
html = """<!DOCTYPE html>
<html>
<head>
    <title>Calculator</title>
    <style>
        body { font-family: Arial; padding: 20px; background: #f0f0f0; }
        .calc { background: white; padding: 20px; border-radius: 10px; max-width: 300px; }
        button { padding: 10px; margin: 5px; font-size: 16px; }
    </style>
</head>
<body>
    <div class="calc">
        <h2>Simple Calculator</h2>
        <p>2 + 3 = 5</p>
        <p>4 × 5 = 20</p>
        <button onclick="alert('Calculator works!')">Test</button>
    </div>
</body>
</html>"""

print(html)'''
    }
    
    save_response = session.post(f"{BASE_URL}/apps", 
                                json=test_app,
                                headers={'Content-Type': 'application/json'})
    
    if save_response.status_code != 200:
        print(f"❌ App save failed: {save_response.status_code}")
        print(f"Response: {save_response.text}")
        return False
    
    save_data = save_response.json()
    if not save_data.get('success'):
        print(f"❌ App save unsuccessful: {save_data}")
        return False
    
    print("✅ App save successful")
    
    # 4. Test listing apps again (should have 1 app)
    print("4. Testing apps list after save...")
    apps_response = session.get(f"{BASE_URL}/apps")
    apps_data = apps_response.json()
    
    if len(apps_data.get('apps', [])) != 1:
        print(f"❌ Expected 1 app, found {len(apps_data.get('apps', []))}")
        return False
    
    print("✅ Apps list shows 1 app correctly")
    
    # 5. Test loading the app
    print("5. Testing app load...")
    load_response = session.get(f"{BASE_URL}/apps/{test_app['name']}")
    
    if load_response.status_code != 200:
        print(f"❌ App load failed: {load_response.status_code}")
        return False
    
    load_data = load_response.json()
    if load_data.get('code') != test_app['code']:
        print("❌ Loaded code doesn't match saved code")
        return False
    
    print("✅ App load successful")
    
    # 6. Test updating the app
    print("6. Testing app update...")
    updated_app = test_app.copy()
    updated_app['description'] = 'Updated calculator with more features'
    updated_app['code'] += '\n\n# Updated with division\nprint(f"10 / 2 = {10 / 2}")'
    
    update_response = session.post(f"{BASE_URL}/apps", 
                                  json=updated_app,
                                  headers={'Content-Type': 'application/json'})
    
    if update_response.status_code != 200:
        print(f"❌ App update failed: {update_response.status_code}")
        return False
    
    print("✅ App update successful")
    
    # 7. Test deleting the app
    print("7. Testing app delete...")
    delete_response = session.delete(f"{BASE_URL}/apps/{test_app['name']}")
    
    if delete_response.status_code != 200:
        print(f"❌ App delete failed: {delete_response.status_code}")
        return False
    
    delete_data = delete_response.json()
    if not delete_data.get('success'):
        print(f"❌ App delete unsuccessful: {delete_data}")
        return False
    
    print("✅ App delete successful")
    
    # 8. Test listing apps after delete (should be empty)
    print("8. Testing apps list after delete...")
    apps_response = session.get(f"{BASE_URL}/apps")
    apps_data = apps_response.json()
    
    if len(apps_data.get('apps', [])) != 0:
        print(f"❌ Expected 0 apps, found {len(apps_data.get('apps', []))}")
        return False
    
    print("✅ Apps list is empty after delete")
    
    print("\n🎉 All tests passed! Apps functionality is working correctly.")
    return True

if __name__ == "__main__":
    try:
        success = test_apps_workflow()
        exit(0 if success else 1)
    except Exception as e:
        print(f"❌ Test failed with exception: {e}")
        exit(1)
