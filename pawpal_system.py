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
    due_date: date | None = None
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

    def mark_complete(self) -> "Task | None":
        """Mark the task as completed and create the next recurring instance if needed."""
        self.completion_status = True

        if self.frequency not in {"daily", "weekly"}:
            return None

        # Compute next due date using timedelta
        current_due = self.due_date if self.due_date is not None else date.today()
        if self.frequency == "daily":
            next_due = current_due + timedelta(days=1)
        else:
            next_due = current_due + timedelta(weeks=1)

        # Return next instance for recurrence
        return Task(
            description=self.description,
            category=self.category,
            time=self.time,
            priority=self.priority,
            frequency=self.frequency,
            preferred_time=self.preferred_time,
            due_date=next_due,
            completion_status=False,
        )

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

    def mark_task_complete(self, task: Task, pet: Pet):
        """Mark a task complete for a given pet and add its next recurring instance if needed."""
        if pet not in self.owner.pets:
            raise ValueError("Pet not found for owner")

        if task not in pet.tasks:
            raise ValueError("Task not found for pet")

        next_task = task.mark_complete()
        if next_task is not None:
            # Enqueue next recurrence instance
            pet.add_task(next_task)
        return next_task

    def sort_by_time(self, tasks: List[Task]) -> List[Task]:
        """Return tasks sorted by ascending duration (minutes)."""
        return sorted(tasks, key=lambda t: t.time)

    def detect_conflicts(self, plan: 'DailyPlan') -> List[str]:
        """Return warning messages for overlapping task time ranges in a daily plan."""
        warnings = []
        entries = plan.scheduled_tasks

        def minutes_of(t: time) -> int:
            return t.hour * 60 + t.minute

        for i in range(len(entries)):
            for j in range(i + 1, len(entries)):
                t1 = entries[i]
                t2 = entries[j]
                s1, e1 = minutes_of(t1['start_time']), minutes_of(t1['end_time'])
                s2, e2 = minutes_of(t2['start_time']), minutes_of(t2['end_time'])

                if s1 < e2 and s2 < e1:
                    warnings.append(
                        f"Conflict: '{t1['task'].description}' ({t1['task'].category}) overlaps "
                        f"with '{t2['task'].description}' ({t2['task'].category})."
                    )

        return warnings

    def generate_daily_plan(self, plan_date: date) -> 'DailyPlan':
        """Generate a daily plan by scheduling due tasks in priority order."""
        tasks = self.owner.get_all_tasks()
        # Filter due and incomplete tasks
        due_tasks = [t for t in tasks if t.is_due(plan_date) and not t.completion_status]
        # Sort by priority (higher first), then by duration (shorter first)
        due_tasks.sort(key=lambda t: (-t.priority, t.time))
        # Optionally have an explicit time-sorted order method:
        due_tasks = self.sort_by_time(due_tasks)
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
        plan = DailyPlan(date=plan_date, scheduled_tasks=scheduled, total_time=total_time, explanation=explanation)
        conflicts = self.detect_conflicts(plan)
        plan.warnings = conflicts
        return plan

    def optimize_schedule(self):
        """Placeholder for advanced schedule optimization logic."""
        # Placeholder for optimization logic, e.g., consider preferred times or constraints
        pass

    def detect_conflicts(self, plan: 'DailyPlan') -> List[str]:
        """Detect conflicts where tasks overlap in scheduled time windows."""
        warnings = []
        entries = plan.scheduled_tasks

        def minutes_of(t: time) -> int:
            return t.hour * 60 + t.minute

        for i in range(len(entries)):
            for j in range(i + 1, len(entries)):
                t1 = entries[i]
                t2 = entries[j]
                s1, e1 = minutes_of(t1['start_time']), minutes_of(t1['end_time'])
                s2, e2 = minutes_of(t2['start_time']), minutes_of(t2['end_time'])

                if s1 < e2 and s2 < e1:  # Overlap check
                    warnings.append(
                        f"Conflict: '{t1['task'].description}' ({t1['task'].category}) overlaps "
                        f"with '{t2['task'].description}' ({t2['task'].category})."
                    )

        return warnings

    def filter_tasks(self, completed: bool | None = None, pet_name: str | None = None) -> List[Task]:
        """Return tasks filtered by completion status and/or pet name."""
        tasks = self.owner.get_all_tasks()

        if pet_name is not None:
            matching_pet = next((pet for pet in self.owner.pets if pet.name == pet_name), None)
            tasks = matching_pet.tasks if matching_pet else []

        if completed is not None:
            tasks = [t for t in tasks if t.completion_status == completed]

        return tasks

@dataclass
class DailyPlan:
    date: date
    scheduled_tasks: List[Dict[str, Any]]
    total_time: int
    explanation: str
    warnings: List[str] = field(default_factory=list)

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
