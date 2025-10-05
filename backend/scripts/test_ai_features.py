#!/usr/bin/env python3
"""
AI Features Testing Script for PKM Backend

This script automatically tests all AI features to ensure they work correctly.
Run this after making changes to validate AI functionality.

Usage:
    python scripts/test_ai_features.py
    python scripts/test_ai_features.py --verbose
    python scripts/test_ai_features.py --model llama3.2:1b
"""

import asyncio
import json
import time
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import httpx
import argparse
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn, TimeElapsedColumn

console = Console()

@dataclass
class TestResult:
    """Test result data structure"""
    test_name: str
    success: bool
    response_time: float
    model_used: str
    response_length: int
    error: Optional[str] = None
    response_preview: Optional[str] = None


class AITester:
    """Automated AI testing class"""
    
    def __init__(self, base_url: str = "http://localhost:8000", verbose: bool = False):
        self.base_url = base_url
        self.verbose = verbose
        self.results: List[TestResult] = []
        
    async def test_health_check(self) -> bool:
        """Test if the server is running"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.base_url}/health")
                return response.status_code == 200
        except Exception:
            return False
    
    async def test_ai_rephrase(self) -> TestResult:
        """Test AI text rephrasing feature"""
        test_data = {
            "text": "This code is buggy and needs fixing badly",
            "style": "academic"
        }
        
        return await self._make_ai_request(
            endpoint="/api/v1/ai/rephrase",
            data=test_data,
            test_name="AI Rephrase (Academic)"
        )
    
    async def test_ai_rephrase_professional(self) -> TestResult:
        """Test AI rephrasing with professional style"""
        test_data = {
            "text": "The algorithm sucks and is slow",
            "style": "professional"
        }
        
        return await self._make_ai_request(
            endpoint="/api/v1/ai/rephrase",
            data=test_data,
            test_name="AI Rephrase (Professional)"
        )
    
    async def test_ai_chat_general(self) -> TestResult:
        """Test AI chat with general question"""
        test_data = {
            "message": "Explain time complexity in algorithms briefly",
            "note_ids": []
        }
        
        return await self._make_ai_request(
            endpoint="/api/v1/ai/chat",
            data=test_data,
            test_name="AI Chat (General)"
        )
    
    async def test_ai_chat_with_notes(self) -> TestResult:
        """Test AI chat with note context"""
        # First get available notes
        try:
            async with httpx.AsyncClient() as client:
                notes_response = await client.get(f"{self.base_url}/api/v1/notes/")
                notes = notes_response.json()
                note_ids = [note["id"] for note in notes[:2]] if notes else []
        except Exception:
            note_ids = []
        
        test_data = {
            "message": "What are the key concepts mentioned in these notes?",
            "note_ids": note_ids
        }
        
        return await self._make_ai_request(
            endpoint="/api/v1/ai/chat",
            data=test_data,
            test_name="AI Chat (With Notes)"
        )
    
    async def test_ai_cleanup(self) -> TestResult:
        """Test AI note cleanup feature"""
        # First get a note to clean up
        try:
            async with httpx.AsyncClient() as client:
                notes_response = await client.get(f"{self.base_url}/api/v1/notes/")
                notes = notes_response.json()
                if notes:
                    note_id = notes[0]["id"]
                else:
                    # Create a test note if none exist
                    test_note = {
                        "title": "Test Note for AI Cleanup",
                        "content": "this note has bad grammar and poor structure. it needs improvement badly!!",
                        "workspace_id": 1
                    }
                    create_response = await client.post(f"{self.base_url}/api/v1/notes/", json=test_note)
                    if create_response.status_code == 201:
                        note_id = create_response.json()["id"]
                    else:
                        note_id = 1  # Fallback
        except Exception:
            note_id = 1  # Fallback
        
        test_data = {
            "note_id": note_id,
            "instructions": "Improve grammar and make it more professional"
        }
        
        return await self._make_ai_request(
            endpoint="/api/v1/ai/cleanup",
            data=test_data,
            test_name="AI Note Cleanup"
        )
    
    async def _make_ai_request(self, endpoint: str, data: Dict[str, Any], test_name: str) -> TestResult:
        """Make an AI API request and measure performance"""
        start_time = time.time()
        
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    f"{self.base_url}{endpoint}",
                    json=data,
                    headers={"Content-Type": "application/json"}
                )
                
                response_time = time.time() - start_time
                response_data = response.json()
                
                success = response_data.get("success", False)
                model_used = response_data.get("model_used", "unknown")
                ai_response = response_data.get("response", "")
                error = response_data.get("error") if not success else None
                
                # Create preview of response (first 100 chars)
                preview = ai_response[:100] + "..." if len(ai_response) > 100 else ai_response
                
                return TestResult(
                    test_name=test_name,
                    success=success,
                    response_time=response_time,
                    model_used=model_used,
                    response_length=len(ai_response),
                    error=error,
                    response_preview=preview
                )
                
        except Exception as e:
            response_time = time.time() - start_time
            return TestResult(
                test_name=test_name,
                success=False,
                response_time=response_time,
                model_used="unknown",
                response_length=0,
                error=str(e)
            )
    
    async def run_all_tests(self) -> List[TestResult]:
        """Run all AI tests"""
        console.print(Panel.fit("🤖 AI Features Testing Suite", style="bold blue"))
        
        # Check if server is running
        if not await self.test_health_check():
            console.print("[red]❌ Server is not running at http://localhost:8000[/red]")
            console.print("[yellow]Please start the server first: uv run uvicorn pkm_backend.main:app --reload[/yellow]")
            return []
        
        console.print("[green]✅ Server is running[/green]\n")
        
        # Define all tests
        tests = [
            ("AI Rephrase (Academic)", self.test_ai_rephrase),
            ("AI Rephrase (Professional)", self.test_ai_rephrase_professional),
            ("AI Chat (General)", self.test_ai_chat_general),
            ("AI Chat (With Notes)", self.test_ai_chat_with_notes),
            ("AI Note Cleanup", self.test_ai_cleanup),
        ]
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            TimeElapsedColumn(),
            console=console,
        ) as progress:
            
            for test_name, test_func in tests:
                task = progress.add_task(f"Running {test_name}...", total=None)
                
                result = await test_func()
                self.results.append(result)
                
                # Show immediate result
                status = "✅" if result.success else "❌"
                time_str = f"{result.response_time:.2f}s"
                console.print(f"{status} {test_name} ({time_str})")
                
                if self.verbose and result.success and result.response_preview:
                    console.print(f"   Preview: {result.response_preview}", style="dim")
                elif not result.success and result.error:
                    console.print(f"   Error: {result.error}", style="red")
                
                progress.remove_task(task)
        
        return self.results
    
    def generate_report(self) -> None:
        """Generate a detailed test report"""
        if not self.results:
            return
        
        console.print("\n" + "="*60)
        console.print(Panel.fit("📊 AI Testing Report", style="bold green"))
        
        # Summary stats
        total_tests = len(self.results)
        passed_tests = sum(1 for r in self.results if r.success)
        avg_response_time = sum(r.response_time for r in self.results) / total_tests
        
        console.print(f"[bold]Summary:[/bold]")
        console.print(f"  Total Tests: {total_tests}")
        console.print(f"  Passed: {passed_tests}")
        console.print(f"  Failed: {total_tests - passed_tests}")
        console.print(f"  Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        console.print(f"  Average Response Time: {avg_response_time:.2f}s")
        
        # Detailed results table
        table = Table(title="Detailed Results")
        table.add_column("Test", style="cyan")
        table.add_column("Status", justify="center")
        table.add_column("Time (s)", justify="right")
        table.add_column("Model", style="blue")
        table.add_column("Response Length", justify="right")
        table.add_column("Error", style="red")
        
        for result in self.results:
            status = "✅ PASS" if result.success else "❌ FAIL"
            error = result.error[:50] + "..." if result.error and len(result.error) > 50 else (result.error or "")
            
            table.add_row(
                result.test_name,
                status,
                f"{result.response_time:.2f}",
                result.model_used,
                str(result.response_length),
                error
            )
        
        console.print(table)
        
        # Performance insights
        console.print(f"\n[bold]Performance Insights:[/bold]")
        fastest = min(self.results, key=lambda r: r.response_time)
        slowest = max(self.results, key=lambda r: r.response_time)
        
        console.print(f"  Fastest: {fastest.test_name} ({fastest.response_time:.2f}s)")
        console.print(f"  Slowest: {slowest.test_name} ({slowest.response_time:.2f}s)")
        
        # Model usage
        models = set(r.model_used for r in self.results if r.success)
        console.print(f"  Models Used: {', '.join(models)}")


async def main():
    """Main testing function"""
    parser = argparse.ArgumentParser(description="Test AI features of PKM Backend")
    parser.add_argument("--verbose", "-v", action="store_true", help="Show detailed output")
    parser.add_argument("--base-url", default="http://localhost:8000", help="Base URL of the API")
    
    args = parser.parse_args()
    
    tester = AITester(base_url=args.base_url, verbose=args.verbose)
    
    try:
        results = await tester.run_all_tests()
        if results:
            tester.generate_report()
        
        # Exit with appropriate code
        failed_tests = sum(1 for r in results if not r.success)
        exit(failed_tests)
        
    except KeyboardInterrupt:
        console.print("\n[yellow]Testing interrupted by user[/yellow]")
        exit(1)
    except Exception as e:
        console.print(f"\n[red]Testing failed with error: {e}[/red]")
        exit(1)


if __name__ == "__main__":
    asyncio.run(main())