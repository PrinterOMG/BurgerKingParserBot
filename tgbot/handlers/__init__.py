from .commands import register_commands
from .registration import register_registration
from .profile import register_profile

register_functions = (
    register_commands,
    register_registration,
    register_profile
)
