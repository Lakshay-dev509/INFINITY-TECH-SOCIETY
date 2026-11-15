
"""Neon PostgreSQL database connection and operations."""

import os
import psycopg
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")


def get_connection():
    if not DATABASE_URL:
        raise RuntimeError("DATABASE_URL missing in .env")

    return psycopg.connect(
        DATABASE_URL,
        connect_timeout=15,
        sslmode="require"
    )


def test_connection():
    """Test the PostgreSQL connection."""

    connection = None

    try:
        connection = get_connection()

        with connection.cursor() as cursor:
            cursor.execute("SELECT current_database(), current_user")
            result = cursor.fetchone()

        return {
            "success": True,
            "database": result[0],
            "login": result[1]
        }

    except Exception as error:
        return {
            "success": False,
            "error": str(error)
        }

    finally:
        if connection:
            connection.close()


def save_contact_message(name, email, subject, message):
    """Save a contact form message in PostgreSQL."""

    connection = None

    try:
        connection = get_connection()

        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO contactmessages
                (fullname, email, subject, message)
                VALUES (%s, %s, %s, %s)
                """,
                (name, email, subject, message)
            )

        connection.commit()
        return True

    except Exception as error:
        if connection:
            connection.rollback()

        print("Database error:", error)
        return False

    finally:
        if connection:
            connection.close()


def get_events():
    """Retrieve events from PostgreSQL."""

    connection = None

    try:
        connection = get_connection()

        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT eventid, eventname, description,
                       category, eventdate, venue, imagepath, status
                FROM events
                ORDER BY eventdate DESC
                """
            )

            return cursor.fetchall()

    except Exception as error:
        print("Event retrieval error:", error)
        return []

    finally:
        if connection:
            connection.close()
