import asyncio
import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from queries.core import SyncCore, AsyncCore
from queries.orm import SyncORM, AsyncORM

# SyncCore.update_worker()
# SyncCore.insert_resumes()
# SyncCore.select_resumes_avg_compensation()
# SyncCore.insert_additional_resumes()
# SyncCore.join_cte_subquery_window_func()

# ORM
if "--orm" in sys.argv and "--sync" in sys.argv:
    SyncORM.create_tables()
    SyncORM.insert_workers()
    SyncORM.update_worker()
    SyncORM.insert_resumes()
    SyncORM.select_resumes_avg_compensation()
    SyncORM.insert_additional_resumes()
    SyncORM.join_cte_subquery_window_func()
    SyncORM.select_workers_with_lazy_reletaionship()
    SyncORM.select_workers_with_joined_reletaionship()
    SyncORM.select_workers_with_selection_reletaionship()
    SyncORM.select_workers_with_condition_relationship()
    SyncORM.select_workers_with_condition_relationship_contains_eager()

# # ========== ASYNC ==========

# # CORE
# await AsyncCore.update_worker()
# await AsyncCore.insert_resumes()
# await AsyncCore.select_resumes_avg_compensation()
# await AsyncCore.insert_additional_resumes()
# await AsyncCore.join_cte_subquery_window_func()

# # ORM
# if "--orm" in sys.argv and "--async" in sys.argv:
#     await AsyncORM.update_worker()
#     await AsyncORM.insert_resumes()
#     await AsyncORM.select_resumes_avg_compensation()
#     await AsyncORM.insert_additional_resumes()
#     await AsyncORM.join_cte_subquery_window_func()

if __name__ == "__main__":
    pass
