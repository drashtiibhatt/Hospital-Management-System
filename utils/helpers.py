"""
Helper Utility Functions
Common helper functions used throughout the application
"""

from datetime import datetime, date, time, timedelta
import re


def format_date(date_obj, format_string='%Y-%m-%d'):
    """
    Format a date object to string

    Args:
        date_obj: date or datetime object
        format_string: desired format (default: YYYY-MM-DD)

    Returns:
        Formatted date string or None
    """
    if date_obj is None:
        return None

    if isinstance(date_obj, str):
        return date_obj

    try:
        return date_obj.strftime(format_string)
    except:
        return str(date_obj)


def format_time(time_obj, format_string='%H:%M'):
    """
    Format a time object to string

    Args:
        time_obj: time or datetime object
        format_string: desired format (default: HH:MM)

    Returns:
        Formatted time string or None
    """
    if time_obj is None:
        return None

    if isinstance(time_obj, str):
        return time_obj

    try:
        return time_obj.strftime(format_string)
    except:
        return str(time_obj)


def format_datetime(datetime_obj, format_string='%Y-%m-%d %H:%M:%S'):
    """
    Format a datetime object to string

    Args:
        datetime_obj: datetime object
        format_string: desired format

    Returns:
        Formatted datetime string or None
    """
    if datetime_obj is None:
        return None

    if isinstance(datetime_obj, str):
        return datetime_obj

    try:
        return datetime_obj.strftime(format_string)
    except:
        return str(datetime_obj)


def parse_date(date_string, format_string='%Y-%m-%d'):
    """
    Parse a date string to date object

    Args:
        date_string: date in string format
        format_string: format of the input string

    Returns:
        date object or None
    """
    if not date_string:
        return None

    if isinstance(date_string, date):
        return date_string

    try:
        return datetime.strptime(date_string, format_string).date()
    except:
        return None


def parse_time(time_string, format_string='%H:%M'):
    """
    Parse a time string to time object

    Args:
        time_string: time in string format
        format_string: format of the input string

    Returns:
        time object or None
    """
    if not time_string:
        return None

    if isinstance(time_string, time):
        return time_string

    try:
        return datetime.strptime(time_string, format_string).time()
    except:
        return None


def calculate_age(birth_date):
    """
    Calculate age from date of birth

    Args:
        birth_date: date of birth (date object or string)

    Returns:
        Age in years (int) or None
    """
    if not birth_date:
        return None

    # Convert string to date if needed
    if isinstance(birth_date, str):
        birth_date = parse_date(birth_date)

    if not birth_date:
        return None

    today = date.today()
    age = today.year - birth_date.year

    # Adjust if birthday hasn't occurred this year
    if (today.month, today.day) < (birth_date.month, birth_date.day):
        age -= 1

    return age


def get_date_range(start_date, end_date):
    """
    Get list of dates between start and end date

    Args:
        start_date: starting date
        end_date: ending date

    Returns:
        List of date objects
    """
    if isinstance(start_date, str):
        start_date = parse_date(start_date)
    if isinstance(end_date, str):
        end_date = parse_date(end_date)

    if not start_date or not end_date:
        return []

    date_list = []
    current_date = start_date

    while current_date <= end_date:
        date_list.append(current_date)
        current_date += timedelta(days=1)

    return date_list


def get_next_n_days(n=7, start_date=None):
    """
    Get next N days from start date

    Args:
        n: number of days (default: 7)
        start_date: starting date (default: today)

    Returns:
        List of date objects
    """
    if start_date is None:
        start_date = date.today()
    elif isinstance(start_date, str):
        start_date = parse_date(start_date)

    date_list = []
    for i in range(n):
        date_list.append(start_date + timedelta(days=i))

    return date_list


def is_weekend(check_date):
    """
    Check if date is weekend (Saturday or Sunday)

    Args:
        check_date: date to check

    Returns:
        True if weekend, False otherwise
    """
    if isinstance(check_date, str):
        check_date = parse_date(check_date)

    if not check_date:
        return False

    # Monday = 0, Sunday = 6
    return check_date.weekday() >= 5


def get_weekday_name(check_date):
    """
    Get weekday name from date

    Args:
        check_date: date object

    Returns:
        Weekday name (e.g., 'Monday')
    """
    if isinstance(check_date, str):
        check_date = parse_date(check_date)

    if not check_date:
        return None

    return check_date.strftime('%A')


def validate_email(email):
    """
    Validate email address format

    Args:
        email: email address string

    Returns:
        True if valid, False otherwise
    """
    if not email:
        return False

    # Basic email regex pattern
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validate_phone(phone):
    """
    Validate phone number format

    Args:
        phone: phone number string

    Returns:
        True if valid, False otherwise
    """
    if not phone:
        return False

    # Remove spaces, dashes, parentheses
    clean_phone = re.sub(r'[\s\-\(\)]', '', phone)

    # Check if it contains only digits and is 10 digits long
    return clean_phone.isdigit() and len(clean_phone) == 10


