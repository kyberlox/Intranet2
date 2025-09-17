from src.base.pSQL.objects.DepartmentModel import DepartmentModel

dep = DepartmentModel(Id=456).find_dep_by_id()
print(dep)