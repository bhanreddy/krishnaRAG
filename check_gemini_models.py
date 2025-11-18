"""
Check available Gemini models
"""
import os
import google.generativeai as genai

# Setup API key
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY', 'AIzaSyBT49gqX6QXI9QdPBusoGU76wq8YzCGKb8')

if not GEMINI_API_KEY:
    print("❌ GEMINI_API_KEY not found in environment!")
    exit(1)

genai.configure(api_key=GEMINI_API_KEY)

print("=" * 60)
print("Available Gemini Models")
print("=" * 60)

try:
    models = genai.list_models()
    
    for m in models:
        print(f"\n📌 Model: {m.name}")
        print(f"   Display Name: {m.display_name}")
        print(f"   Supported Methods: {m.supported_generation_methods}")
        print(f"   Description: {m.description}")
        print(f"   Input Token Limit: {m.input_token_limit}")
        print(f"   Output Token Limit: {m.output_token_limit}")
        
        # Check if supports generateContent
        if 'generateContent' in m.supported_generation_methods:
            print(f"   ✅ SUPPORTS generateContent")
        
except Exception as e:
    print(f"❌ Error listing models: {e}")
    print(f"   Make sure GEMINI_API_KEY is valid")

print("\n" + "=" * 60)
print("Testing model initialization...")
print("=" * 60)

model_names_to_test = [
    'gemini-1.5-flash',
    'gemini-1.5-pro',
    'gemini-pro',
    'gemini-2.0-flash'
]

for model_name in model_names_to_test:
    try:
        model = genai.GenerativeModel(model_name)
        # Try a simple generation
        response = model.generate_content("Say 'Hello'", stream=False)
        if response:
            print(f"✅ {model_name}: WORKS")
        else:
            print(f"❌ {model_name}: No response")
    except Exception as e:
        print(f"❌ {model_name}: {str(e)[:80]}")

print("\n" + "=" * 60)
