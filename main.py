from pawpal_system import Owner, Pet, Task, Scheduler, DailyPlan
from datetime import date, time

# Create an Owner
owner = Owner(
    name="John Doe",
    available_hours_per_day=8,
    preferred_start_time="8:00 AM",
    preferred_end_time="6:00 PM",
    preferences={"morning_person": True}
)

# Create at least two Pets
pet1 = Pet(
    name="Buddy",
    species="Dog",
    age=3,
    special_needs=[]
)

pet2 = Pet(
    name="Whiskers",
    species="Cat",
    age=2,
    special_needs=["Dietary restrictions"]
)

# Add pets to the owner
owner.add_pet(pet1)
owner.add_pet(pet2)

# Create tasks out of order to test sorting/filtering
task1 = Task(
    description="Feed Breakfast",
    category="feeding",
    time=10,
    priority=4,
    frequency="daily",
    preferred_time="morning"
)

task2 = Task(
    description="Grooming",
    category="grooming",
    time=45,
    priority=2,
    frequency="weekly",
    preferred_time="afternoon"
)

task3 = Task(
    description="Evening Play",
    category="enrichment",
    time=20,
    priority=3,
    frequency="daily",
    preferred_time="evening"
)

# Assign tasks to pets in non-sequential order
pet2.add_task(task3)
pet1.add_task(task1)
pet1.add_task(task2)

# Mark one as complete to test filtering
task1.mark_complete()

# Create Scheduler
scheduler = Scheduler(owner=owner, constraints={})

# Print unsorted task list
print("Unsorted tasks:")
for task in owner.get_all_tasks():
    print(f"- {task.description}: {task.time} min, priority {task.priority}, complete={task.completion_status}")

# Sort tasks by time using scheduler method
sorted_by_time = scheduler.sort_by_time(owner.get_all_tasks())
print("\nTasks sorted by time:")
for task in sorted_by_time:
    print(f"- {task.description}: {task.time} min")

# Filter by completion status
incomplete_tasks = scheduler.filter_tasks(completed=False)
print("\nIncomplete tasks:")
for task in incomplete_tasks:
    print(f"- {task.description} (pet-specific by owner tasks) ")

# Filter by pet name
buddy_tasks = scheduler.filter_tasks(pet_name="Buddy")
print("\nBuddy's tasks:")
for task in buddy_tasks:
    print(f"- {task.description} (complete={task.completion_status})")

# Generate today schedule and print
plan = scheduler.generate_daily_plan(date.today())
print("\nToday's schedule summary:")
print(plan.get_plan_summary())
print("Explanation:")
print(plan.explain_plan())
if plan.warnings:
    print("Warnings:")
    for w in plan.warnings:
        print(f"- {w}")

# Manual conflict case: two tasks intentionally at same time
conflict_plan = DailyPlan(date=date.today(), scheduled_tasks=[], total_time=0, explanation="Conflict test")
conflict_plan.add_scheduled_task(task1, time(8, 0), time(8, 30))
conflict_plan.add_scheduled_task(task3, time(8, 0), time(8, 20))
conflicts = scheduler.detect_conflicts(conflict_plan)
print("\nManual conflict test warnings:")
for c in conflicts:
    print(f"- {c}")

task3 = Task(
    description="Playtime",
    category="enrichment",
    time=20,  # 20 minutes
    priority=3,
    frequency="daily",
    preferred_time="afternoon"
)

# Add tasks to pets
pet1.add_task(task1)
pet1.add_task(task2)
pet2.add_task(task3)

# Create a Scheduler
scheduler = Scheduler(owner=owner, constraints={})

# Generate today's schedule
today = date.today()
plan = scheduler.generate_daily_plan(today)

# Print "Today's Schedule" to the terminal
print("Today's Schedule:")
print(plan.get_plan_summary())
print("\nExplanation:")
print(plan.explain_plan())
