from dataclasses import dataclass, field
from typing import List, Dict, Any
from datetime import date, time, datetime, timedelta

@dataclass
class Task:
    description: str
    category: str
    time: int  # in minutes
    priority: int  # 1-5, higher is more important
    frequency: str  # e.g., "daily", "weekly"
    preferred_time: str  # e.g., "morning", "evening"
    completion_status: bool = False

    def is_due(self, check_date: date) -> bool:
        """Check if the task is due on the given date."""
        # Simple implementation: assume daily tasks are always due
        # For more complex, check frequency against date
        if self.frequency == "daily":
            return True
        # Add logic for other frequencies if needed
        return False

    def get_time(self) -> int:
        """Return the time required for the task in minutes."""
        return self.time

    def set_priority(self, priority: int):
        """Set the priority level of the task (1-5)."""
        self.priority = priority

    def mark_complete(self):
        """Mark the task as completed."""
        self.completion_status = True

@dataclass
class Pet:
    name: str
    species: str
    age: int
    special_needs: List[str]
    tasks: List[Task] = field(default_factory=list)

    def get_info(self) -> Dict[str, Any]:
        """Return a dictionary containing pet details and task descriptions."""
        return {
            "name": self.name,
            "species": self.species,
            "age": self.age,
            "special_needs": self.special_needs,
            "tasks": [task.description for task in self.tasks]
        }

    def update_info(self, new_info: Dict[str, Any]):
        """Update pet attributes with the provided dictionary."""
        for key, value in new_info.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def add_task(self, task: Task):
        """Add a task to the pet's task list."""
        self.tasks.append(task)

    def remove_task(self, task: Task):
        """Remove a task from the pet's task list if it exists."""
        if task in self.tasks:
            self.tasks.remove(task)

@dataclass
class Owner:
    name: str
    available_hours_per_day: int
    preferred_start_time: str
    preferred_end_time: str
    preferences: Dict[str, Any]
    pets: List[Pet] = field(default_factory=list)

    def get_available_time(self) -> int:
        """Return the owner's available hours per day."""
        return self.available_hours_per_day

    def update_preferences(self, new_prefs: Dict[str, Any]):
        """Update the owner's preferences with new values."""
        self.preferences.update(new_prefs)

    def add_pet(self, pet: Pet):
        """Add a pet to the owner's pet list."""
        self.pets.append(pet)

    def get_all_tasks(self) -> List[Task]:
        """Return a flattened list of all tasks from all pets."""
        all_tasks = []
        for pet in self.pets:
            all_tasks.extend(pet.tasks)
        return all_tasks

@dataclass
class Scheduler:
    owner: Owner
    constraints: Dict[str, Any]

    def add_task(self, task: Task, pet: Pet):
        """Add a task to the specified pet if owned by the owner."""
        if pet in self.owner.pets:
            pet.add_task(task)

    def remove_task(self, task: Task, pet: Pet):
        """Remove a task from the specified pet if owned by the owner."""
        if pet in self.owner.pets:
            pet.remove_task(task)

    def generate_daily_plan(self, plan_date: date) -> 'DailyPlan':
        """Generate a daily plan by scheduling due tasks in priority order."""
        tasks = self.owner.get_all_tasks()
        # Filter due and incomplete tasks
        due_tasks = [t for t in tasks if t.is_due(plan_date) and not t.completion_status]
        # Sort by priority (higher first)
        due_tasks.sort(key=lambda t: t.priority, reverse=True)
        # Simple scheduling: start at 8 AM, schedule sequentially
        scheduled = []
        current_time = time(8, 0)
        total_time = 0
        for task in due_tasks:
            start = current_time
            end_dt = datetime.combine(plan_date, start) + timedelta(minutes=task.time)
            end = end_dt.time()
            scheduled.append({"task": task, "start_time": start, "end_time": end})
            current_time = end
            total_time += task.time
        explanation = f"Scheduled {len(scheduled)} tasks in priority order, starting at 8:00 AM."
        return DailyPlan(date=plan_date, scheduled_tasks=scheduled, total_time=total_time, explanation=explanation)

    def optimize_schedule(self):
        """Placeholder for advanced schedule optimization logic."""
        # Placeholder for optimization logic, e.g., consider preferred times or constraints
        pass

@dataclass
class DailyPlan:
    date: date
    scheduled_tasks: List[Dict[str, Any]]
    total_time: int
    explanation: str

    def add_scheduled_task(self, task: Task, start_time: time, end_time: time):
        """Add a scheduled task with start and end times to the plan."""
        self.scheduled_tasks.append({"task": task, "start_time": start_time, "end_time": end_time})
        self.total_time += task.time

    def get_plan_summary(self) -> str:
        """Return a formatted string summary of the daily plan."""
        summary = f"Daily Plan for {self.date}:\n"
        for item in self.scheduled_tasks:
            task = item["task"]
            start = item["start_time"]
            end = item["end_time"]
            summary += f"- {task.description} ({start} - {end})\n"
        summary += f"Total time: {self.total_time} minutes\n"
        return summary

    def explain_plan(self) -> str:
        """Return the explanation of how the plan was generated."""
        return self.explanation
