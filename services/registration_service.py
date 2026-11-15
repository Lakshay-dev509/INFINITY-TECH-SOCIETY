
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

    try:
        connection = get_connection()

        with connection.cursor() as cursor:

            # Check published event
            cursor.execute(
                """
                SELECT eventid
                FROM events
                WHERE eventid = %s AND status = 'Published'
                """,
                (event_id,)
            )

            if not cursor.fetchone():
                return {
                    "success": False,
                    "message": "This event is not available for registration."
                }

            # Find existing user
            cursor.execute(
                """
                SELECT userid
                FROM users
                WHERE email = %s
                """,
                (email,)
            )

            user = cursor.fetchone()

            if user:
                user_id = user[0]

            else:
                cursor.execute(
                    """
                    INSERT INTO users (fullname, email, phone)
                    VALUES (%s, %s, %s)
                    RETURNING userid
                    """,
                    (name, email, phone)
                )

                user_id = cursor.fetchone()[0]

            # Prevent duplicate registration
            cursor.execute(
                """
                SELECT registrationid
                FROM registrations
                WHERE userid = %s AND eventid = %s
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
                INSERT INTO registrations (userid, eventid)
                VALUES (%s, %s)
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
        if connection:
            connection.close()
