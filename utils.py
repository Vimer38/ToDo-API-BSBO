from datetime import datetime, timezone

URGENT_DAYS = 3  # срочно, если до дедлайна осталось 3 дня или меньше


def to_utc(dt: datetime) -> datetime:
    """Naive-дату считаем UTC, aware приводим к UTC."""
    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def calculate_days_left(deadline_at: datetime) -> int:
    """Дней от сегодняшней даты до дедлайна (отрицательное = просрочено)."""
    today = datetime.now(timezone.utc).date()
    return (to_utc(deadline_at).date() - today).days


def is_urgent(deadline_at: datetime) -> bool:
    return calculate_days_left(deadline_at) <= URGENT_DAYS


def calculate_quadrant(is_important: bool, deadline_at: datetime) -> str:
    urgent = is_urgent(deadline_at)
    if is_important and urgent:
        return "Q1"
    if is_important and not urgent:
        return "Q2"
    if not is_important and urgent:
        return "Q3"
    return "Q4"