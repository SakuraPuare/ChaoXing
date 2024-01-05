class Video:
    def __init__(self, data: dict):
        self.aid: int = 0
        self.begins: int = 0
        self.customType: int = 0
        self.ends: int = 0
        self.headOffset: int = 0
        self.headOffsetVersion: int = 0
        self.isPassed: bool = False
        self.jobid: str = ""
        self.jumpTimePointList: list = []
        self.mid: str = ""
        self.objectId: str = ""
        self.otherInfo: str = ""
        self.playTime: int = 0
        self.property: dict = {}
        self.type: str = ""

        self.__dict__.update(data)

    def __repr__(self):
        return f'<Video {self.mid}>'


class Document:
    def __init__(self, data: dict):
        self.aid: int = 0
        self.begins: int = 0
        self.enc: str = ""
        self.ends: int = 0
        self.jtoken: str = ""
        self.mid: str = ""
        self.otherInfo: str = ""
        self.property: dict = {}
        self.type: str = ""

        self.__dict__.update(data)

    def __repr__(self):
        return f'<Document {self.mid}>'


class TaskFactory:
    @staticmethod
    def create(data: dict):
        task_type = data.get('type')
        if task_type == 'video':
            return Video(data)
        elif task_type == 'document':
            return Document(data)
        elif task_type == 'workid':
            raise NotImplementedError('Workid task is not implemented')
        else:
            raise Exception('Invalid task type')
