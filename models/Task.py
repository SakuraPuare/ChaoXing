from utils import logger


class BaseTask:
    def __init__(self):
        self.aid: int = 0
        self.begins: int = 0
        self.ends: int = 0

        self.knowledgeid: str = ""
        self.courseid: str = ""
        self.clazzId: str = ""
        self.userid: str = ""
        self.reportUrl: str = ""

        self.otherInfo: str = ""
        self.property: dict = {}

    @property
    def types(self) -> str:
        return self.property.get('module', '').split('module')[-1]

    def __repr__(self):
        return f'<BaseTask {self.aid}>'


class VideoTask(BaseTask):
    def __init__(self, data: dict):
        super().__init__()
        self.customType: int = 0
        self.headOffset: int = 0
        self.headOffsetVersion: int = 0
        self.isPassed: bool = False
        self.jobid: str = ""
        self.jumpTimePointList: list = []
        self.mid: str = ""
        self.objectId: str = ""
        self.playTime: int = 0
        self.property: dict = {}
        self.type: str = ""

        self.__dict__.update(data)

    def __repr__(self):
        return f'<Video {self.mid}>'


class DocumentTask(BaseTask):
    def __init__(self, data: dict):
        super().__init__()
        self.enc: str = ""
        self.jtoken: str = ""
        self.jobid: str = ""
        self.mid: str = ""
        self.type: str = ""

        self.__dict__.update(data)

    def __repr__(self):
        return f'<Document {self.mid}>'


class BookTask(BaseTask):
    def __init__(self, data: dict):
        super().__init__()
        self.jtoken: str = ""
        self.mid: str = ""

        self.__dict__.update(data)

    @property
    def _from(self) -> str:
        return self.__getattribute__('from')

    @_from.setter
    def _from(self, value):
        self.__setattr__('from', value)

    def __repr__(self):
        return f'<Book {self.property.get("bookname", "")}>'


class ImageTask(BaseTask):
    def __init__(self, data: dict):
        super().__init__()

        self.__dict__.update(data)

    def __repr__(self):
        return f'<Image {self.aid}>'


class AudioTask(BaseTask):
    def __init__(self, data: dict):
        super().__init__()
        self.customType: int = 0
        self.headOffset: int = 0
        self.headOffsetVersion: int = 0
        self.isPassed: bool = False
        self.jobid: str = ""
        self.jumpTimePointList: list = []
        self.mid: str = ""
        self.objectId: str = ""
        self.playTime: int = 0
        self.type: str = ""

        self.__dict__.update(data)

    def __repr__(self):
        return f'<Audio {self.aid}>'


class TaskFactory:
    @staticmethod
    def create(data: dict) -> None | BaseTask:
        task_type: str = data.get('property', {}).get('module')

        if not task_type:
            return None

        if task_type.endswith('video'):
            return VideoTask(data)
        elif task_type.endswith('doc'):
            return DocumentTask(data)
        elif task_type.endswith('book'):
            return BookTask(data)
        elif task_type.endswith('image'):
            return ImageTask(data)
        elif task_type.endswith('audio'):
            return AudioTask(data)
        elif task_type.endswith('work'):
            logger.warning('Work task is not implemented')
            # raise NotImplementedError('Work task is not implemented')
        else:
            raise Exception('Invalid task type')
