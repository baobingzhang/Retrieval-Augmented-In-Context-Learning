
class TelemetryContext:
    def record_expense(self, *args, **kwargs): pass
    
telemetry_context = TelemetryContext()

def track_model_call(*args, **kwargs):
    def decorator(func):
        return func
    return decorator

def set_model_config(*args, **kwargs): pass
