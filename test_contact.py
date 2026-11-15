from services.contact_service import submit_contact_message

result = submit_contact_message(
    name="INFINITY Test User",
    email="test@example.com",
    subject="Database Integration Test",
    message="Testing contact form integration with SQL Server."
)

print(result)