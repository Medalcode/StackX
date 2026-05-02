from fastapi import APIRouter, Request, HTTPException
import os

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
def trigger_sanity_sync(request: Request):
    """Enqueue a Sanity/GROQ sync job via Celery and return the job id.

    Protects the endpoint with `ADMIN_TOKEN` when that env var is set.
    """
    _validate_admin_token(request)

    from ..tasks import sync_sanity  # imported here to avoid circular imports at module load
    result = sync_sanity.delay()
    return {"status": "queued", "job_id": result.id}
