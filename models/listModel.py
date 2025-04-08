from database import db 

 

class TaskList(db.Model):
    __tablename__ = 'lists'  # Name der Tabelle in der Datenbank

    id = db.Column(db.Integer, primary_key=True)  # Primärschlüssel
    name = db.Column(db.String(100), nullable=False)  # Name der Liste, z. B. „Arbeit“
    color = db.Column(db.String(20))  # Optional: z. B. „#ff9900“ für Farbanzeige

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))  # Liste gehört zu einem bestimmten Benutzer

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'color': self.color,
            'user_id': self.user_id
        }
