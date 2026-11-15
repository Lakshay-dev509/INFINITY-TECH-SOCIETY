from services.database import test_connection

result = test_connection()

if result["success"]:
    print("\nDATABASE CONNECTED SUCCESSFULLY!")
    print("Database:", result["database"])
    print("Login:", result["login"])
else:
    print("\nCONNECTION FAILED!")
    print("Error:", result["error"])