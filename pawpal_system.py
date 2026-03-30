from dataclasses import dataclass
from typing import List, Dict, Any
from datetime import date, time

@dataclass
class Pet:
    name: str
    species: str
    age: int
    special_needs: List[str]

    def get_info(self) -> Dict[str, Any]:
        pass

    def update_info(self, new_info: Dict[str, Any]):
        pass

@dataclass
class Task:
    name: str
    category: str
    duration: int  # in minutes
    priority: int  # 1-5
    frequency: str
    preferred_time: str  # or time range

    def is_due(self, check_date: date) -> bool:
        pass

    def get_duration(self) -> int:
        pass

    def set_priority(self, priority: int):
        pass

@dataclass
class Owner:
    name: str
    available_hours_per_day: int
    preferred_start_time: str
    preferred_end_time: str
    preferences: Dict[str, Any]

    def get_available_time(self) -> int:
        pass

    def update_preferences(self, new_prefs: Dict[str, Any]):
        pass

@dataclass
class Scheduler:
    pet: Pet
    owner: Owner
    tasks: List[Task]
    constraints: Dict[str, Any]

    def add_task(self, task: Task):
        pass

    def remove_task(self, task: Task):
        pass

    def generate_daily_plan(self, plan_date: date) -> 'DailyPlan':
        pass

    def optimize_schedule(self):
        pass

@dataclass
class DailyPlan:
    date: date
    scheduled_tasks: List[Dict[str, Any]]
    total_time: int
    explanation: str

    def add_scheduled_task(self, task: Task, start_time: time, end_time: time):
        pass

    def get_plan_summary(self) -> str:
        pass

    def explain_plan(self) -> str:
        pass
