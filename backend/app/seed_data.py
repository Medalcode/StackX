from sqlalchemy.orm import Session

from .models import Attribute, Category, Technology, TechScore


def seed(db: Session):
    # categories
    backend_cat = Category(name='Backend', description='Backend frameworks')
    db.add(backend_cat)
    db.commit()

    # attributes
    a_scal = Attribute(name='Escalabilidad')
    a_fac = Attribute(name='Facilidad')
    a_ecos = Attribute(name='Ecosistema')
    db.add_all([a_scal, a_fac, a_ecos])
    db.commit()

    # technologies
    t_node = Technology(name='Node.js (Express)', description='JS backend', category_id=backend_cat.id)
    t_fastapi = Technology(name='FastAPI', description='Python modern API', category_id=backend_cat.id)
    t_go = Technology(name='Go (Gin)', description='Go microservices', category_id=backend_cat.id)
    db.add_all([t_node, t_fastapi, t_go])
    db.commit()

    # scores (1-10)
    db.add_all([
        TechScore(tech_id=t_node.id, attr_id=a_scal.id, value=8),
        TechScore(tech_id=t_node.id, attr_id=a_fac.id, value=9),
        TechScore(tech_id=t_node.id, attr_id=a_ecos.id, value=10),

        TechScore(tech_id=t_fastapi.id, attr_id=a_scal.id, value=8),
        TechScore(tech_id=t_fastapi.id, attr_id=a_fac.id, value=9),
        TechScore(tech_id=t_fastapi.id, attr_id=a_ecos.id, value=8),

        TechScore(tech_id=t_go.id, attr_id=a_scal.id, value=10),
        TechScore(tech_id=t_go.id, attr_id=a_fac.id, value=6),
        TechScore(tech_id=t_go.id, attr_id=a_ecos.id, value=7),
    ])
    db.commit()
