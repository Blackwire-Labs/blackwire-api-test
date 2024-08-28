# Blackwire API Test Script

This repository contains a Python script for testing the Blackwire API. It provides a comprehensive test suite that covers various endpoints of the Blackwire API, including conversation management, AI-powered analysis, and data operations.

## About Blackwire

Blackwire is a cutting-edge cybersecurity platform that leverages AI to provide advanced threat detection and response capabilities. For more information, visit [blackwirelabs.com](https://blackwirelabs.com).

## Prerequisites

- Python 3.7 or later
- `aiohttp` library

## Setup

1. Clone this repository:
   ```
   git clone https://github.com/blackwirelabs/api-test-script.git
   cd api-test-script
   ```

2. Install the required dependency:
   ```
   pip install aiohttp
   ```

3. Open the `api_test_script.py` file and update the following variables with your Blackwire account information:
   - `API_KEY`: Your API key (client ID and secret)
   - `OWNER_ID`: Your user ID
   - `TENANT_ID`: Your tenant ID

   You can find your client ID and secret in the Blackwire application:
   - Go to [app.blackwire.ai](https://app.blackwire.ai)
   - Navigate to User Profile -> Edit Profile -> Personal Tokens

   To retrieve your `OWNER_ID` and `TENANT_ID`:
   1. Run the script with placeholder values for these IDs.
   2. Look for the response from the `/settings` endpoint in the console output.
   3. In the response, you'll find your `OWNER_ID` (usually labeled as "userId" or similar) and `TENANT_ID`.
   4. Update the script with these values and run it again for a complete test.

## Usage

Run the script using Python:

```
python bwapitest.py
```

The script will test various endpoints of the Blackwire API and display the results in the console. The output is color-coded for easy reading:
- Green: Successful responses (status codes 200, 201, 204)
- Red: Failed responses
- Yellow: Responses that took longer than 1000ms

## API Documentation

For detailed information about the Blackwire API, refer to the [Swagger documentation](https://app.blackwire.ai/swagger).

## Contributing

We welcome contributions to improve this test script. Please feel free to submit issues or pull requests.

## License

Copyright © 2024 Blackwire Labs. All rights reserved.

This script is provided for testing purposes only. Unauthorized distribution or use of this script is strictly prohibited.

## Contact

For any questions or support, please contact [support@blackwirelabs.com](mailto:support@blackwirelabs.com).