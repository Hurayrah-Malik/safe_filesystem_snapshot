"""
Random Python script.
Demonstrates:
- functions
- dictionaries and lists
- simple simulation
- name binding vs mutation
"""

import random
import time


def generate_users(count: int) -> list:
    """
    Create a list of user records.

    What this does:
    - Builds a list of dictionaries
    - Each dict represents a user

    Why Python behaves this way:
    - Lists store references to dict objects
    - Each dict is a separate object in memory
    """
    users = []

    for i in range(count):
        user = {
            "id": i,
            "score": random.randint(0, 100),
            "active": random.choice([True, False]),
        }
        users.append(user)  # mutation of the list

    return users


def boost_active_users(users: list, bonus: int) -> None:
    """
    Increase score for active users IN PLACE.

    What this does:
    - Mutates dictionaries inside the list

    Why:
    - `user` is a reference to the same dict object
    - Changing user["score"] mutates the original object
    """
    for user in users:
        if user["active"]:
            user["score"] += bonus


def average_score(users: list) -> float:
    """
    Compute average score.

    What this does:
    - Reads data only (no mutation)
    """
    total = sum(user["score"] for user in users)
    return total / len(users) if users else 0.0


def main() -> None:
    """
    Program entry point.
    """
    random.seed(time.time())  # non-deterministic randomness

    users = generate_users(5)
    print("Initial users:")
    print(users)

    boost_active_users(users, bonus=10)
    print("\nAfter boosting active users:")
    print(users)

    avg = average_score(users)
    print(f"\nAverage score: {avg:.2f}")


# This check prevents code from running on import
if __name__ == "__main__":
    main()
