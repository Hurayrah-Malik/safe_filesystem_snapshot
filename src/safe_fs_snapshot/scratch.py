# Random Python code example
# Purpose: simulate a simple task queue with retry logic

import time
import random


class Task:
    """Represents a unit of work."""

    def __init__(self, task_id: int, max_retries: int = 3):
        self.task_id = task_id
        self.max_retries = max_retries
        self.attempts = 0

    def run(self) -> bool:
        """
        Simulate running the task.
        Returns True on success, False on failure.
        """
        self.attempts += 1

        # Randomly decide if the task succeeds
        success = random.random() > 0.4
        print(
            f"Task {self.task_id} attempt {self.attempts}: {'SUCCESS' if success else 'FAIL'}"
        )
        return success

    def can_retry(self) -> bool:
        """Check whether the task is allowed another retry."""
        return self.attempts < self.max_retries


def process_tasks(tasks: list[Task]) -> None:
    """
    Process tasks sequentially with retry logic.
    """
    for task in tasks:
        while True:
            if task.run():
                break  # Task completed successfully

            if not task.can_retry():
                print(f"Task {task.task_id} exhausted retries")
                break  # Give up on this task

            # Backoff before retrying
            sleep_time = random.uniform(0.2, 0.8)
            time.sleep(sleep_time)


def main() -> None:
    """Entry point."""
    random.seed()  # Initialize RNG from system entropy

    # Create a batch of tasks
    tasks = [Task(task_id=i) for i in range(1, 6)]

    process_tasks(tasks)


if __name__ == "__main__":
    main()
