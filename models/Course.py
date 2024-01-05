class Course:
    def __init__(self, name: str = "", url: str = "", desc: str = "", teacher: str = "", classes: str = "") -> None:
        self.name = name.strip()
        self.url = url.strip()
        self.desc = desc.strip()
        self.teacher = teacher.strip()
        self.classes = classes.strip()

    def __repr__(self):
        return f'<Course {self.name} {self.url} {self.desc} {self.teacher} {self.classes}>'
