from sqlalchemy import Integer, and_, text, insert, select, update, func, cast
from sqlalchemy.orm import aliased, joinedload, selectinload, contains_eager
# aliased --- нужен лишь когда появляется та же таблица в коде, 
# чтобы создать независимый экземлпяр и иметь возможность к нем применять условия, соединения
from database import sync_engine, async_engine, session_factory, async_session_factory
from models import Base, WorkLoad, WorkersORM, ResumesORM


class SyncORM:
    @staticmethod
    def create_tables():
        sync_engine.echo = False
        Base.metadata.drop_all(sync_engine)
        Base.metadata.create_all(sync_engine)
        sync_engine.echo = True

    @staticmethod
    def insert_workers():
        with session_factory() as session:
            worker_bobr = WorkersORM(username="Bobr")
            worker_volk = WorkersORM(username="Volk")
            session.add_all([worker_bobr, worker_volk,]) # нет изменений в базе, в памяти (сессии)
            session.flush() # отправляет изменения в базу, но не завершить запрос
            session.commit()

    @staticmethod
    def select_workers():
        with session_factory() as session:
            query = select(WorkersORM)
            result = session.execute(query)
            workers = result.scalars().all()
            print(f"{workers=}")

    @staticmethod
    def update_worker(worker_id: int = 2, new_username: str = "Misha"):
        with session_factory() as session:
            worker_volk = session.get(WorkersORM, worker_id)
            worker_volk.username = new_username
            session.refresh(worker_volk)
            session.commit()

    
    @staticmethod
    def insert_resumes():
        with session_factory() as session:
            resume_jack_1 = ResumesORM(
                title="Python Junior Developer", compensation=50000, workload=WorkLoad.fulltime, worker_id=1) 
            resume_jack_2 = ResumesORM(
                title="Python Разработчик", compensation=150000, workload=WorkLoad.fulltime, worker_id=1) 
            resume_michael_1 = ResumesORM(
                title="Python Data Engineer", compensation=250000, workload=WorkLoad. parttime, worker_id=2) 
            resume_michael_2 = ResumesORM(
                title="Data Scientist", compensation=300000, workload=WorkLoad.fulltime, worker_id=2) 
            session.add_all([resume_jack_1, resume_jack_2, 
                            resume_michael_1, resume_michael_2])
            session.commit() 
            sync_engine.echo = True

    @staticmethod
    def select_resumes_avg_compensation(like_language: str = "Python"):
        with session_factory() as session:
            avg_comp = cast(func.avg(ResumesORM.compensation), Integer).label("avg_compensation") # FUNC - любая функция, что есть так же на СУБД, в том числе если добвить самостоятельно

            query = (
                select(
                    ResumesORM.workload,
                    avg_comp, 
                    )
                    .select_from(ResumesORM)
                    .filter(and_(
                        ResumesORM.title.contains(like_language), # contains - ставит %слово%
                        ResumesORM.compensation > 40000,
                    ))
                    .group_by(ResumesORM.workload)
                    .having(avg_comp > 70000)
            )
            print(query.compile(compile_kwargs={"literal_binds": True}))
            res = session.execute(query)
            result = res.all()
            print(result[0].avg_compensation)

    @staticmethod
    def insert_additional_resumes():
        with session_factory() as session:
            workers = [
                {"username": "Artem"},  # id 3
                {"username": "Roman"},  # id 4
                {"username": "Petr"},   # id 5
            ]
            resumes = [
                {"title": "Python программист", "compensation": 60000, "workload": "fulltime", "worker_id": 3},
                {"title": "Machine Learning Engineer", "compensation": 70000, "workload": "parttime", "worker_id": 3},
                {"title": "Python Data Scientist", "compensation": 80000, "workload": "parttime", "worker_id": 4},
                {"title": "Python Analyst", "compensation": 90000, "workload": "fulltime", "worker_id": 4},
                {"title": "Python Junior Developer", "compensation": 100000, "workload": "fulltime", "worker_id": 5},
            ]
            session.execute(insert(WorkersORM).values(workers))
            session.execute(insert(ResumesORM).values(resumes))
            session.commit()

    @staticmethod
    def join_cte_subquery_window_func():
        """WITH helper2 AS (
            SELECT *, compensation - avg_workload_compensation AS compensation_diff
            FROM (
                SELECT
                    w.id,
                    w.username,
                    r.compensation,
                    r.workload,
                    avg(r.compensation) OVER (PARTITION BY workload)::int AS avg_workload_compensation
                FROM resumes r
                JOIN workers w ON r.worker_id = w.id
            ) helper1
        )
        SELECT * FROM helper2
        ORDER BY compensation_diff DESC;"""
        with session_factory() as session:
            r = ResumesORM
            w = WorkersORM
            subq = (
                select(
                    r, 
                    w, 
                    func.avg(r.compensation).over(partition_by=r.workload).cast(Integer).label("avg_workload_compensation"),      
                )
                .select_from(r)
                .join(w, r.worker_id == w.id).subquery("helper1") # авто название = anon_1
            )
            cte = ( # включает subq
                select(
                    subq.c.id,
                    subq.c.username,
                    subq.c.compensation,
                    subq.c.workload,
                    subq.c.avg_workload_compensation,
                    (subq.c.compensation - subq.c.avg_workload_compensation).label("compensation_diff")
                )
                .cte("helper2")
            ) 
            query = (
                select(cte)
                .order_by(cte.c.compensation_diff.desc())
            )

            print(query.compile(compile_kwargs={"literal_binds": True}))
            res = session.execute(query)
            result = res.all()
            print(f"{len(result)=}. {result=}")


    # Мноежство запросов O(n + 1) ; 1 = Select начальный
    @staticmethod
    def select_workers_with_lazy_reletaionship():
        with session_factory() as session:
            query = (
                select(WorkersORM)
            )

            res = session.execute(query)
            result = res.scalars().all() # преобразует результат с одной колонкой в "плоский" [ obj1, obj2, obj3 ] список значений, отбрасывая SQLAlchemy-обёртки Row и кортежи.

            worker_1_resumes = result[0].resumes
            print(worker_1_resumes)

            worker_2_resumes = result[1].resumes
            print(worker_2_resumes)

    # подходит для Many To One m2o : One to One o2o
    @staticmethod
    def select_workers_with_joined_reletaionship():
        with session_factory() as session:
            query = (
                select(WorkersORM)
                .options(joinedload(WorkersORM.resumes))
            )

            res = session.execute(query)
            result = res.unique().scalars().all() # scalars преобразует результат с одной колонкой в "плоский" [ obj1, obj2, obj3 ] список значений, отбрасывая SQLAlchemy-обёртки Row и кортежи.
            # unique запрос на уровне питона-алхимии и не в базу, чтобы отсеить уникальные первичные ключи 
            # если к одному ключу много всего, то будет их список вложен к одному ключу (на уровне пайтон лишь)
            worker_1_resumes = result[0].resumes
            print(worker_1_resumes)

            worker_2_resumes = result[1].resumes
            print(worker_2_resumes)
 

    # подходит для Many to Many m2m : One to Many o2m
    @staticmethod
    def select_workers_with_selection_reletaionship():
        with session_factory() as session:
            query = (
                select(WorkersORM)
                .options(selectinload(WorkersORM.resumes))
            )

            res = session.execute(query)
            result = res.unique().scalars().all() 

            worker_1_resumes = result[0].resumes
            # print(worker_1_resumes)

            worker_2_resumes = result[1].resumes
            # print(worker_2_resumes)

    @staticmethod
    def select_workers_with_condition_relationship():
        with session_factory() as session:
            query = (
                select(WorkersORM)
                .options(selectinload(WorkersORM.resumes_parttime))
            )
            
            res = session.execute(query)
            result = res.unique().scalars().all() 
            print(result)


    @staticmethod
    def select_workers_with_condition_relationship_contains_eager():
        with session_factory() as session:
            query = (
                select(WorkersORM)
                .join(WorkersORM.resumes)
                .options(contains_eager(WorkersORM.resumes)) 
                .filter(ResumesORM.workload == 'parttime')
                # contains_eager + filter -- мы говорим что не нужно делать отдельный SQL-запрос для подгрузки отношения resumes 
                # — мы уже сделали JOIN и получили нужные данные в этом же запросе. Просто разложи их по нужным полям объектов (как? Благодаря .filter 
                # что отберёт данные которые нужно разлаживать).
            )

            res = session.execute(query)
            result = res.unique().scalars().all() 
            print(result)
            

class AsyncORM:
    @staticmethod
    async def create_tables():
        async_engine.echo = False
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)
        async_engine.echo = True

    @staticmethod
    async def insert_workers():
        async with async_session_factory() as session:
            worker_bobr = WorkersORM(username="Bobr")
            worker_volk = WorkersORM(username="Volk")
            session.add_all([worker_bobr, worker_volk])
            await session.commit()

