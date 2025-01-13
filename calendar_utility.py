import win32com.client
import datetime

def add_outlook_event(subject="New Meeting", start_time=None, duration=60, location="Remote", body=""):
    """
    Create a new Outlook appointment.
    Returns the EntryID of the created appointment.
    """
    
    outlook = win32com.client.Dispatch("Outlook.Application")
    appointment = outlook.CreateItem(1)  # 1=outlook appointment item

    # Defaults
    if not start_time:
        start_time = datetime.datetime.now() + datetime.timedelta(hours=1)

    appointment.Subject = subject
    appointment.Start = start_time
    appointment.Duration = duration
    appointment.Location = location
    appointment.Body = body

    appointment.Save()
    # appointment.Send() # Only if you need to send an actual meeting invite
    return appointment.EntryID

def find_calendar_events(search_subject=None):
    """
    Returns a list of matching Outlook appointment items.
    If search_subject is None, returns all. If search_subject is a string,
    returns events whose subject contains that string (case-insensitive).
    """
    outlook = win32com.client.Dispatch("Outlook.Application")
    namespace = outlook.GetNamespace("MAPI")
    calendar_folder = namespace.GetDefaultFolder(9)  # 9=outlook calendar folder

    items = calendar_folder.Items
    items.Sort("[Start]")
    items.IncludeRecurrences = True

    matching = []
    for item in items:
        # 26 = olAppointmentItem
        if item.Class == 26:
            # If no search_subject given, or subject matches
            if(search_subject is None or (item.Subject and search_subject.lower() in item.Subject.lower())):
                matching.append(item)
    return matching

def delete_outlook_event(entry_id):
    """
    Deletes the event with the given EntryID from Outlook.
    """
    outlook = win32com.client.Dispatch("Outlook.Application")
    namespace = outlook.GetNamespace("MAPI")
    appointment = namespace.GetFolderFromID(entry_id)
    appointment.Delete()

def update_outlook_event(entry_id, **kwargs):
    """
    Updates the event with given EntryID. Kwargs can include:
        subject, start_time (datetime), duration (int), location, body
    """
    outlook = win32com.client.Dispatch("Outlook.Application")
    namespace = outlook.GetNamespace("MAPI")
    appointment = namespace.GetFolderFromID(entry_id)

    if "subject" in kwargs:
        appointment.Subject = kwargs["subject"]
    if "start_time" in kwargs:
        appointment.Start = kwargs["start_time"]
    if "duration" in kwargs:
        appointment.Duration = kwargs["duration"]
    if "location" in kwargs:
        appointment.Location = kwargs["location"]
    if "body" in kwargs:
        appointment.Body = kwargs["body"]

    appointment.Save()
    return appointment.EntryID