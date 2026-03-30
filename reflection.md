# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

The PawPal+ system is built around five main parts: Pet, Task, Owner, Scheduler, and DailyPlan. Together, they help organize and plan pet care.

Pet: Stores basic info about the pet (name, type, age, special needs) and lets you view or update it.

Task: Represents a care activity (like feeding or walking). It includes details like how long it takes, how important it is, how often it happens, and when it should be done.

Owner: Holds information about the owner’s schedule and preferences, such as how much time they have each day and when they prefer to start or end tasks.

Scheduler: The “brain” of the system. It takes the pet, owner, and tasks, applies any rules or limits, and creates a daily plan.

DailyPlan: The final schedule for the day. It lists tasks with their times, total time needed, and a short explanation of the plan.

Relationships: Scheduler aggregates Pet, Owner, and a list of Tasks; it generates a DailyPlan. Tasks are associated with the Pet, and the Owner provides constraints for the Scheduler.

The Scheduler uses the Pet, Owner, and Tasks to create a DailyPlan. Tasks are for the pet, and the owner’s availability helps decide when they can be done.

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

The scheduler uses a basic method to detect conflicts. It only checks if tasks overlap in time and gives a warning if they do. It doesn’t try to fix the conflicts by rearranging or splitting tasks.

This keeps the system simple and fast, which is good for an early version (MVP). Instead of automatically solving conflicts, it lets the user see the issue and adjust task times or priorities themselves.

---

## 3. AI Collaboration

**a. How you used AI**

- Used VS Code Copilot to help set up the initial design (UML and basic class structure for Pet, Task, Owner, and Scheduler).
- Used it to suggest coding patterns, like sorting tasks, using dataclasses, and simple logic for conflicts and recurring tasks.
- Helpful prompts included things like:
“sort tasks by duration in a scheduler”
“detect overlap between task start and end times”

**b. Judgment and verification**

- One AI suggestion rejected: Copilot suggested a full backtracking interval scheduling conflict solver; I chose to keep a simpler, readable pairwise overlap warning strategy to avoid over-engineering.
- Verified the system using unit tests (sorting, recurrence, and conflict detection) and by checking outputs from main.py.

**c. Lead architect lesson**

- Separating into phases (design, implementation, UI) kept focus and reduced scope creep; each phase had its own chat session.
- Being the lead architect means you keep final control, prune suggestions, and enforce clear API boundaries through code and tests.

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
