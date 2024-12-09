from fastapi.testclient import TestClient
import api
import io
import pandas as pd

# Initialize test client
client = TestClient(api.app)

# def test_health_check():
#     """Test the health check endpoint"""
#     response = client.get("/health")
#     assert response.status_code == 200
#     assert response.json() == {"status": "healthy"}

# def test_analyze_wrong_file():
#     """Test analyzing with wrong file format"""
#     response = client.post(
#         "/analyze",
#         files={"file": ("test.txt", "test content", "text/plain")},
#         data={
#             "prod_info": "test product",
#             "user_position": "Not Selected",
#             "analysis_focus": "Not Selected"
#         }
#     )
#     assert response.status_code == 400
#     assert "Invalid file format" in response.json()["detail"]

# def test_analyze_valid_file():
#     """Test analyzing with valid Excel file"""
#     # Create a valid Excel file
#     df = pd.DataFrame({
#         'user_id': ['user1'],
#         'date': ['2024-01-01'],
#         'product': ['Test Product'],
#         'comment': ['Test review content']
#     })
#     excel_buffer = io.BytesIO()
#     df.to_excel(excel_buffer, index=False)
#     excel_buffer.seek(0)

#     response = client.post(
#         "/analyze",
#         files={"file": ("test.xlsx", excel_buffer, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")},
#         data={
#             "prod_info": "test product",
#             "user_position": "Not Selected",
#             "analysis_focus": "Not Selected"
#         }
#     )
    
#     # Should return 200 even if OpenAI analysis fails
#     assert response.status_code in [200, 500]

def test_metrics():
    """Test metrics endpoint"""
    response = client.get("/metrics")
    assert response.status_code == 200
    metrics = response.json()
    assert metrics["service"] == "review_analyzer"
    assert metrics["status"] == "running"
    assert "version" in metrics