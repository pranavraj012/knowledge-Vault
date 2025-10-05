"""
Development CLI for PKM Backend
"""

import asyncio
import typer
from rich.console import Console
from rich.table import Table

from pkm_backend.services.ollama import ollama_service
from pkm_backend.db.init_db import init_database, reset_database

app = typer.Typer()
console = Console()


@app.command()
def init_db():
    """Initialize the database"""
    init_database()
    console.print("✅ Database initialized", style="green")


@app.command()
def reset_db():
    """Reset the database (WARNING: Deletes all data)"""
    if typer.confirm("This will delete all data. Are you sure?"):
        reset_database()
        console.print("✅ Database reset", style="green")
    else:
        console.print("❌ Database reset cancelled", style="yellow")


@app.command()
def check_ollama():
    """Check Ollama connection and list available models"""
    
    async def _check():
        # Check health
        is_healthy = await ollama_service.check_health()
        
        if not is_healthy:
            console.print("❌ Ollama is not running or not accessible", style="red")
            console.print("Make sure Ollama is installed and running on http://localhost:11434")
            return
        
        console.print("✅ Ollama is running", style="green")
        
        # List models
        try:
            models = await ollama_service.list_models()
            
            if models:
                table = Table(title="Available Models")
                table.add_column("Model Name", style="cyan")
                
                for model in models:
                    table.add_row(model)
                
                console.print(table)
            else:
                console.print("⚠️  No models found. You may need to pull a model:", style="yellow")
                console.print("   ollama pull llama3.2:1b")
                
        except Exception as e:
            console.print(f"❌ Error listing models: {e}", style="red")
    
    asyncio.run(_check())


@app.command()
def test_ai(text: str = "Hello, this is a test message."):
    """Test AI functionality with sample text"""
    
    async def _test():
        try:
            console.print(f"Testing AI with text: '{text}'")
            
            # Test cleanup
            console.print("\n🧹 Testing cleanup...")
            cleaned = await ollama_service.cleanup_text(text)
            console.print(f"Cleaned: {cleaned}")
            
            # Test rephrase
            console.print("\n✏️  Testing rephrase...")
            rephrased = await ollama_service.rephrase_text(text, "academic")
            console.print(f"Rephrased: {rephrased}")
            
            console.print("\n✅ AI tests completed successfully", style="green")
            
        except Exception as e:
            console.print(f"❌ AI test failed: {e}", style="red")
    
    asyncio.run(_test())


@app.command()
def run_server(
    host: str = "localhost",
    port: int = 8000,
    reload: bool = True
):
    """Run the development server"""
    import uvicorn
    
    console.print(f"🚀 Starting PKM Backend server on {host}:{port}")
    
    uvicorn.run(
        "pkm_backend.main:app",
        host=host,
        port=port,
        reload=reload,
        log_level="info"
    )


if __name__ == "__main__":
    app()