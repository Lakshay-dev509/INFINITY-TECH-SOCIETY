
"""Event database operations for INFINITY."""

from services.database import get_connection


def get_all_events():
    """Fetch all events from the existing Events table."""

    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                EventID,
                EventName AS Title,
                Description,
                Category,
                EventDate,
                Venue,
                ImagePath,
                Status,
                CreatedAt
            FROM dbo.Events
            ORDER BY CreatedAt DESC;
        """)

        rows = cursor.fetchall()
        columns = [column[0] for column in cursor.description]

        events = [
            dict(zip(columns, row))
            for row in rows
        ]

        return {
            "success": True,
            "events": events,
            "message": "Events loaded successfully."
        }

    except Exception as error:

        print("EVENT DATABASE ERROR:", repr(error))

        return {
            "success": False,
            "events": [],
            "message": str(error)
        }

    finally:

        if cursor is not None:
            cursor.close()

        if connection is not None:
            connection.close()


def get_published_events():
    """Fetch published events from SQL Server."""

    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                EventID,
                EventName AS Title,
                Description,
                Category,
                EventDate,
                Venue,
                ImagePath,
                Status,
                CreatedAt
            FROM dbo.Events
            WHERE Status = 'Published'
            ORDER BY EventDate ASC;
        """)

        rows = cursor.fetchall()
        columns = [column[0] for column in cursor.description]

        events = [
            dict(zip(columns, row))
            for row in rows
        ]

        return {
            "success": True,
            "events": events,
            "message": "Published events loaded successfully."
        }

    except Exception as error:

        print("PUBLISHED EVENTS ERROR:", repr(error))

        return {
            "success": False,
            "events": [],
            "message": str(error)
        }

    finally:

        if cursor is not None:
            cursor.close()

        if connection is not None:
            connection.close()
