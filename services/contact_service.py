"""Contact form processing placeholder."""

from services.database import get_connection


def submit_contact_message(name, email, subject, message):
    """
    Validate and save a contact form message
    into the INFINITY SQL Server database.
    """

    name = (name or "").strip()
    email = (email or "").strip()
    subject = (subject or "").strip()
    message = (message or "").strip()

    # Basic validation
    if not name or not email or not message:
        return {
            "success": False,
            "message": "Please fill all required fields."
        }

    if "@" not in email or "." not in email.split("@")[-1]:
        return {
            "success": False,
            "message": "Please enter a valid email address."
        }

    connection = None

    try:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO ContactMessages
            (FullName, Email, Subject, Message)
            VALUES (?, ?, ?, ?)
            """,
            (name, email, subject or None, message)
        )

        connection.commit()

        return {
            "success": True,
            "message": "Your message has been submitted successfully!"
        }

    except Exception as error:
        if connection:
            connection.rollback()

        print("Contact service error:", error)

        return {
            "success": False,
            "message": "Unable to submit your message. Please try again."
        }

    finally:
        if connection:
            connection.close()
