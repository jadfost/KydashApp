# session.py
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from flask_session import Session
from datetime import timedelta

session_bp = Blueprint('session_bp', __name__)
SESSION_TYPE = 'filesystem'

# Configuración de la extensión de sesión
session_bp.config = dict(
    SESSION_PERMANENT=True,
    SESSION_USE_SIGNER=True,
    SESSION_KEY_PREFIX='kydash_',
    PERMANENT_SESSION_LIFETIME=timedelta(hours=1),
)

# Inicializar la extensión de sesión
Session(session_bp)
