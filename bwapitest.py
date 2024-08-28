import aiohttp
import asyncio
import json
import os
from datetime import datetime

# Configurable variables
BASE_URL = 'https://app.blackwire.ai/api'
API_KEY = {
    "clientId": "YOUR_CLIENT_ID_HERE",  # Available in app.blackwire.ai -> User Profile -> Edit Profile -> Personal Tokens
    "secret": "YOUR_SECRET_HERE"        # Available in app.blackwire.ai -> User Profile -> Edit Profile -> Personal Tokens
}
OWNER_ID = "YOUR_OWNER_ID_HERE"  # Can be retrieved from the /settings endpoint response
TENANT_ID = "YOUR_TENANT_ID_HERE"  # Can be retrieved from the /settings endpoint response

headers = {
    'x-api-key': json.dumps(API_KEY),
    'Content-Type': 'application/json'
}

# ANSI color codes
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
RESET = '\033[0m'

def color_output(text, color):
    return f"{color}{text}{RESET}"

def format_response(response_data, max_length=150):
    if isinstance(response_data, str):
        return (response_data[:max_length] + '...') if len(response_data) > max_length else response_data
    elif isinstance(response_data, dict):
        return json.dumps(response_data)[:max_length] + '...'
    else:
        return str(response_data)[:max_length] + '...'

async def test_endpoint(session, method, endpoint, data=None):
    start_time = datetime.now()
    url = f"{BASE_URL}{endpoint}"
    try:
        if method == 'GET':
            async with session.get(url) as response:
                response_data = await handle_response(response)
        elif method == 'POST':
            if endpoint == '/ai-conversation-stream':
                async with session.post(url, json=data) as response:
                    response_data = await handle_streaming_response(response)
            else:
                async with session.post(url, json=data) as response:
                    response_data = await handle_response(response)
        elif method == 'DELETE':
            async with session.delete(url) as response:
                response_data = await handle_response(response)
        
        status = response.status
        time_taken = (datetime.now() - start_time).total_seconds() * 1000
        
        color = GREEN if status in [200, 201, 204] else RED
        time_color = YELLOW if time_taken > 1000 else GREEN
        
        status_str = color_output(f"Status: {status}", color)
        time_str = color_output(f"Time: {time_taken:.2f}ms", time_color)
        
        print(f"{method} {endpoint} - {status_str}, {time_str}")
        
        if response_data and status in [200, 201]:
            print(f"Response: {format_response(response_data)}")
        
        return {
            'timestamp': datetime.now().isoformat(),
            'endpoint': endpoint,
            'method': method,
            'status': status,
            'timeTaken': f"{time_taken:.2f}",
            'error': None
        }, response_data
    except Exception as e:
        time_taken = (datetime.now() - start_time).total_seconds() * 1000
        error_str = color_output(f"Error: {str(e)}", RED)
        time_str = color_output(f"Time: {time_taken:.2f}ms", YELLOW if time_taken > 1000 else GREEN)
        print(f"{method} {endpoint} - {error_str}, {time_str}")
        return {
            'timestamp': datetime.now().isoformat(),
            'endpoint': endpoint,
            'method': method,
            'status': 500,
            'timeTaken': f"{time_taken:.2f}",
            'error': str(e)
        }, None

async def handle_response(response):
    content_type = response.headers.get('Content-Type', '')
    if 'application/json' in content_type:
        return await response.json()
    else:
        return await response.text()

async def handle_streaming_response(response):
    chunks = []
    async for chunk in response.content.iter_any():
        chunks.append(chunk.decode())
    return ''.join(chunks)

