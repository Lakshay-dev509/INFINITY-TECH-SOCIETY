
"""Test the INFINITY event registration service."""

from services.registration_service import register_for_event


def main():

    print("\n========== REGISTRATION TEST ==========")

    # Test registration for the existing published event
    result = register_for_event(
        name="GC Test User",
        email="gctest_registration@gmail.com",
        phone="9876543210",
        event_id=1
    )

    print("\nRegistration Result:")
    print(result)

    if result["success"]:
        print("\nREGISTRATION TEST PASSED!")
    else:
        print("\nREGISTRATION TEST RESULT:", result["message"])

    print("\n========== TEST COMPLETED ==========")


if __name__ == "__main__":
    main()
