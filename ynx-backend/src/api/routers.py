from .auth import router as router_auth
from .user import router as router_user
from .generate import router as router_search
from .verify import router as router_verify

all_routers = [
    router_auth,
    router_verify,
    router_user,
    router_search,
]
