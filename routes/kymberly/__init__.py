from .novedad import novedad_bp
from .liquidaciones import liquidacion_bp
from .tradicional.diciembre_2023 import novedad_dic2023
from ..db.db import get_users_collection
from ..db.auth import auth_bp
from ..db.session import session_bp
from .cuotas import cuotas_bp
from .mecanica import mecanica_bp