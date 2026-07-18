def execute(intent: str, text: str):
    if intent == "reminder":
        from actions.reminder_action import get_reminders
        resp = get_reminders(text)
    
    elif intent == "weather":
        from actions.weather_action import get_weather
        resp = get_weather(text)
    
    elif intent == "device":
        from actions.device_action import device_action
        resp = device_action(text)
    
    elif intent == "identity":
        from actions.identity_action import update_identity
        resp = update_identity(text)
    
    else:
        from actions.general_actions import general_execute, fallback_response
        resp = fallback_response(text)
       
    return resp
