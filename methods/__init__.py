import hashlib
import json
import re
from datetime import datetime

from httpx import Response

from models.Course import Course, Unit, Chapter, Catalog
from models.Task import TaskFactory, BaseTask, VideoTask, DocumentTask
from utils import get_soup
from utils import httpx, logger


def get_user_course() -> list[Course]:
    course = httpx.get('https://mooc2-ans.chaoxing.com/mooc2-ans/visit/courses/list')
    soup = get_soup(course.text)
    course_list = []
    for c in soup.find_all('li', {'class': 'course'}):
        name = c.find('h3').get_text()
        ids = c.find('input', {'class': 'courseId'}).get('value')
        class_ids = c.find('input', {'class': 'clazzId'}).get('value')
        info = [i.get_text().strip() for i in c.find_all('p')]
        is_finish = True if c.find('a', {'class': 'not-open-tip'}) else False
        if len(info) == 3:
            desc, teacher, classes = info
        else:
            desc, teacher, _, classes = info
        classes = classes.split('班级：')[-1]
        course_list.append(Course(name, ids, class_ids, desc, teacher, classes, is_finish))

    return course_list


def get_course_catalog(course: Course) -> Catalog:
    url = (f'https://mooc2-ans.chaoxing.com/mooc2-ans/mycourse/studentcourse?'
           f'courseid={course.ids}&clazzid={course.class_ids}')
    course_info = httpx.get(url)
    soup = get_soup(course_info.text)
    catalog = Catalog()
    for unit in soup.find_all('div', {'class': 'chapter_unit'}):
        u = Unit(unit.find('div', {'class': 'catalog_name'}).get_text().strip())
        for chapter in unit.find_all('li'):
            tasks = chapter.find('div', {'class': 'catalog_task'}).find('input')
            if tasks:
                tasks = tasks.get('value')
            else:
                tasks = 0
            ids = chapter.find('input').get('value')
            c = Chapter(chapter.find('div', {'class': 'catalog_name'}).get_text().strip(), int(tasks), ids)
            u.add_chapter(c)
        catalog.add_unit(u)

    return catalog


def get_chapter_tasks(course: Course, chapter: Chapter) -> list[BaseTask]:
    count = get_chapter_task_page_count(course, chapter)
    task_list = []
    for page in range(count):
        url = (f'https://mooc1.chaoxing.com/knowledge/cards?'
               f'clazzid={course.class_ids}&courseid={course.ids}&knowledgeid={chapter.ids}&num={page}')
        rsp = httpx.get(url)
        try:
            data = re.findall(r'mArg = ({[\s\S]*);\n}catch', rsp.text)
            if not data:
                continue
            else:
                data = data[-1]

            json_data = json.loads(data)
            print(json_data.get('defaults').get('reportUrl'))
            root_data = {}
            for k, v in json_data.items():
                if k == 'attachments':
                    continue
                if isinstance(v, dict):
                    root_data.update(v)

            for task in json_data.get('attachments', []):
                task.update(root_data)
                t = TaskFactory.create(task)
                if t:
                    task_list.append(t)

        except Exception as e:
            logger.error(e)
            continue
    return task_list


def get_chapter_task_page_count(course: Course, chapter: Chapter) -> int:
    url = (f'https://mooc1.chaoxing.com/mycourse/studentstudyAjax?'
           f'courseId={course.ids}&clazzid={course.class_ids}&chapterId={chapter.ids}')
    rsp = httpx.get(url)
    soup = get_soup(rsp.text)
    return int(soup.find('input', {'id': 'cardcount'}).get('value'))


def get_chapters(catalog: Catalog) -> list[Chapter]:
    for u in catalog:
        for c in u:
            yield c


def get_uncompleted_chapters(catalog: Catalog) -> list[Chapter]:
    for u in catalog:
        for c in u:
            if c.tasks > 0:
                yield c


def solve_video_task(task: VideoTask) -> None:
def get_video_status(object_id: str) -> Response:
    url = (f'https://mooc1-1.chaoxing.com/ananas/status/{object_id}'
           f'?k=&flag=normal&_dc={int(datetime.now().timestamp() * 1000)}')
    headers = {'Referer': 'https://mooc1.chaoxing.com/ananas/modules/video/index.html'}
    resp = httpx.get(url, headers=headers)
    return resp
    pass


def solve_document_task(task: DocumentTask) -> bool:
    url = (f'https://mooc1-2.chaoxing.com/ananas/job/document?'
           f'jobid={task.jobid}&knowledgeid={task.knowledgeid}&courseid={task.courseid}&clazzid={task.clazzId}'
           f'&jtoken={task.jtoken}&_dc={int(datetime.now().timestamp() * 1000)}')
    resp = httpx.get(url)
    status = resp.json().get('status')
    if status:
        logger.info(f'任务点"{task.property.get("name")}"完成成功')
    else:
        logger.error(f'任务点"{task.property.get("name")}"完成失败')
    return status


def solve_task(task: BaseTask) -> bool:
    if isinstance(task, VideoTask):
        return solve_video_task(task)
    elif isinstance(task, DocumentTask):
        return solve_document_task(task)
    else:
        return False
