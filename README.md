# grai-core

## Desired Features

- Data Lineage
  - source system to final warehouse table
  - transformations applied at each step
  - dependant applications (dashboards, ML apps, etc...)
- Update timestamps
- Execution engine (airflow, dbt, etc...)
- Execution time (query duration, job duration, etc...)
- ability to reconstitute the graph at any point in the past (i.e. data history)