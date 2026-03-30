# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

The initial UML design for PawPal+ includes the following main classes to model the pet care planning system: Pet, Task, Owner, Scheduler, and DailyPlan. These classes encapsulate the data and logic for managing pet information, care tasks, owner constraints, scheduling logic, and the resulting daily plans.

- **Pet**: Represents the pet being cared for. Responsibilities: Store and manage pet details. Attributes: name (str), species (str), age (int), special_needs (list of str). Methods: __init__, get_info (return pet details as dict), update_info (modify pet attributes).

- **Task**: Represents individual care tasks. Responsibilities: Define task properties and check scheduling relevance. Attributes: name (str), category (str), duration (int in minutes), priority (int 1-5), frequency (str), preferred_time (str or range). Methods: __init__, is_due (check if task is due on a given day), get_duration, set_priority.

- **Owner**: Represents the pet owner. Responsibilities: Hold owner preferences and availability. Attributes: name (str), available_hours_per_day (int), preferred_start_time (str), preferred_end_time (str), preferences (dict). Methods: __init__, get_available_time, update_preferences.

- **Scheduler**: Core logic class for generating plans. Responsibilities: Manage tasks, apply constraints, and create daily schedules. Attributes: pet (Pet instance), owner (Owner instance), tasks (list of Task), constraints (dict). Methods: __init__, add_task, remove_task, generate_daily_plan (return DailyPlan based on tasks and constraints), optimize_schedule.

- **DailyPlan**: Represents the output daily schedule. Responsibilities: Store and display scheduled tasks with explanations. Attributes: date (date), scheduled_tasks (list of dicts with task, start_time, end_time), total_time (int), explanation (str). Methods: __init__, add_scheduled_task, get_plan_summary, explain_plan.

Relationships: Scheduler aggregates Pet, Owner, and a list of Tasks; it generates a DailyPlan. Tasks are associated with the Pet, and the Owner provides constraints for the Scheduler.

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

**c. Core User Actions**

Based on the scenario in README.md, PawPal+ is designed to help busy pet owners plan and track pet care tasks by generating daily schedules considering constraints like time availability, task priorities, and owner preferences.

The three core actions a user should be able to perform are:

1. Add a pet: Enter basic information about the owner and their pet, such as pet name, type, age, and any special needs. 

2. Add/edit tasks: Create or modify pet care tasks, including details like task type (e.g., walk, feeding, medication), duration, priority level, and any specific preferences or constraints. For example, scheduling a daily walk with a set duration and high priority.

3. View today's tasks: Generate and display a daily schedule or plan of tasks based on the entered information, constraints, and priorities. 

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
