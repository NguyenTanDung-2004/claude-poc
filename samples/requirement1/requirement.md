Requirement 01 — Greeting Service
=================================

Background
----------

A basic service to demonstrate the CI/CD pipeline and JaCoCo reporting. It handles simple string manipulation and personalized messages.

Ask
---

Add two endpoints to the FastAPI app under samples/app/:

1.  **GET /hello** — Returns a generic greeting.
    
2.  **GET /hello/{name}** — Returns a personalized greeting using the name provided in the URL.
    

Observable Behavior (Acceptance Criteria)
-----------------------------------------

*   **Default Greeting:** A GET request to /hello must return 200 OK with the body {"message": "Hello, World!"}.
    
*   **Personalized Greeting:** A GET request to /hello/John must return 200 OK with the body {"message": "Hello, John!"}.
    
*   **Validation:** If the name is shorter than 2 characters, the service should return 400 Bad Request.
    
*   **Storage:** No persistence required.
    

Implementation Detail (For Dev)
-------------------------------

*   Use a simple Python function to capitalize the first letter of the name.
    
*   Ensure unit tests cover both the "valid name" and "too short name" scenarios to satisfy JaCoCo requirements.
    

### Why this is better for your JaCoCo testing:

1.  **Branch Coverage:** The "name length" validation creates an if/else branch. You can easily see if your tests cover both the success and the error paths.
    
2.  **Zero Dependencies:** You won't run into issues with URL validation libraries or complex logic.
    
3.  **Speed:** You can write the code and the tests in under 5 minutes.
    

Would you like me to provide the **FastAPI code** and the **Unit Tests** for this new requirement so you can run your JaCoCo report immediately?