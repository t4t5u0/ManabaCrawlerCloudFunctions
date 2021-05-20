from dataclasses import dataclass

import requests as rq
from bs4 import BeautifulSoup, element
from datetime import datetime, timedelta, timezone


@dataclass
class Task:
    task_id: int
    task_title: str
    task_url: str
    course_id: int
    course_name: str
    state: str
    start: str
    end: str
    remain: str
    description: str

    def to_dict(self):
        return {
            "task_id": self.task_id,
            "task_title": self.task_title,
            "task_url": self.task_url,
            "course_id": self.course_id,
            "course_name": self.course_name,
            "state": self.state,
            "start": self.start,
            "end": self.end,
            "remain": self.remain,
            "description": self.description
        }


Tasks = list[Task]


def get_tasks(userid: str, password: str) -> Tasks:
    "タスクを取得する"

    base_url = 'https://manaba.fun.ac.jp/ct/'
    url = base_url + 'login'
    login_data = {
        'userid': userid,
        'password': password
    }

    session = rq.session()
    session.get(url)

    login = session.post(url, data=login_data)

    courses_have_tasks = Tasks()

    bs = BeautifulSoup(login.text, 'lxml')

    courses: list[element.Tag] = [course for course in bs.find_all(
        'td', class_='course')if course.find('a')]

    courses_have_tasks += _get_tasks(session, base_url, courses, '_report')
    courses_have_tasks += _get_tasks(session, base_url, courses, '_query')
    courses_have_tasks += _get_tasks(session, base_url, courses, '_survey')

    return list(map(lambda x: x.to_dict(), courses_have_tasks))


def _get_tasks(session: rq.Session, base_url: str, courses: list[element.Tag], query: str) -> Tasks:
    "タスクを取得する"
    un_submitted_tasks = Tasks()
    for course in courses:
        task_url: str = base_url + course.find('a').get('href') + query
        task = BeautifulSoup(session.get(task_url).text, 'lxml')
        course_name: str = task.find('a', id='coursename').get_text()
        course_id = int(task.find('a', id='coursename').get(
            'href').split('_')[-1])
        table = task.find_all('table', class_='stdlist')
        for row in table:
            row: element.Tag
            # 0 は項目、１以降が実際の課題
            tasks: list[element.Tag] = row.find_all('tr')[1:]

            for item in tasks:
                title: element.Tag
                state: element.Tag
                start: element.Tag
                end: element.Tag
                title, state, start, end = item.find_all('td')
                if is_unsubmitted(state, query):

                    id: str = title.find('a').get('href').split('_')[-1]
                    description = get_description(session, task_url, id)

                    end = end.get_text()
                    remain = get_remianing_time(end)
                    t = Task(
                        task_id=int(id),
                        task_title=title.find('a').get_text(),
                        task_url=f'{task_url}_{id}',
                        course_name=course_name,
                        course_id=course_id,
                        description=description,
                        state=state.find('span', class_='deadline').get_text(),
                        start=start.get_text(),
                        end=end,
                        remain=remain
                    )
                    un_submitted_tasks.append(t)
    return un_submitted_tasks


def is_unsubmitted(state: element.Tag, query: str) -> bool:
    "受付中かつ未提出"
    acception: str
    submission: str
    if query == '_report':
        if (div := state.find('div')) and (deadline := state.find('span', class_='deadline')):
            acception = div.get_text()
            submission = deadline.get_text()
        else:
            return False
    elif query in ['_query', '_survey']:
        if (td := state.get_text()) and (deadline := state.find('span', class_='deadline')):
            # 構造が悪い
            acception, submission = td.strip().split()
        else:
            return False
    else:
        print(f"{query=} unreachable!")
        return False

    if acception == '受付中' and submission == '未提出':
        return True
    return False


def get_description(session: rq.Session, task_url: str, id: str) -> str:
    "課題のページから説明を取得"
    url = task_url + '_' + id
    page = BeautifulSoup(session.get(url).text, 'lxml')
    table: element.Tag = page.find('table')
    if not table:
        return ""
    tr: element.Tag = table.find('tr', class_='row1')
    if not tr:
        return ""
    td: element.Tag = tr.find('td', class_='left')
    return td.text


def get_remianing_time(end: str) -> str:
    # タイムゾーンの生成
    JST = timezone(timedelta(hours=+9), 'JST')
    end_time = datetime.strptime(end, '%Y-%m-%d %H:%M').replace(tzinfo=JST)
    now_time = datetime.now(JST)
    residual = end_time - now_time
    return str(residual)
