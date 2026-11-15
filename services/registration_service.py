
"""Event registration service for INFINITY."""

from services.database import get_connection


def register_for_event(name, email, phone, event_id):

    name = (name or "").strip()
    email = (email or "").strip().lower()
    phone = (phone or "").strip()

    if not name or not email or not phone or not event_id:
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
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor()

        # Check whether the event exists and is published
        cursor.execute(
            """
            SELECT EventID
            FROM dbo.Events
            WHERE EventID = ? AND Status = 'Published'
            """,
            (event_id,)
        )

        if not cursor.fetchone():
            return {
                "success": False,
                "message": "This event is not available for registration."
            }

        # Find existing user by email
        cursor.execute(
            """
            SELECT UserID
            FROM dbo.Users
            WHERE Email = ?
            """,
            (email,)
        )

        user = cursor.fetchone()

        if user:
            user_id = user[0]

        else:
            # Create new user
            cursor.execute(
            """
            INSERT INTO dbo.Users (FullName, Email, Phone)
            OUTPUT INSERTED.UserID
            VALUES (?, ?, ?)
            """,
            (name, email, phone)
        )

        user_id = cursor.fetchone()[0]

        # Prevent duplicate registration
        cursor.execute(
            """
            SELECT RegistrationID
            FROM dbo.Registrations
            WHERE UserID = ? AND EventID = ?
            """,
            (user_id, event_id)
        )

        if cursor.fetchone():
            connection.rollback()
            return {
                "success": False,
                "message": "You have already registered for this event."
            }

        # Save registration
        cursor.execute(
            """
            INSERT INTO dbo.Registrations (UserID, EventID)
            VALUES (?, ?)
            """,
            (user_id, event_id)
        )

        connection.commit()

        return {
            "success": True,
            "message": "Registration successful! Welcome to INFINITY."
        }

    except Exception as error:
        if connection:
            connection.rollback()

        print("REGISTRATION ERROR:", repr(error))

        return {
            "success": False,
            "message": "Registration failed. Please try again."
        }

    finally:
        if cursor:
            cursor.close()

        if connection:
            connection.close()
