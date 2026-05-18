from typing import Optional


def perfil_tipo(request) -> dict:
    """Expose the authenticated user's Perfil.tipo as ``perfil_tipo`` in templates.

    Returns {'perfil_tipo': <string>|None}.
    """
    tipo: Optional[str] = None

    user = getattr(request, 'user', None)
    if user and user.is_authenticated:
        try:
            perfil = getattr(user, 'perfil', None)
            if perfil:
                tipo = getattr(perfil, 'tipo', None)
        except Exception:
            tipo = None

    return {'perfil_tipo': tipo}
