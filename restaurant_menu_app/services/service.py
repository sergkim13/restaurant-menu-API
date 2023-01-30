from sqlalchemy.orm import Session


class ServiceMixin:
    def __init__(self, db: Session):
        self.db = db
