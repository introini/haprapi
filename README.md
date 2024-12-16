# HAPrapi

HAPrapi is a Python library for interacting with HAProxy's runtime API. It provides a simple and intuitive interface to manage and monitor HAProxy instances programmatically.

## Features

- Connect to HAProxy's runtime API
- Retrieve HAProxy information and statistics
- Manage backend servers (enable/disable)
- Manage frontends (enable/disable)
- Parse and structure HAProxy data

## Installation

To install HAPrapi, run the following command:

```bash
pip install haprapi
```

## Usage

Here are some basic examples of how to use HAPrapi:

### Get HAProxy Host information
```python
from haprapi import Client

# Initialize the client
client = Client('localhost', 9999)

info = client.get_info()
print(info)
```
### Get statistics
```python
from haprapi import Client

# Initialize the client
client = Client('localhost', 9999)

stats = client.get_stat()
print(stats)
```
### Enable a server
```python
from haprapi import Client

# Initialize the client
client = Client('localhost', 9999)

client.enable_server('backend_name', 'server_name')
```

### Disable a frontend
```python
from haprapi import Client

# Initialize the client
client = Client('localhost', 9999)

client.disable_frontend('frontend_name')
```

## Documentation

For detailed documentation, please refer to the docstrings in the source code.

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

## License
This project is open source and available under the GPL-3.0 License.
