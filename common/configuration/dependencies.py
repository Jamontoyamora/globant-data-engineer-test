from fastapi import Depends
from core.use_case.impl.data_use_case_impl import DataUseCaseImpl
from core.use_case.impl.backup_use_case_impl import BackupUseCaseImpl
from core.use_case.impl.report_use_case_impl import ReportUseCaseImpl
from controller.service.impl.data_service_impl import DataServiceImpl
from controller.service.impl.backup_service_impl import BackupServiceImpl
from controller.service.impl.report_service_impl import ReportServiceImpl
from data_provider.provider.impl.department_provider_impl import DepartmentProviderImpl
from data_provider.provider.impl.job_provider_impl import JobProviderImpl
from data_provider.provider.impl.employee_provider_impl import EmployeeProviderImpl

def get_department_provider():
    return DepartmentProviderImpl()

def get_job_provider():
    return JobProviderImpl()

def get_employee_provider():
    return EmployeeProviderImpl()

def get_data_use_case(
    department_provider: DepartmentProviderImpl = Depends(get_department_provider),
    job_provider: JobProviderImpl = Depends(get_job_provider),
    employee_provider: EmployeeProviderImpl = Depends(get_employee_provider)
):
    return DataUseCaseImpl(department_provider, job_provider, employee_provider)

def get_backup_use_case(
    department_provider: DepartmentProviderImpl = Depends(get_department_provider),
    job_provider: JobProviderImpl = Depends(get_job_provider),
    employee_provider: EmployeeProviderImpl = Depends(get_employee_provider)
):
    return BackupUseCaseImpl(department_provider, job_provider, employee_provider)

def get_report_use_case(
    employee_provider: EmployeeProviderImpl = Depends(get_employee_provider),
    department_provider: DepartmentProviderImpl = Depends(get_department_provider),
    job_provider: JobProviderImpl = Depends(get_job_provider)
):
    return ReportUseCaseImpl(employee_provider, department_provider, job_provider)

def get_data_service(
    data_use_case: DataUseCaseImpl = Depends(get_data_use_case)
):
    return DataServiceImpl(data_use_case)

def get_backup_service(
    backup_use_case: BackupUseCaseImpl = Depends(get_backup_use_case)
):
    return BackupServiceImpl(backup_use_case)

def get_report_service(
    report_use_case: ReportUseCaseImpl = Depends(get_report_use_case)
):
    return ReportServiceImpl(report_use_case)
