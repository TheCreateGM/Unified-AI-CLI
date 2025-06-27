#!/usr/bin/env python3
"""
Deep Thinking Brain - Unified AI CLI
Combines Mistral AI, Gemini, and Claude into one intelligent system
"""

import os
import sys
import json
import yaml
import click
import asyncio
import requests
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime
from dotenv import load_dotenv

# Rich for beautiful output
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from rich.prompt import Prompt, Confirm
from rich.progress import Progress, SpinnerColumn, TextColumn

# AI Provider imports
import google.generativeai as genai
import anthropic

# Load environment variables
load_dotenv()

console = Console()

class Config:
    """Configuration management for the AI CLI"""
    
    def __init__(self):
        self.config_file = Path("config.yaml")
        self.history_dir = Path.home() / ".brain-cli"
        self.history_dir.mkdir(exist_ok=True)
        self.load_config()
        self.setup_providers()
    
    def load_config(self):
        """Load configuration from YAML file"""
        if self.config_file.exists():
            with open(self.config_file, 'r') as f:
                self.config = yaml.safe_load(f)
        else:
            self.config = self.get_default_config()
            self.save_config()
    
    def save_config(self):
        """Save configuration to YAML file"""
        with open(self.config_file, 'w') as f:
            yaml.dump(self.config, f, default_flow_style=False)
    
    def get_default_config(self):
        """Get default configuration"""
        return {
            'default_provider': 'mistral',
            'default_model': 'mistral-large-latest',
            'max_tokens': 4096,
            'temperature': 0.7,
            'history_enabled': True,
            'output_format': 'markdown'
        }
    
    def setup_providers(self):
        """Setup API clients for all providers"""
        # Mistral AI
        self.mistral_api_key = os.getenv('MISTRAL_API_KEY')
        if not self.mistral_api_key:
            console.print("[red]Warning: MISTRAL_API_KEY not found in environment[/red]")
        
        # Gemini
        gemini_key = os.getenv('GEMINI_API_KEY')
        if gemini_key:
            genai.configure(api_key=gemini_key)
        else:
            console.print("[red]Warning: GEMINI_API_KEY not found in environment[/red]")
        
        # Anthropic
        anthropic_key = os.getenv('ANTHROPIC_API_KEY')
        if anthropic_key:
            self.anthropic_client = anthropic.Anthropic(api_key=anthropic_key)
        else:
            console.print("[red]Warning: ANTHROPIC_API_KEY not found in environment[/red]")
            self.anthropic_client = None

class HistoryManager:
    """Manage conversation history across sessions"""
    
    def __init__(self, history_dir: Path):
        self.history_dir = history_dir
        self.current_thread = "default"
        self.history_file = self.history_dir / f"{self.current_thread}.json"
    
    def set_thread(self, thread_name: str):
        """Set the current conversation thread"""
        self.current_thread = thread_name
        self.history_file = self.history_dir / f"{thread_name}.json"
    
    def load_history(self) -> List[Dict]:
        """Load conversation history for current thread"""
        if self.history_file.exists():
            with open(self.history_file, 'r') as f:
                return json.load(f)
        return []
    
    def save_history(self, history: List[Dict]):
        """Save conversation history for current thread"""
        with open(self.history_file, 'w') as f:
            json.dump(history, f, indent=2)
    
    def add_message(self, role: str, content: str, provider: str = None):
        """Add a message to the current thread history"""
        history = self.load_history()
        message = {
            'role': role,
            'content': content,
            'provider': provider,
            'timestamp': datetime.now().isoformat()
        }
        history.append(message)
        self.save_history(history)
    
    def get_context_messages(self, max_messages: int = 10) -> List[Dict]:
        """Get recent messages for context"""
        history = self.load_history()
        return history[-max_messages:] if history else []

class AIProvider:
    """Base class for AI providers"""
    
    def __init__(self, config: Config):
        self.config = config
    
    async def generate_response(self, prompt: str, context: List[Dict] = None) -> Dict:
        """Generate response from AI provider"""
        raise NotImplementedError

