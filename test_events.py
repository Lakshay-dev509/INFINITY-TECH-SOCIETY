
from services.event_service import (
    get_all_events,
    get_published_events
)

print("\n========== INFINITY EVENT DATABASE TEST ==========\n")

# Test 1: Fetch all events
result = get_all_events()

if result["success"]:
    print("ALL EVENTS: DATABASE CONNECTION SUCCESSFUL")
    print("Total events:", len(result["events"]))

    for event in result["events"]:
        print(
            event["EventID"],
            event["Title"],
            event["Status"]
        )
else:
    print("ALL EVENTS TEST FAILED:")
    print(result["message"])


# Test 2: Fetch published events
result = get_published_events()

if result["success"]:
    print("\nPUBLISHED EVENTS TEST SUCCESSFUL")
    print("Published events:", len(result["events"]))
else:
    print("\nPUBLISHED EVENTS TEST FAILED:")
    print(result["message"])


print("\n========== TEST COMPLETED ==========\n")
