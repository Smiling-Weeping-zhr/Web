from flask_login import UserMixin
from datetime import datetime
from sqlalchemy import or_, desc
from sqlalchemy.dialects.postgresql import ARRAY
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login_manager


class Dataset(db.Model):
    __tablename__ = 'datasets'
    id = db.Column(db.Integer, primary_key=True)  # 必须有
    study_id = db.Column(db.String(50), nullable=False)
    sample_name = db.Column(db.String(100), nullable=False)
    biome = db.Column(db.String(50))
    data_type = db.Column(db.String(50))
    release_date = db.Column(db.Date)
    tags = db.Column(ARRAY(db.Text))  # PostgreSQL TEXT[]
    download_link = db.Column(db.Text)

    def __repr__(self):
        return f"<Dataset {self.study_id} - {self.sample_name}>"

    @classmethod
    def search(cls, form):
        """
        Apply filters from DownloadSearchForm
        """
        query = cls.query

        # 关键词搜索
        if form.keyword.data:
            keyword = f"%{form.keyword.data}%"
            query = query.filter(
                or_(
                    cls.study_id.ilike(keyword),
                    cls.sample_name.ilike(keyword)
                )
            )

        # biome 过滤
        if form.biome.data:
            query = query.filter(cls.biome == form.biome.data)

        # data type 过滤
        if form.data_type.data:
            query = query.filter(cls.data_type == form.data_type.data)

        # 多标签过滤（PostgreSQL 数组重叠）
        if form.tags.data:
            query = query.filter(cls.tags.overlap(form.tags.data))

        # 排序
        if form.sort_by.data == "release_date_desc":
            query = query.order_by(desc(cls.release_date))
        elif form.sort_by.data == "release_date_asc":
            query = query.order_by(cls.release_date)
        else:
            query = query.order_by(cls.study_id)

        return query
    
    
class Employee(UserMixin, db.Model):
    """
    Employee table
    """
    __tablename__ = 'users'  # 数据库表名

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(60), index=True, unique=True)
    first_name = db.Column(db.String(60), index=True)
    last_name = db.Column(db.String(60), index=True)
    password_hash = db.Column(db.String(128))
    user_type = db.Column(db.String(20))
    is_admin = db.Column(db.Boolean, default=False)

    @property
    def password(self):
        """Prevent password from being accessed"""
        raise AttributeError('password is not a readable attribute.')

    @password.setter
    def password(self, password):
        """Set password to a hashed password"""
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """Check if hashed password matches actual password"""
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<Employee: {}>'.format(self.email)  # 用 email 替代 username

# Flask-Login user loader
@login_manager.user_loader
def load_user(user_id):
    return Employee.query.get(int(user_id))