def format_phone(phone):
    """
    Format phone number to standard format

    Args:
        phone: phone number string

    Returns:
        Formatted phone number or original if invalid
    """
    if not phone:
        return phone

    # Remove all non-digit characters
    digits = re.sub(r'\D', '', phone)

    # Format as XXX-XXX-XXXX if 10 digits
    if len(digits) == 10:
        return f'{digits[:3]}-{digits[3:6]}-{digits[6:]}'

    return phone


def sanitize_string(input_string, max_length=None):
    """
    Sanitize user input string

    Args:
        input_string: string to sanitize
        max_length: maximum allowed length

    Returns:
        Sanitized string
    """
    if not input_string:
        return ''

    # Strip whitespace
    sanitized = input_string.strip()

    # Truncate if max_length specified
    if max_length and len(sanitized) > max_length:
        sanitized = sanitized[:max_length]

    return sanitized


def generate_time_slots(start_time, end_time, interval_minutes=30):
    """
    Generate time slots between start and end time

    Args:
        start_time: starting time (time object or string)
        end_time: ending time (time object or string)
        interval_minutes: interval in minutes (default: 30)

    Returns:
        List of time objects
    """
    if isinstance(start_time, str):
        start_time = parse_time(start_time)
    if isinstance(end_time, str):
        end_time = parse_time(end_time)

    if not start_time or not end_time:
        return []

    # Convert to datetime for easy manipulation
    start_dt = datetime.combine(date.today(), start_time)
    end_dt = datetime.combine(date.today(), end_time)

    time_slots = []
    current_time = start_dt

    while current_time <= end_dt:
        time_slots.append(current_time.time())
        current_time += timedelta(minutes=interval_minutes)

    return time_slots


def get_status_badge_class(status):
    """
    Get Bootstrap badge class for appointment status

    Args:
        status: appointment status string

    Returns:
        Bootstrap class name
    """
    status_classes = {
        'Booked': 'badge-primary',
        'Completed': 'badge-success',
        'Cancelled': 'badge-danger'
    }
    return status_classes.get(status, 'badge-secondary')


def paginate_list(items, page=1, per_page=10):
    """
    Paginate a list of items

    Args:
        items: list of items
        page: current page number (1-indexed)
        per_page: items per page

    Returns:
        Dictionary with pagination info
    """
    total_items = len(items)
    total_pages = (total_items + per_page - 1) // per_page

    # Ensure page is within valid range
    page = max(1, min(page, total_pages)) if total_pages > 0 else 1

    start_idx = (page - 1) * per_page
    end_idx = start_idx + per_page

    return {
        'items': items[start_idx:end_idx],
        'page': page,
        'per_page': per_page,
        'total_items': total_items,
        'total_pages': total_pages,
        'has_prev': page > 1,
        'has_next': page < total_pages,
        'prev_page': page - 1 if page > 1 else None,
        'next_page': page + 1 if page < total_pages else None
    }


def flash_form_errors(form):
    """
    Flash all form validation errors

    Args:
        form: WTForm form object with errors
    """
    from flask import flash

    for field, errors in form.errors.items():
        for error in errors:
            flash(f'{field}: {error}', 'danger')


def allowed_file(filename, allowed_extensions=None):
    """
    Check if file has allowed extension

    Args:
        filename: name of the file
        allowed_extensions: set of allowed extensions

    Returns:
        True if allowed, False otherwise
    """
    if allowed_extensions is None:
        allowed_extensions = {'png', 'jpg', 'jpeg', 'gif'}

    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions


def get_current_time():
    """Get current time"""
    return datetime.now().time()


def get_today():
    """Get today's date"""
    return date.today()


def is_past_datetime(check_date, check_time=None):
    """
    Check if date/time is in the past

    Args:
        check_date: date to check
        check_time: optional time to check

    Returns:
        True if in past, False otherwise
    """
    if isinstance(check_date, str):
        check_date = parse_date(check_date)

    today = date.today()

    if check_date < today:
        return True
    elif check_date == today and check_time:
        if isinstance(check_time, str):
            check_time = parse_time(check_time)
        current_time = get_current_time()
        return check_time < current_time

    return False


def truncate_string(text, length=50, suffix='...'):
    """
    Truncate string to specified length

    Args:
        text: string to truncate
        length: maximum length
        suffix: suffix to add if truncated

    Returns:
        Truncated string
    """
    if not text or len(text) <= length:
        return text

    return text[:length].strip() + suffix
