"""Database connection and initialization functions will live here."""

import os
import mssql_python
from dotenv import load_dotenv

load_dotenv()

CONNECTION_STRING = os.getenv("SQL_CONNECTION_STRING")


def get_connection():
    if not CONNECTION_STRING:
        raise RuntimeError("SQL connection string missing in .env")

    return mssql_python.connect(CONNECTION_STRING)


def test_connection():
    connection = None

    try:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("SELECT DB_NAME(), SUSER_SNAME()")
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
    connection = None

    try:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT EventID, EventName, Description,
                   Category, EventDate, Venue, ImagePath, Status
            FROM Events
            ORDER BY EventDate DESC
        """)

        return cursor.fetchall()

    except Exception as error:
        print("Event retrieval error:", error)
        return []

    finally:
        if connection:
            connection.close()

