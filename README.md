

Endpoints to upload historical files

* curl -X POST -F "file=@{path-file}" {ip}:{port}/departments/historical/
* curl -X POST -F "file=@{path-file}" {ip}:{port}/jobs/historical/
* curl -X POST -F "file=@{path-file}" {ip}:{port}/employees/historical/

Enpoints to calculate metrics

* curl  {ip}:{port}/metrics/number_employees_hired_by_department_by_job_by_quarter?year=2021
* curl  {ip}:{port}/metrics/departments_with_employees_hired_more_than_mean?year=2021