async def run_tests():
    async with aiohttp.ClientSession(headers=headers) as session:
        # Get conversation ID
        conversation_result, response_data = await test_endpoint(session, 'GET', '/ai-conversation')

        if response_data and conversation_result['status'] in [200, 201]:
            conversation_id = response_data.get('new', {}).get('conversation_id')
            if not conversation_id:
                print(color_output('Failed to get conversation ID from response. Aborting further tests.', RED))
                return
        else:
            print(color_output('Failed to get conversation ID. Aborting further tests.', RED))
            return

        # Test conversation stream
        await test_endpoint(session, 'POST', '/ai-conversation-stream', {
            "conversation_id": conversation_id,
            "user_message": "Analyze potential vulnerabilities in a microservices architecture using containerization.",
            "image_url": None
        })

        test_cases = [
            {'method': 'POST', 'endpoint': '/ai-prompt', 'data': {
                "items": [{
                    "question": "Generate a comprehensive checklist for securing cloud-native applications against common attack vectors.",
                    "response": ""
                }]
            }},
            {'method': 'POST', 'endpoint': '/ai-summary', 'data': {
                "items": [{
                    "question": "Summarize the impact of a sophisticated supply chain attack targeting multiple Fortune 500 companies.",
                    "response": ""
                }]
            }},
            {'method': 'POST', 'endpoint': '/ai-tags', 'data': {
                "items": [{
                    "question": "Extract relevant tags from a report on a major ransomware attack targeting healthcare institutions.",
                    "response": ""
                }]
            }},
            {'method': 'POST', 'endpoint': '/ai-title', 'data': {
                "items": [{
                    "question": "Generate a title for an event describing a large-scale DDoS attack on critical infrastructure.",
                    "response": ""
                }]
            }},
            {'method': 'GET', 'endpoint': '/personas'},
            {'method': 'GET', 'endpoint': '/settings'},
            {'method': 'GET', 'endpoint': '/registry'},
            {'method': 'POST', 'endpoint': '/registry', 'data': {
                "name": "Advanced Persistent Threat (APT) Detection Framework",
                "description": "A comprehensive framework for identifying and mitigating APT activities within enterprise networks.",
                "tags": ["APT", "Threat Detection", "Network Security"],
                "items": [
                    {"name": "Network Traffic Analysis Module", "description": "AI-powered anomaly detection in network traffic patterns."},
                    {"name": "Endpoint Behavior Monitoring", "description": "Continuous analysis of endpoint activities for suspicious behavior."},
                    {"name": "Threat Intelligence Integration", "description": "Real-time integration with global threat intelligence feeds."}
                ],
                "tenantId": TENANT_ID
            }},
            {'method': 'GET', 'endpoint': '/session'},
            {'method': 'POST', 'endpoint': '/session', 'data': {
                "sessionName": "Zero-Trust Architecture Implementation",
                "owner": OWNER_ID,
                "dataItems": [
                    {
                        "prompt": "What are the key components of a zero-trust architecture?",
                        "response": "",
                        "isDone": True
                    }
                ],
                "tenantIds": [TENANT_ID]
            }},
            {'method': 'GET', 'endpoint': '/trending'},
            {'method': 'POST', 'endpoint': '/trending', 'data': {
                "prompt": "Analyze the potential cybersecurity implications of quantum computing on current encryption standards.",
                "order": 1,
                "favorited": True
            }}
        ]

        created_session_id = None
        created_trending_id = None

        for test_case in test_cases:
            result, response_data = await test_endpoint(session, test_case['method'], test_case['endpoint'], test_case.get('data'))
            if test_case['endpoint'] == '/session' and test_case['method'] == 'POST':
                if response_data and 'id' in response_data:
                    created_session_id = response_data['id']
            elif test_case['endpoint'] == '/trending' and test_case['method'] == 'POST':
                if response_data and 'id' in response_data:
                    created_trending_id = response_data['id']

        # Clean up created resources
        if created_session_id:
            print("\nCleaning up created session...")
            await test_endpoint(session, 'DELETE', f'/session?id={created_session_id}')

        if created_trending_id:
            print("\nCleaning up created trending prompt...")
            await test_endpoint(session, 'DELETE', f'/trending?id={created_trending_id}')

if __name__ == "__main__":
    asyncio.run(run_tests())