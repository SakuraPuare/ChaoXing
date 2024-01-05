class Course:
    def __init__(self, name: str = "", ids: str = "", class_ids: str = "", desc: str = "",
                 teacher: str = "", classes: str = "",
                 is_finish: bool = False) -> None:
        self.name = name.strip()
        self.ids = ids.strip()
        self.class_ids = class_ids.strip()
        self.desc = desc.strip()
        self.teacher = teacher.strip()
        self.classes = classes.strip()

        self.is_finish = is_finish

    def __repr__(self):
        return f'<Course {self.name} {self.ids} {self.teacher}>'


class Chapter:
    def __init__(self, title: str = "", tasks: int = 0, ids: str = ""):
        self.seq = -1

        self.title = title
        self.tasks = tasks
        self.ids = ids

    def __repr__(self):
        return f'<Chapter {self.seq} {self.title} {self.ids}>'


class Unit:
    def __init__(self, title: str = ""):
        self.seq = -1

        self.title = title
        self.chapters = []

    def __repr__(self):
        return f'<Unit {self.seq} {self.title} {len(self.chapters)}>'

    def __len__(self):
        return len(self.chapters)

    def __iter__(self):
        return iter(self.chapters)

    def add_chapter(self, chapter: Chapter) -> None:
        chapter.seq = len(self.chapters) + 1
        self.chapters.append(chapter)


class Catalog:
    def __init__(self):
        self.units = []

    def __repr__(self):
        return f'<Catalog {len(self.units)}>'

    def __iter__(self):
        return iter(self.units)

    def add_unit(self, unit: Unit) -> None:
        unit.seq = len(self.units) + 1
        self.units.append(unit)
