import os
import requests
from sqlalchemy.orm import Session
from .database import SessionLocal
from .models import Category, Technology

SANITY_PROJECT_ID = os.getenv('SANITY_PROJECT_ID')
SANITY_DATASET = os.getenv('SANITY_DATASET', 'production')
SANITY_API_VERSION = os.getenv('SANITY_API_VERSION', '2024-01-01')
SANITY_TOKEN = os.getenv('SANITY_TOKEN')

def fetch_technologies():
    if not SANITY_PROJECT_ID:
        raise RuntimeError('SANITY_PROJECT_ID not set')

    url = f"https://{SANITY_PROJECT_ID}.api.sanity.io/v{SANITY_API_VERSION}/data/query/{SANITY_DATASET}"
    # Basic GROQ to fetch technology docs; adjust according to your schema
    groq = '*[_type == "technology"]{_id, name, description, category->{name}}'
    resp = requests.get(url, params={'query': groq}, headers={
        'Authorization': f'Bearer {SANITY_TOKEN}'
    } if SANITY_TOKEN else {})
    resp.raise_for_status()
    data = resp.json()
    return data.get('result', [])

def upsert_technologies(db: Session, techs):
    for t in techs:
        name = t.get('name') or t.get('_id')
        desc = t.get('description')
        cat = t.get('category', {}).get('name') if t.get('category') else None

        # find or create category
        cat_obj = None
        if cat:
            cat_obj = db.query(Category).filter_by(name=cat).first()
            if not cat_obj:
                cat_obj = Category(name=cat, description=None)
                db.add(cat_obj)
                db.commit()

        tech_obj = db.query(Technology).filter_by(name=name).first()
        if not tech_obj:
            tech_obj = Technology(name=name, description=desc, category_id=cat_obj.id if cat_obj else None)
            db.add(tech_obj)
        else:
            tech_obj.description = desc
            if cat_obj:
                tech_obj.category_id = cat_obj.id
        db.commit()

def sync():
    techs = fetch_technologies()
    db = SessionLocal()
    try:
        upsert_technologies(db, techs)
    finally:
        db.close()


if __name__ == '__main__':
    sync()