class MistralProvider(AIProvider):
    """Mistral AI provider"""
    
    async def generate_response(self, prompt: str, context: List[Dict] = None) -> Dict:
        try:
            if not self.config.mistral_api_key:
                return {
                    'content': "Mistral API key not configured",
                    'provider': 'mistral',
                    'error': True
                }
            
            # Prepare messages for Mistral API
            messages = []
            
            # Add context messages
            if context:
                for msg in context:
                    if msg['role'] in ['user', 'assistant']:
                        messages.append({
                            'role': msg['role'],
                            'content': msg['content']
                        })
            
            # Add current prompt
            messages.append({'role': 'user', 'content': prompt})
            
            # Prepare request payload
            payload = {
                'model': self.config.config['default_model'],
                'messages': messages,
                'max_tokens': self.config.config['max_tokens'],
                'temperature': self.config.config['temperature'],
                'top_p': self.config.config.get('top_p', 1.0),
                'stream': False
            }
            
            # Make API request
            headers = {
                'Authorization': f'Bearer {self.config.mistral_api_key}',
                'Content-Type': 'application/json'
            }
            
            response = requests.post(
                'https://api.mistral.ai/v1/chat/completions',
                headers=headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                return {
                    'content': data['choices'][0]['message']['content'],
                    'provider': 'mistral',
                    'model': self.config.config['default_model'],
                    'usage': data.get('usage', {})
                }
            else:
                return {
                    'content': f"Mistral API error: {response.status_code} - {response.text}",
                    'provider': 'mistral',
                    'error': True
                }
                
        except Exception as e:
            return {
                'content': f"Error with Mistral: {str(e)}",
                'provider': 'mistral',
                'error': True
            }

class GeminiProvider(AIProvider):
    """Google Gemini provider"""
    
    async def generate_response(self, prompt: str, context: List[Dict] = None) -> Dict:
        try:
            model = genai.GenerativeModel('gemini-pro')
            
            # Build context
            full_prompt = prompt
            if context:
                context_text = "\n".join([
                    f"{msg['role']}: {msg['content']}" 
                    for msg in context[-5:]  # Last 5 messages for context
                ])
                full_prompt = f"Context:\n{context_text}\n\nCurrent question: {prompt}"
            
            response = await model.generate_content_async(full_prompt)
            
            return {
                'content': response.text,
                'provider': 'gemini',
                'model': 'gemini-pro',
                'usage': None
            }
        except Exception as e:
            return {
                'content': f"Error with Gemini: {str(e)}",
                'provider': 'gemini',
                'error': True
            }

class ClaudeProvider(AIProvider):
    """Anthropic Claude provider"""
    
    async def generate_response(self, prompt: str, context: List[Dict] = None) -> Dict:
        try:
            if not self.config.anthropic_client:
                return {
                    'content': "Anthropic API key not configured",
                    'provider': 'claude',
                    'error': True
                }
            
            messages = []
            
            # Add context messages
            if context:
                for msg in context:
                    if msg['role'] in ['user', 'assistant']:
                        messages.append({
                            'role': msg['role'],
                            'content': msg['content']
                        })
            
            # Add current prompt
            messages.append({'role': 'user', 'content': prompt})
            
            response = await self.config.anthropic_client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=self.config.config['max_tokens'],
                temperature=self.config.config['temperature'],
                messages=messages
            )
            
            return {
                'content': response.content[0].text,
                'provider': 'claude',
                'model': 'claude-3-sonnet-20240229',
                'usage': {
                    'input_tokens': response.usage.input_tokens,
                    'output_tokens': response.usage.output_tokens
                } if hasattr(response, 'usage') else None
            }
        except Exception as e:
            return {
                'content': f"Error with Claude: {str(e)}",
                'provider': 'claude',
                'error': True
            }

