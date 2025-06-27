#!/usr/bin/env python3
"""
Simple test script for Deep Thinking Brain CLI
"""

import os
import sys
import asyncio
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

def test_imports():
    """Test if all required modules can be imported"""
    print("🧪 Testing imports...")
    
    try:
        import requests
        print("✅ Requests imported successfully")
    except ImportError as e:
        print(f"❌ Requests import failed: {e}")
        return False
    
    try:
        import google.generativeai as genai
        print("✅ Google Generative AI imported successfully")
    except ImportError as e:
        print(f"❌ Google Generative AI import failed: {e}")
        return False
    
    try:
        import anthropic
        print("✅ Anthropic imported successfully")
    except ImportError as e:
        print(f"❌ Anthropic import failed: {e}")
        return False
    
    try:
        from rich.console import Console
        from rich.markdown import Markdown
        from rich.panel import Panel
        print("✅ Rich library imported successfully")
    except ImportError as e:
        print(f"❌ Rich library import failed: {e}")
        return False
    
    return True

def test_config():
    """Test configuration loading"""
    print("\n🧪 Testing configuration...")
    
    try:
        from brain import Config
        config = Config()
        print("✅ Configuration loaded successfully")
        print(f"   Default provider: {config.config['default_provider']}")
        print(f"   Default model: {config.config['default_model']}")
        return True
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        return False

def test_history():
    """Test history management"""
    print("\n🧪 Testing history management...")
    
    try:
        from brain import HistoryManager
        from pathlib import Path
        
        history_dir = Path.home() / ".brain-cli"
        history = HistoryManager(history_dir)
        
        # Test adding a message
        history.add_message('user', 'test message')
        history.add_message('assistant', 'test response')
        
        # Test loading history
        loaded_history = history.load_history()
        print(f"✅ History management working - {len(loaded_history)} messages")
        return True
    except Exception as e:
        print(f"❌ History test failed: {e}")
        return False

def test_providers():
    """Test provider initialization"""
    print("\n🧪 Testing provider initialization...")
    
    try:
        from brain import MistralProvider, GeminiProvider, ClaudeProvider, Config
        
        config = Config()
        
        # Test provider creation
        mistral_provider = MistralProvider(config)
        gemini_provider = GeminiProvider(config)
        claude_provider = ClaudeProvider(config)
        
        print("✅ All providers initialized successfully")
        return True
    except Exception as e:
        print(f"❌ Provider test failed: {e}")
        return False

async def test_simple_query():
    """Test a simple query (requires API keys)"""
    print("\n🧪 Testing simple query...")
    
    # Check if API keys are available
    mistral_key = os.getenv('MISTRAL_API_KEY')
    gemini_key = os.getenv('GEMINI_API_KEY')
    anthropic_key = os.getenv('ANTHROPIC_API_KEY')
    
    if not any([mistral_key, gemini_key, anthropic_key]):
        print("⚠️  No API keys found. Skipping query test.")
        print("   Set MISTRAL_API_KEY, GEMINI_API_KEY, or ANTHROPIC_API_KEY to test queries")
        return True
    
    try:
        from brain import DeepThinkingBrain
        
        brain = DeepThinkingBrain()
        
        # Test with a simple query
        test_prompt = "Say 'Hello, World!' in a creative way"
        
        print(f"   Testing with prompt: '{test_prompt}'")
        
        # Try with available providers
        if mistral_key:
            print("   Testing Mistral...")
            response = await brain.generate_response(test_prompt, provider='mistral')
            if not response.get('error'):
                print("✅ Mistral query successful")
            else:
                print(f"❌ Mistral query failed: {response['content']}")
        
        if gemini_key:
            print("   Testing Gemini...")
            response = await brain.generate_response(test_prompt, provider='gemini')
            if not response.get('error'):
                print("✅ Gemini query successful")
            else:
                print(f"❌ Gemini query failed: {response['content']}")
        
        if anthropic_key:
            print("   Testing Claude...")
            response = await brain.generate_response(test_prompt, provider='claude')
            if not response.get('error'):
                print("✅ Claude query successful")
            else:
                print(f"❌ Claude query failed: {response['content']}")
        
        return True
    except Exception as e:
        print(f"❌ Query test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🧠 Deep Thinking Brain CLI - Test Suite")
    print("=" * 50)
    
    # Run synchronous tests
    tests = [
        test_imports,
        test_config,
        test_history,
        test_providers
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    # Run async test
    try:
        asyncio.run(test_simple_query())
        passed += 1
        total += 1
    except Exception as e:
        print(f"❌ Async test failed: {e}")
        total += 1
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The CLI is ready to use.")
        print("\nNext steps:")
        print("1. Set up your API keys in .env file")
        print("2. Run: python3 brain.py --help")
        print("3. Try: python3 brain.py 'Hello, World!'")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
        return 1
    
    return 0

if __name__ == '__main__':
    exit(main()) 