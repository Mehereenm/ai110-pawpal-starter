from pawpal_system import Owner, Pet, Task, Scheduler
from datetime import date

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

# Create at least three Tasks with different times
task1 = Task(
    description="Morning Walk",
    category="exercise",
    time=30,  # 30 minutes
    priority=5,
    frequency="daily",
    preferred_time="morning"
)

task2 = Task(
    description="Feed Breakfast",
    category="feeding",
    time=10,  # 10 minutes
    priority=4,
    frequency="daily",
    preferred_time="morning"
)

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
