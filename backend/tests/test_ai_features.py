"""
AI Features Integration Tests

Test all AI endpoints to ensure they work correctly with Ollama.
These tests require a running FastAPI server and Ollama.

Run with:
    pytest tests/test_ai_features.py -v
    pytest tests/test_ai_features.py::test_ai_rephrase -v
    pytest tests/test_ai_features.py -v -s  # with output
"""

import pytest
import time
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from pkm_backend.main import app
from pkm_backend.models.database import Note as NoteModel, Workspace as WorkspaceModel


@pytest.fixture
def ai_test_note(db_session: Session, sample_workspace):
    """Create a test note for AI operations"""
    note = NoteModel(
        title="Test Note for AI",
        content="this note has bad grammar and poor structure. it needs improvement badly!! the algorithm is slow and buggy.",
        workspace_id=sample_workspace.id
    )
    db_session.add(note)
    db_session.commit()
    db_session.refresh(note)
    return note


class TestAIRephrase:
    """Test AI text rephrasing functionality"""
    
    def test_ai_rephrase_academic_style(self, client: TestClient):
        """Test AI rephrase with academic style"""
        request_data = {
            "text": "This code is buggy and needs fixing badly",
            "style": "academic"
        }
        
        start_time = time.time()
        response = client.post("/api/v1/ai/rephrase", json=request_data)
        response_time = time.time() - start_time
        
        assert response.status_code == 200
        data = response.json()
        
        # Verify response structure
        assert "success" in data
        assert "response" in data
        assert "model_used" in data
        assert "processing_time_ms" in data
        
        # Verify success
        assert data["success"] is True
        assert data["response"] != ""
        assert data["model_used"] == "llama3.2:1b"
        
        # Verify response quality (should be different from input)
        assert data["response"] != request_data["text"]
        assert len(data["response"]) > 10  # Should be substantial
        
        # Performance check (should be reasonable)
        assert response_time < 30  # Should complete within 30 seconds
        
        print(f"\n✅ Academic Rephrase Test:")
        print(f"   Input: {request_data['text']}")
        print(f"   Output: {data['response'][:100]}...")
        print(f"   Response Time: {response_time:.2f}s")
    
    def test_ai_rephrase_professional_style(self, client: TestClient):
        """Test AI rephrase with formal style"""
        request_data = {
            "text": "The algorithm sucks and is really slow",
            "style": "formal"
        }
        
        response = client.post("/api/v1/ai/rephrase", json=request_data)
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["success"] is True
        assert data["response"] != request_data["text"]
        assert "llama3.2" in data["model_used"]
        
        print(f"\n✅ Formal Rephrase Test:")
        print(f"   Input: {request_data['text']}")
        print(f"   Output: {data['response'][:100]}...")
    
    def test_ai_rephrase_casual_style(self, client: TestClient):
        """Test AI rephrase with casual style"""
        request_data = {
            "text": "The implementation demonstrates suboptimal performance characteristics",
            "style": "casual"
        }
        
        response = client.post("/api/v1/ai/rephrase", json=request_data)
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["success"] is True
        assert data["response"] != request_data["text"]
        
    def test_ai_rephrase_empty_text(self, client: TestClient):
        """Test AI rephrase with empty text should return validation error"""
        request_data = {
            "text": "",
            "style": "academic"
        }
        
        response = client.post("/api/v1/ai/rephrase", json=request_data)
        
        # Should return 422 validation error for empty text
        assert response.status_code == 422
        
        print(f"\n✅ Empty Text Validation Test: Got expected 422 error")


class TestAIChat:
    """Test AI chat functionality"""
    
    def test_ai_chat_general_question(self, client: TestClient):
        """Test AI chat with general question"""
        request_data = {
            "message": "What is Big O notation and why is it important?",
            "note_ids": []
        }
        
        start_time = time.time()
        response = client.post("/api/v1/ai/chat", json=request_data)
        response_time = time.time() - start_time
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["success"] is True
        assert data["response"] != ""
        assert "big o" in data["response"].lower() or "complexity" in data["response"].lower()
        
        print(f"\n✅ General Chat Test:")
        print(f"   Question: {request_data['message']}")
        print(f"   Answer: {data['response'][:150]}...")
        print(f"   Response Time: {response_time:.2f}s")
    
    def test_ai_chat_with_note_context(self, client: TestClient, ai_test_note):
        """Test AI chat with note context"""
        request_data = {
            "message": "What are the main issues mentioned in this note?",
            "note_ids": [ai_test_note.id]
        }
        
        response = client.post("/api/v1/ai/chat", json=request_data)
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["success"] is True
        assert data["response"] != ""
        
        print(f"\n✅ Chat with Context Test:")
        print(f"   Note Content: {ai_test_note.content}")
        print(f"   Question: {request_data['message']}")
        print(f"   Answer: {data['response'][:150]}...")
    
    def test_ai_chat_technical_question(self, client: TestClient):
        """Test AI chat with technical programming question"""
        request_data = {
            "message": "Explain the difference between stack and heap memory",
            "note_ids": []
        }
        
        response = client.post("/api/v1/ai/chat", json=request_data)
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["success"] is True
        assert data["response"] != ""
        # Should mention relevant concepts
        response_lower = data["response"].lower()
        assert any(term in response_lower for term in ["stack", "heap", "memory", "allocation"])


