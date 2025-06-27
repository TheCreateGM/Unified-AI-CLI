#!/usr/bin/env python3
"""
Demo script for Deep Thinking Brain CLI
Showcases various features and capabilities
"""

import asyncio
import os
from pathlib import Path

# Add current directory to path
import sys
sys.path.insert(0, str(Path(__file__).parent))

from brain import DeepThinkingBrain
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()

async def demo_basic_usage():
    """Demo basic usage with different providers"""
    console.print(Panel("🚀 Basic Usage Demo", style="bold blue"))
    
    brain = DeepThinkingBrain()
    
    # Test questions
    questions = [
        "What is the capital of France?",
        "Explain quantum computing in simple terms",
        "Write a haiku about artificial intelligence"
    ]
    
    providers = ['mistral', 'gemini', 'claude']
    
    for i, question in enumerate(questions, 1):
        console.print(f"\n[bold cyan]Question {i}:[/bold cyan] {question}")
        
        for provider in providers:
            try:
                console.print(f"\n[dim]Using {provider}...[/dim]")
                response = await brain.generate_response(question, provider=provider)
                
                if not response.get('error'):
                    # Show just a preview
                    preview = response['content'][:100] + "..." if len(response['content']) > 100 else response['content']
                    console.print(f"[green]✅ {provider.title()}:[/green] {preview}")
                else:
                    console.print(f"[red]❌ {provider.title()}: {response['content']}[/red]")
                    
            except Exception as e:
                console.print(f"[red]❌ {provider.title()}: Error - {str(e)}[/red]")
        
        console.print("-" * 50)

async def demo_deep_thinking():
    """Demo deep thinking mode"""
    console.print(Panel("🧠 Deep Thinking Mode Demo", style="bold blue"))
    
    brain = DeepThinkingBrain()
    
    complex_question = """
    Compare and contrast the approaches to artificial intelligence taken by:
    1. Mistral AI (Mistral models)
    2. Google (Gemini models) 
    3. Anthropic (Claude models)
    
    Focus on their philosophical differences, technical approaches, and use cases.
    """
    
    console.print(f"[bold cyan]Complex Question:[/bold cyan]")
    console.print(complex_question)
    
    console.print("\n[bold yellow]Deep Thinking Analysis...[/bold yellow]")
    
    try:
        response = await brain.generate_response(complex_question, use_deep_thinking=True)
        
        if not response.get('error'):
            console.print("\n[bold green]🎯 Final Synthesis:[/bold green]")
            console.print(response['content'])
        else:
            console.print(f"[red]❌ Deep thinking failed: {response['content']}[/red]")
            
    except Exception as e:
        console.print(f"[red]❌ Deep thinking error: {str(e)}[/red]")

async def demo_interactive_features():
    """Demo interactive features"""
    console.print(Panel("💬 Interactive Features Demo", style="bold blue"))
    
    brain = DeepThinkingBrain()
    
    # Demo thread management
    console.print("\n[bold cyan]Thread Management:[/bold cyan]")
    
    threads = ['coding', 'research', 'creative']
    for thread in threads:
        brain.history.set_thread(thread)
        brain.history.add_message('user', f'Test message in {thread} thread')
        brain.history.add_message('assistant', f'Response in {thread} thread')
        console.print(f"✅ Created thread: {thread}")
    
    # Show thread info
    console.print("\n[bold cyan]Thread Information:[/bold cyan]")
    table = Table()
    table.add_column("Thread", style="cyan")
    table.add_column("Messages", style="green")
    
    for thread in threads:
        brain.history.set_thread(thread)
        history = brain.history.load_history()
        table.add_row(thread, str(len(history)))
    
    console.print(table)

def demo_configuration():
    """Demo configuration features"""
    console.print(Panel("⚙️ Configuration Demo", style="bold blue"))
    
    from brain import Config
    config = Config()
    
    console.print("\n[bold cyan]Current Configuration:[/bold cyan]")
    
    table = Table()
    table.add_column("Setting", style="cyan")
    table.add_column("Value", style="green")
    
    for key, value in config.config.items():
        if isinstance(value, (list, dict)):
            value = str(value)[:50] + "..." if len(str(value)) > 50 else str(value)
        table.add_row(key, str(value))
    
    console.print(table)

def demo_installation_check():
    """Check if everything is properly installed"""
    console.print(Panel("🔍 Installation Check", style="bold blue"))
    
    # Check Python version
    import sys
    python_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    console.print(f"✅ Python version: {python_version}")
    
    # Check required packages
    required_packages = [
        'requests', 'google.generativeai', 'anthropic', 
        'rich', 'click', 'pyyaml', 'python-dotenv'
    ]
    
    console.print("\n[bold cyan]Required Packages:[/bold cyan]")
    for package in required_packages:
        try:
            __import__(package)
            console.print(f"✅ {package}")
        except ImportError:
            console.print(f"❌ {package} - Not installed")
    
    # Check API keys
    console.print("\n[bold cyan]API Keys:[/bold cyan]")
    api_keys = {
        'Mistral': 'MISTRAL_API_KEY',
        'Gemini': 'GEMINI_API_KEY', 
        'Anthropic': 'ANTHROPIC_API_KEY'
    }
    
    for name, key in api_keys.items():
        if os.getenv(key):
            console.print(f"✅ {name} API key found")
        else:
            console.print(f"⚠️ {name} API key not found")

async def main():
    """Run all demos"""
    console.print("🧠 Deep Thinking Brain CLI - Demo Suite")
    console.print("=" * 60)
    
    # Check installation first
    demo_installation_check()
    
    # Run demos
    demos = [
        demo_configuration,
        demo_interactive_features,
        demo_basic_usage,
        demo_deep_thinking
    ]
    
    for demo in demos:
        try:
            if asyncio.iscoroutinefunction(demo):
                await demo()
            else:
                demo()
        except Exception as e:
            console.print(f"[red]❌ Demo failed: {str(e)}[/red]")
        
        console.print("\n" + "=" * 60)
    
    console.print("\n🎉 Demo complete!")
    console.print("\nTo use the CLI:")
    console.print("  python3 brain.py --help")
    console.print("  python3 brain.py 'Your question here'")
    console.print("  python3 brain.py --interactive")

if __name__ == '__main__':
    asyncio.run(main()) 