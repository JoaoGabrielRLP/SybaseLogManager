sh
#!/bin/bash

echo "Creating virtual environment..."
python3 -m venv venv

echo "Activating virtual environment..."
source venv/bin/activate

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Installation complete. To run the application, activate the virtual environment with:"
echo "source venv/bin/activate"
echo "Then run:"
echo "python log_application.py"