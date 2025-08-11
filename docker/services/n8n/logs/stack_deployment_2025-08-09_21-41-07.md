### Comando Executado
```
docker-compose up -d
```

### Sa√≠da do Comando
```
 Container swaif_postgres_n8n  Running
 Container swaif_redis_n8n  Running
 Container swaif_n8n  Running
 Container swaif_n8n_importer  Created
 Container swaif_redis_n8n  Waiting
 Container swaif_postgres_n8n  Waiting
 Container swaif_redis_n8n  Healthy
 Container swaif_postgres_n8n  Healthy
 Container swaif_n8n  Waiting
 Container swaif_n8n  Healthy
 Container swaif_n8n_importer  Starting
 Container swaif_n8n_importer  Started
```
[2025-08-09 21:41:17] [SUCCESS] n8n Workflow iniciado com sucesso!
[2025-08-09 21:41:22] [INFO] Capturando logs detalhados de n8n Workflow...

### Logs Recentes (50 linhas)
```
swaif_n8n_importer  | Starting migration CreateTestMetricTable1732271325258
swaif_n8n           | Finished migration CreateTestDefinitionTable1730386903556
swaif_n8n_importer  | Finished migration CreateTestMetricTable1732271325258
swaif_n8n           | Starting migration AddDescriptionToTestDefinition1731404028106
swaif_n8n_importer  | Starting migration CreateTestRun1732549866705
swaif_n8n_importer  | Finished migration CreateTestRun1732549866705
swaif_redis_n8n     | 1:C 09 Aug 2025 21:35:34.700 * oO0OoO0OoO0Oo Redis is starting oO0OoO0OoO0Oo
swaif_n8n_importer  | Starting migration AddMockedNodesColumnToTestDefinition1733133775640
swaif_n8n_importer  | Finished migration AddMockedNodesColumnToTestDefinition1733133775640
swaif_postgres_n8n  | 
swaif_n8n_importer  | Starting migration AddManagedColumnToCredentialsTable1734479635324
swaif_postgres_n8n  | PostgreSQL Database directory appears to contain a database; Skipping initialization
swaif_postgres_n8n  | 
swaif_n8n_importer  | Finished migration AddManagedColumnToCredentialsTable1734479635324
swaif_postgres_n8n  | 2025-08-09 21:35:34.612 -03 [1] LOG:  starting PostgreSQL 15.13 on x86_64-pc-linux-musl, compiled by gcc (Alpine 14.2.0) 14.2.0, 64-bit
swaif_n8n_importer  | Starting migration AddStatsColumnsToTestRun1736172058779
swaif_n8n_importer  | Finished migration AddStatsColumnsToTestRun1736172058779
swaif_n8n           | Finished migration AddDescriptionToTestDefinition1731404028106
swaif_n8n           | Starting migration MigrateTestDefinitionKeyToString1731582748663
swaif_n8n           | Finished migration MigrateTestDefinitionKeyToString1731582748663
swaif_n8n           | Starting migration CreateTestMetricTable1732271325258
swaif_n8n           | Finished migration CreateTestMetricTable1732271325258
swaif_n8n           | Starting migration CreateTestRun1732549866705
swaif_n8n           | Finished migration CreateTestRun1732549866705
swaif_n8n           | Starting migration AddMockedNodesColumnToTestDefinition1733133775640
swaif_n8n           | Finished migration AddMockedNodesColumnToTestDefinition1733133775640
swaif_n8n           | Starting migration AddManagedColumnToCredentialsTable1734479635324
swaif_n8n           | Finished migration AddManagedColumnToCredentialsTable1734479635324
swaif_n8n           | Starting migration AddStatsColumnsToTestRun1736172058779
swaif_n8n           | Finished migration AddStatsColumnsToTestRun1736172058779
swaif_n8n           | Starting migration CreateTestCaseExecutionTable1736947513045
swaif_n8n           | Finished migration CreateTestCaseExecutionTable1736947513045
swaif_n8n           | Starting migration AddErrorColumnsToTestRuns1737715421462
swaif_postgres_n8n  | 2025-08-09 21:35:34.612 -03 [1] LOG:  listening on IPv4 address "0.0.0.0", port 5432
swaif_postgres_n8n  | 2025-08-09 21:35:34.612 -03 [1] LOG:  listening on IPv6 address "::", port 5432
swaif_n8n           | Finished migration AddErrorColumnsToTestRuns1737715421462
swaif_redis_n8n     | 1:C 09 Aug 2025 21:35:34.701 * Redis version=8.2.0, bits=64, commit=00000000, modified=1, pid=1, just started
swaif_redis_n8n     | 1:C 09 Aug 2025 21:35:34.701 * Configuration loaded
swaif_n8n_importer  | Starting migration CreateTestCaseExecutionTable1736947513045
swaif_n8n           | Starting migration CreateFolderTable1738709609940
swaif_redis_n8n     | 1:M 09 Aug 2025 21:35:34.701 * monotonic clock: POSIX clock_gettime
swaif_redis_n8n     | 1:M 09 Aug 2025 21:35:34.703 * Running mode=standalone, port=6379.
swaif_redis_n8n     | 1:M 09 Aug 2025 21:35:34.704 * Server initialized
swaif_redis_n8n     | 1:M 09 Aug 2025 21:35:34.704 * Loading RDB produced by version 8.2.0
swaif_n8n           | Finished migration CreateFolderTable1738709609940
swaif_n8n           | Starting migration CreateAnalyticsTables1739549398681
swaif_n8n_importer  | Finished migration CreateTestCaseExecutionTable1736947513045
swaif_n8n_importer  | Starting migration AddErrorColumnsToTestRuns1737715421462
swaif_n8n_importer  | Finished migration AddErrorColumnsToTestRuns1737715421462
swaif_postgres_n8n  | 2025-08-09 21:35:34.618 -03 [1] LOG:  listening on Unix socket "/var/run/postgresql/.s.PGSQL.5432"
swaif_n8n_importer  | Starting migration CreateFolderTable1738709609940
swaif_redis_n8n     | 1:M 09 Aug 2025 21:35:34.704 * RDB age 4 seconds
swaif_redis_n8n     | 1:M 09 Aug 2025 21:35:34.704 * RDB memory usage when created 0.64 Mb
swaif_postgres_n8n  | 2025-08-09 21:35:34.627 -03 [29] LOG:  database system was shut down at 2025-08-09 21:35:30 -03
swaif_postgres_n8n  | 2025-08-09 21:35:34.639 -03 [1] LOG:  database system is ready to accept connections
swaif_n8n_importer  | Finished migration CreateFolderTable1738709609940
swaif_n8n_importer  | Starting migration CreateAnalyticsTables1739549398681
swaif_n8n_importer  | Finished migration CreateAnalyticsTables1739549398681
swaif_n8n_importer  | Starting migration UpdateParentFolderIdColumn1740445074052
swaif_n8n_importer  | Finished migration UpdateParentFolderIdColumn1740445074052
swaif_postgres_n8n  | 2025-08-09 21:40:36.226 -03 [27] LOG:  checkpoint starting: time
swaif_n8n_importer  | Starting migration RenameAnalyticsToInsights1741167584277
swaif_n8n_importer  | Finished migration RenameAnalyticsToInsights1741167584277
swaif_n8n_importer  | Starting migration AddScopesColumnToApiKeys1742918400000
swaif_n8n_importer  | Finished migration AddScopesColumnToApiKeys1742918400000
swaif_n8n_importer  | Starting migration ClearEvaluation1745322634000
swaif_redis_n8n     | 1:M 09 Aug 2025 21:35:34.704 * Done loading RDB, keys loaded: 0, keys expired: 0.
swaif_redis_n8n     | 1:M 09 Aug 2025 21:35:34.704 * DB loaded from disk: 0.000 seconds
swaif_postgres_n8n  | 2025-08-09 21:41:06.115 -03 [27] LOG:  checkpoint complete: wrote 294 buffers (1.8%); 1 WAL file(s) added, 0 removed, 0 recycled; write=29.562 s, sync=0.113 s, total=29.890 s; sync files=468, longest=0.006 s, average=0.001 s; distance=2681 kB, estimate=2681 kB
swaif_n8n_importer  | Finished migration ClearEvaluation1745322634000
swaif_n8n_importer  | Starting migration AddWorkflowStatisticsRootCount1745587087521
swaif_n8n           | Finished migration CreateAnalyticsTables1739549398681
swaif_n8n           | Starting migration UpdateParentFolderIdColumn1740445074052
swaif_n8n           | Finished migration UpdateParentFolderIdColumn1740445074052
swaif_n8n           | Starting migration RenameAnalyticsToInsights1741167584277
swaif_n8n_importer  | Finished migration AddWorkflowStatisticsRootCount1745587087521
swaif_n8n_importer  | Starting migration AddWorkflowArchivedColumn1745934666076
swaif_n8n           | Finished migration RenameAnalyticsToInsights1741167584277
swaif_n8n           | Starting migration AddScopesColumnToApiKeys1742918400000
swaif_n8n           | Finished migration AddScopesColumnToApiKeys1742918400000
swaif_redis_n8n     | 1:M 09 Aug 2025 21:35:34.704 * Ready to accept connections tcp
swaif_n8n           | Starting migration ClearEvaluation1745322634000
swaif_n8n           | Finished migration ClearEvaluation1745322634000
swaif_n8n           | Starting migration AddWorkflowStatisticsRootCount1745587087521
swaif_n8n           | Finished migration AddWorkflowStatisticsRootCount1745587087521
swaif_n8n           | Starting migration AddWorkflowArchivedColumn1745934666076
swaif_n8n           | Finished migration AddWorkflowArchivedColumn1745934666076
swaif_n8n           | Starting migration DropRoleTable1745934666077
swaif_n8n_importer  | Finished migration AddWorkflowArchivedColumn1745934666076
swaif_n8n_importer  | Starting migration DropRoleTable1745934666077
swaif_n8n_importer  | Finished migration DropRoleTable1745934666077
swaif_n8n_importer  | Starting migration AddProjectDescriptionColumn1747824239000
swaif_n8n_importer  | Finished migration AddProjectDescriptionColumn1747824239000
swaif_n8n           | Finished migration DropRoleTable1745934666077
swaif_n8n_importer  | Starting migration AddLastActiveAtColumnToUser1750252139166
swaif_n8n           | Starting migration AddProjectDescriptionColumn1747824239000
swaif_n8n           | Finished migration AddProjectDescriptionColumn1747824239000
swaif_n8n           | Starting migration AddLastActiveAtColumnToUser1750252139166
swaif_n8n_importer  | Finished migration AddLastActiveAtColumnToUser1750252139166
swaif_n8n           | Finished migration AddLastActiveAtColumnToUser1750252139166
swaif_n8n           | 
swaif_n8n_importer  | 
swaif_n8n_importer  | There is a deprecation related to your environment variables. Please take the recommended actions to update your configuration:
swaif_n8n_importer  |  - N8N_RUNNERS_ENABLED -> Running n8n without task runners is deprecated. Task runners will be turned on by default in a future version. Please set `N8N_RUNNERS_ENABLED=true` to enable task runners now and avoid potential issues in the future. Learn more: https://docs.n8n.io/hosting/configuration/task-runners/
swaif_n8n           | There is a deprecation related to your environment variables. Please take the recommended actions to update your configuration:
swaif_n8n           |  - N8N_RUNNERS_ENABLED -> Running n8n without task runners is deprecated. Task runners will be turned on by default in a future version. Please set `N8N_RUNNERS_ENABLED=true` to enable task runners now and avoid potential issues in the future. Learn more: https://docs.n8n.io/hosting/configuration/task-runners/
swaif_n8n           | 
swaif_n8n           | [license SDK] Skipping renewal on init because renewal is not due yet or cert is not initialized
swaif_n8n           | Version: 1.103.2
swaif_n8n           | 
swaif_n8n_importer  | 
swaif_n8n_importer  | Successfully reset the database to default user state.
swaif_n8n_importer  | Permissions 0644 for n8n settings file /home/node/.n8n/config are too wide. This is ignored for now, but in the future n8n will attempt to change the permissions automatically. To automatically enforce correct permissions now set N8N_ENFORCE_SETTINGS_FILE_PERMISSIONS=true (recommended), or turn this check off set N8N_ENFORCE_SETTINGS_FILE_PERMISSIONS=false.
swaif_n8n_importer  | 
swaif_n8n_importer  | There is a deprecation related to your environment variables. Please take the recommended actions to update your configuration:
swaif_n8n_importer  |  - N8N_RUNNERS_ENABLED -> Running n8n without task runners is deprecated. Task runners will be turned on by default in a future version. Please set `N8N_RUNNERS_ENABLED=true` to enable task runners now and avoid potential issues in the future. Learn more: https://docs.n8n.io/hosting/configuration/task-runners/
swaif_n8n           | Editor is now accessible via:
swaif_n8n           | http://n8n:5678
swaif_n8n_importer  | 
swaif_n8n_importer  | Importing 0 workflows...
swaif_n8n_importer  | Successfully imported 0 workflows.
swaif_n8n_importer  | ‘£‡ Import conclu+°do
swaif_n8n_importer  | Permissions 0644 for n8n settings file /home/node/.n8n/config are too wide. This is ignored for now, but in the future n8n will attempt to change the permissions automatically. To automatically enforce correct permissions now set N8N_ENFORCE_SETTINGS_FILE_PERMISSIONS=true (recommended), or turn this check off set N8N_ENFORCE_SETTINGS_FILE_PERMISSIONS=false.
```

### Status dos Containers
```
NAME                 IMAGE                COMMAND                  SERVICE              CREATED         STATUS                   PORTS
swaif_n8n            n8nio/n8n:latest     "tini -- /docker-ent‘«™"   swaif_n8n            5 minutes ago   Up 5 minutes (healthy)   0.0.0.0:5678->5678/tcp
swaif_n8n_importer   n8nio/n8n:latest     "/bin/sh -lc ' if [ ‘«™"   swaif_n8n_importer   5 minutes ago   Up 6 seconds             5678/tcp
swaif_postgres_n8n   postgres:15-alpine   "docker-entrypoint.s‘«™"   swaif_postgres_n8n   5 minutes ago   Up 5 minutes (healthy)   0.0.0.0:5434->5432/tcp
swaif_redis_n8n      redis:alpine         "docker-entrypoint.s‘«™"   swaif_redis_n8n      5 minutes ago   Up 5 minutes (healthy)   0.0.0.0:6381->6379/tcp
```
[2025-08-09 21:41:23] [INFO] Verificando sa√∫de dos containers...