class TestAICleanup:
    """Test AI note cleanup functionality"""
    
    def test_ai_cleanup_note(self, client: TestClient, ai_test_note):
        """Test AI cleanup of a note"""
        request_data = {
            "note_id": ai_test_note.id,
            "cleanup_type": "full"
        }
        
        start_time = time.time()
        response = client.post("/api/v1/ai/cleanup", json=request_data)
        response_time = time.time() - start_time
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["success"] is True
        assert data["response"] != ""
        assert data["response"] != ai_test_note.content  # Should be different
        
        print(f"\n✅ Note Cleanup Test:")
        print(f"   Original: {ai_test_note.content}")
        print(f"   Cleaned: {data['response'][:150]}...")
        print(f"   Response Time: {response_time:.2f}s")
    
    def test_ai_cleanup_grammar_focus(self, client: TestClient, ai_test_note):
        """Test AI cleanup with grammar focus"""
        request_data = {
            "note_id": ai_test_note.id,
            "cleanup_type": "grammar"
        }
        
        response = client.post("/api/v1/ai/cleanup", json=request_data)
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["success"] is True
        assert data["response"] != ""
    
    def test_ai_cleanup_nonexistent_note(self, client: TestClient):
        """Test AI cleanup with non-existent note ID"""
        request_data = {
            "note_id": 99999,
            "cleanup_type": "full"
        }
        
        response = client.post("/api/v1/ai/cleanup", json=request_data)
        
        assert response.status_code == 404  # Should fail gracefully


class TestAIPerformance:
    """Test AI performance and reliability"""
    
    def test_ai_response_times(self, client: TestClient):
        """Test that AI responses are within acceptable time limits"""
        test_cases = [
            {"endpoint": "/api/v1/ai/rephrase", "data": {"text": "Quick test", "style": "academic"}},
            {"endpoint": "/api/v1/ai/chat", "data": {"message": "Hello", "note_ids": []}},
        ]
        
        for case in test_cases:
            start_time = time.time()
            response = client.post(case["endpoint"], json=case["data"])
            response_time = time.time() - start_time
            
            assert response.status_code == 200
            data = response.json()
            assert data["success"] is True
            
            # Performance assertion - should complete within reasonable time
            assert response_time < 15  # 15 seconds max for quick tests
            
            print(f"\n⏱️  Performance Test - {case['endpoint']}: {response_time:.2f}s")
    
    def test_ai_concurrent_requests(self, client: TestClient):
        """Test AI can handle multiple requests (basic concurrency test)"""
        import threading
        import queue
        
        results = queue.Queue()
        
        def make_request():
            try:
                response = client.post("/api/v1/ai/rephrase", json={
                    "text": "Test concurrent request",
                    "style": "academic"
                })
                results.put(response.status_code == 200)
            except Exception:
                results.put(False)
        
        # Start multiple threads
        threads = []
        for _ in range(3):  # Test with 3 concurrent requests
            thread = threading.Thread(target=make_request)
            threads.append(thread)
            thread.start()
        
        # Wait for all to complete
        for thread in threads:
            thread.join(timeout=30)  # 30 second timeout
        
        # Check results
        success_count = 0
        while not results.empty():
            if results.get():
                success_count += 1
        
        # At least 2 out of 3 should succeed (allowing for some potential issues)
        assert success_count >= 2
        
        print(f"\n🔄 Concurrency Test: {success_count}/3 requests succeeded")


class TestAIErrorHandling:
    """Test AI error handling and edge cases"""
    
    def test_ai_with_server_down(self, client: TestClient, monkeypatch):
        """Test AI behavior when Ollama server is unreachable"""
        # Mock the Ollama service to simulate server down
        from pkm_backend.services.ollama import ollama_service
        
        async def mock_failing_generate(*args, **kwargs):
            raise Exception("Connection refused")
        
        monkeypatch.setattr(ollama_service, "generate", mock_failing_generate)
        
        response = client.post("/api/v1/ai/rephrase", json={
            "text": "Test text",
            "style": "academic"
        })
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is False
        assert "error" in data
    
    def test_ai_with_invalid_model(self, client: TestClient, monkeypatch):
        """Test AI behavior with invalid model configuration"""
        # This would require mocking the model configuration
        # For now, just ensure the current model works
        response = client.post("/api/v1/ai/rephrase", json={
            "text": "Test text",
            "style": "academic"
        })
        
        assert response.status_code == 200
        data = response.json()
        # Should either succeed or fail gracefully
        assert "success" in data


# Test execution information
if __name__ == "__main__":
    print("🤖 AI Features Integration Tests")
    print("================================")
    print("Run with: pytest tests/test_ai_features.py -v -s")
    print("Individual tests: pytest tests/test_ai_features.py::TestAIRephrase::test_ai_rephrase_academic_style -v -s")