class DeepThinkingBrain:
    """Main class that combines multiple AI providers"""
    
    def __init__(self):
        self.config = Config()
        self.history = HistoryManager(self.config.history_dir)
        self.providers = {
            'mistral': MistralProvider(self.config),
            'gemini': GeminiProvider(self.config),
            'claude': ClaudeProvider(self.config)
        }
    
    async def generate_response(self, prompt: str, provider: str = None, 
                              use_deep_thinking: bool = False) -> Dict:
        """Generate response using specified provider or deep thinking mode"""
        
        if use_deep_thinking:
            return await self.deep_thinking_mode(prompt)
        
        if provider and provider in self.providers:
            return await self.providers[provider].generate_response(
                prompt, self.history.get_context_messages()
            )
        
        # Use default provider
        default_provider = self.config.config['default_provider']
        return await self.providers[default_provider].generate_response(
            prompt, self.history.get_context_messages()
        )
    
    async def deep_thinking_mode(self, prompt: str) -> Dict:
        """Combine insights from multiple AI providers"""
        console.print("\n[bold blue]🧠 Deep Thinking Mode[/bold blue]")
        console.print("Analyzing with multiple AI providers...\n")
        
        # Get responses from all providers
        tasks = []
        for provider_name in ['mistral', 'gemini', 'claude']:
            if provider_name in self.providers:
                task = self.providers[provider_name].generate_response(
                    prompt, self.history.get_context_messages()
                )
                tasks.append((provider_name, task))
        
        # Execute all requests concurrently
        responses = {}
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            for provider_name, task in tasks:
                progress.add_task(f"Getting response from {provider_name}...", total=None)
                response = await task
                responses[provider_name] = response
                progress.update(progress.task_ids[-1], completed=True)
        
        # Display individual responses
        for provider_name, response in responses.items():
            if not response.get('error'):
                console.print(f"\n[bold]{provider_name.upper()} Response:[/bold]")
                console.print(Panel(response['content'], title=provider_name.title()))
        
        # Create synthesis using Mistral (most reliable for this task)
        synthesis_prompt = f"""
        Analyze the following responses from different AI models and provide a comprehensive synthesis:

        Question: {prompt}

        Responses:
        {json.dumps(responses, indent=2)}

        Please provide a well-reasoned synthesis that combines the best insights from each perspective.
        """
        
        synthesis = await self.providers['mistral'].generate_response(synthesis_prompt)
        
        return {
            'content': synthesis['content'],
            'provider': 'deep_thinking',
            'model': 'multi-provider-synthesis',
            'individual_responses': responses
        }
    
    def display_response(self, response: Dict, show_details: bool = True):
        """Display the AI response with formatting"""
        if response.get('error'):
            console.print(f"[red]Error: {response['content']}[/red]")
            return
        
        # Display main response
        console.print("\n[bold green]🤖 AI Response:[/bold green]")
        
        if response['provider'] == 'deep_thinking':
            console.print(Panel(
                Markdown(response['content']),
                title="🧠 Deep Thinking Synthesis",
                border_style="blue"
            ))
        else:
            console.print(Panel(
                Markdown(response['content']),
                title=f"{response['provider'].title()} ({response['model']})",
                border_style="green"
            ))
        
        # Show details if requested
        if show_details and response.get('usage'):
            usage = response['usage']
            console.print(f"\n[dim]Tokens used: {usage.get('total_tokens', 'N/A')}[/dim]")
    
    async def interactive_mode(self):
        """Run interactive chat mode"""
        console.print("[bold blue]🧠 Deep Thinking Brain - Interactive Mode[/bold blue]")
        console.print("Type 'quit' to exit, 'help' for commands\n")
        
        while True:
            try:
                user_input = Prompt.ask("\n[bold cyan]You[/bold cyan]")
                
                if user_input.lower() in ['quit', 'exit', 'q']:
                    break
                elif user_input.lower() == 'help':
                    self.show_help()
                    continue
                elif user_input.lower().startswith('/'):
                    await self.handle_command(user_input)
                    continue
                
                # Generate response
                response = await self.generate_response(user_input)
                self.display_response(response)
                
                # Save to history
                self.history.add_message('user', user_input)
                self.history.add_message('assistant', response['content'], response['provider'])
                
            except KeyboardInterrupt:
                break
            except Exception as e:
                console.print(f"[red]Error: {str(e)}[/red]")
        
        console.print("\n[green]Goodbye! 👋[/green]")
    
    def show_help(self):
        """Show interactive mode help"""
        help_text = """
        [bold]Available Commands:[/bold]
        • /deep <question> - Use deep thinking mode
        • /provider <name> - Switch provider (mistral, gemini, claude)
        • /thread <name> - Switch conversation thread
        • /history - Show conversation history
        • /config - Show current configuration
        • help - Show this help
        • quit - Exit interactive mode
        """
        console.print(Panel(help_text, title="Help", border_style="yellow"))
    
    async def handle_command(self, command: str):
        """Handle interactive mode commands"""
        parts = command.split(' ', 1)
        cmd = parts[0][1:]  # Remove leading /
        args = parts[1] if len(parts) > 1 else ""
        
        if cmd == 'deep':
            response = await self.generate_response(args, use_deep_thinking=True)
            self.display_response(response)
        elif cmd == 'provider':
            if args in self.providers:
                self.config.config['default_provider'] = args
                console.print(f"[green]Switched to {args} provider[/green]")
            else:
                console.print(f"[red]Unknown provider: {args}[/red]")
        elif cmd == 'thread':
            self.history.set_thread(args)
            console.print(f"[green]Switched to thread: {args}[/green]")
        elif cmd == 'history':
            history = self.history.load_history()
            if history:
                table = Table(title=f"Conversation History - {self.history.current_thread}")
                table.add_column("Time", style="dim")
                table.add_column("Role", style="cyan")
                table.add_column("Content", style="white")
                table.add_column("Provider", style="green")
                
                for msg in history[-10:]:  # Show last 10 messages
                    table.add_row(
                        msg['timestamp'][:19],
                        msg['role'],
                        msg['content'][:100] + "..." if len(msg['content']) > 100 else msg['content'],
                        msg.get('provider', 'N/A')
                    )
                console.print(table)
            else:
                console.print("[yellow]No conversation history[/yellow]")
        elif cmd == 'config':
            console.print(Panel(
                yaml.dump(self.config.config, default_flow_style=False),
                title="Current Configuration"
            ))

