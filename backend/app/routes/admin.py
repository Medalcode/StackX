import os

from fastapi import APIRouter, BackgroundTasks, HTTPException, Request

from .. import sanity_sync

router = APIRouter()


def _validate_admin_token(request: Request):
    admin_token = os.getenv('ADMIN_TOKEN')
    if not admin_token:
        # No token configured: allow but warn (use infra to protect endpoint in production)
        return

    # Accept either `Authorization: Bearer <token>` or `X-ADMIN-TOKEN: <token>`
    auth = request.headers.get('Authorization')
    header_token = request.headers.get('X-ADMIN-TOKEN')
    if auth and auth.startswith('Bearer '):
        supplied = auth.split(' ', 1)[1].strip()
    else:
        supplied = header_token

    if not supplied or supplied != admin_token:
        raise HTTPException(status_code=403, detail='Forbidden')


@router.post('/sync-groq/')
def trigger_sanity_sync(background_tasks: BackgroundTasks, request: Request):
    """Trigger a background sync from Sanity/GROQ into the local DB.

    Protects the endpoint with `ADMIN_TOKEN` when that env var is set.
    """
    _validate_admin_token(request)
    background_tasks.add_task(sanity_sync.sync)
    return {"status": "accepted", "detail": "Sanity sync scheduled"}
