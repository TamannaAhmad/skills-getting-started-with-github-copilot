def test_get_activities(client):
    """Test GET /activities returns all activities."""
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert "Programming Class" in data
    assert data["Chess Club"]["description"] == "Learn strategies and compete in chess tournaments"
    assert data["Chess Club"]["participants"] == ["michael@mergington.edu"]

def test_signup_success(client):
    """Test successful signup for an activity."""
    response = client.post("/activities/Programming%20Class/signup?email=test@mergington.edu")
    assert response.status_code == 200
    data = response.json()
    assert "Signed up test@mergington.edu for Programming Class" in data["message"]
    # Verify added
    activities = client.get("/activities").json()
    assert "test@mergington.edu" in activities["Programming Class"]["participants"]

def test_signup_activity_not_found(client):
    """Test signup for non-existent activity."""
    response = client.post("/activities/NonExistent/signup?email=test@mergington.edu")
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Activity not found"

def test_signup_already_signed_up(client):
    """Test signup when already signed up."""
    response = client.post("/activities/Chess%20Club/signup?email=michael@mergington.edu")
    assert response.status_code == 400
    data = response.json()
    assert data["detail"] == "Student is already signed up for this activity"

def test_unregister_success(client):
    """Test successful unregister from an activity."""
    response = client.delete("/activities/Chess%20Club/signup?email=michael@mergington.edu")
    assert response.status_code == 200
    data = response.json()
    assert "Unregistered michael@mergington.edu from Chess Club" in data["message"]
    # Verify removed
    activities = client.get("/activities").json()
    assert "michael@mergington.edu" not in activities["Chess Club"]["participants"]

def test_unregister_activity_not_found(client):
    """Test unregister from non-existent activity."""
    response = client.delete("/activities/NonExistent/signup?email=test@mergington.edu")
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Activity not found"

def test_unregister_not_signed_up(client):
    """Test unregister when not signed up."""
    response = client.delete("/activities/Programming%20Class/signup?email=notsigned@mergington.edu")
    assert response.status_code == 400
    data = response.json()
    assert data["detail"] == "Student not signed up"