
"""Event database operations for INFINITY using Neon PostgreSQL."""

from services.database import get_connection


def get_all_events():
    connection = None

    try:
        connection = get_connection()

        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT
                    eventid AS "EventID",
                    eventname AS "Title",
                    description AS "Description",
                    category AS "Category",
                    eventdate AS "EventDate",
                    venue AS "Venue",
                    imagepath AS "ImagePath",
                    status AS "Status",
                    createdat AS "CreatedAt"
                FROM public.events
                ORDER BY createdat DESC;
            """)

            rows = cursor.fetchall()
            columns = [column.name for column in cursor.description]

            events = [dict(zip(columns, row)) for row in rows]

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
        if connection:
            connection.close()


def get_published_events():
    connection = None

    try:
        connection = get_connection()

        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT
                    eventid AS "EventID",
                    eventname AS "Title",
                    description AS "Description",
                    category AS "Category",
                    eventdate AS "EventDate",
                    venue AS "Venue",
                    imagepath AS "ImagePath",
                    status AS "Status",
                    createdat AS "CreatedAt"
                FROM public.events
                WHERE status = 'Published'
                ORDER BY eventdate ASC;
            """)

            rows = cursor.fetchall()
            columns = [column.name for column in cursor.description]

            events = [dict(zip(columns, row)) for row in rows]

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
        if connection:
            connection.close()
