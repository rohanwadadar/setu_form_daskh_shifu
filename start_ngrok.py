from pyngrok import ngrok, conf
import time
import sys

# Setup authtoken
conf.get_default().auth_token = '31d0d1At5CwUZtq7aJEogKGmkq7_5oypsDJSxcAkD39oKw87B'

print("Starting ngrok tunnels...")
try:
    # Connect tunnels
    t1 = ngrok.connect(5000, "http")
    t2 = ngrok.connect(5001, "http")

    print(f"DASKFORM_URL: {t1.public_url}")
    print(f"SHIFU_URL: {t2.public_url}")
    
    # Keep alive
    while True:
        time.sleep(1)
except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)