@click.command()
@click.argument('prompt', required=False)
@click.option('--provider', '-p', type=click.Choice(['mistral', 'gemini', 'claude']), 
              help='Specify AI provider')
@click.option('--deep', '-d', is_flag=True, help='Use deep thinking mode')
@click.option('--interactive', '-i', is_flag=True, help='Start interactive mode')
@click.option('--thread', '-t', default='default', help='Conversation thread name')
@click.option('--output', '-o', help='Save output to file')
@click.option('--model', '-m', help='Specify model to use')
@click.option('--temperature', '-temp', type=float, help='Set temperature')
@click.option('--max-tokens', type=int, help='Set max tokens')
def main(prompt, provider, deep, interactive, thread, output, model, temperature, max_tokens):
    """Deep Thinking Brain - Unified AI CLI"""
    
    # Initialize the brain
    brain = DeepThinkingBrain()
    
    # Set thread
    brain.history.set_thread(thread)
    
    # Override config if specified
    if model:
        brain.config.config['default_model'] = model
    if temperature:
        brain.config.config['temperature'] = temperature
    if max_tokens:
        brain.config.config['max_tokens'] = max_tokens
    
    async def run():
        if interactive:
            await brain.interactive_mode()
        elif prompt:
            # Generate response
            response = await brain.generate_response(prompt, provider, deep)
            
            # Display response
            brain.display_response(response)
            
            # Save to history
            brain.history.add_message('user', prompt)
            brain.history.add_message('assistant', response['content'], response['provider'])
            
            # Save to file if requested
            if output:
                with open(output, 'w') as f:
                    f.write(f"Question: {prompt}\n\n")
                    f.write(f"Response: {response['content']}\n")
                console.print(f"[green]Response saved to {output}[/green]")
        else:
            console.print("[red]Please provide a prompt or use --interactive mode[/red]")
    
    # Run the async function
    asyncio.run(run())

if __name__ == '__main__':
    main() 