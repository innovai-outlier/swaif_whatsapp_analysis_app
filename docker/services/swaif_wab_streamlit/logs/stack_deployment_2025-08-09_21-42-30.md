### Comando Executado
```
docker-compose up -d
```

### Saída do Comando
```
 Container swaif_postgres  Running
 Container swaif_streamlit_app  Created
 Container swaif_postgres  Waiting
 Container swaif_postgres  Healthy
 Container swaif_streamlit_app  Starting
 Container swaif_streamlit_app  Started
```
[2025-08-09 21:42:46] [SUCCESS] SWAIF WAB Streamlit iniciado com sucesso!
[2025-08-09 21:42:51] [INFO] Capturando logs detalhados de SWAIF WAB Streamlit...

### Logs Recentes (50 linhas)
```
swaif_postgres       | creating subdirectories ... ok
swaif_streamlit_app  | Requirement already satisfied: six>=1.5 in /usr/local/lib/python3.11/site-packages (from python-dateutil>=2.8.2->pandas<3,>=1.4.0->streamlit) (1.17.0)
swaif_postgres       | selecting dynamic shared memory implementation ... posix
swaif_postgres       | selecting default max_connections ... 100
swaif_postgres       | selecting default shared_buffers ... 128MB
swaif_postgres       | selecting default time zone ... America/Sao_Paulo
swaif_postgres       | creating configuration files ... ok
swaif_streamlit_app  | WARNING: Running pip as the 'root' user can result in broken permissions and conflicting behaviour with the system package manager, possibly rendering your system unusable. It is recommended to use a virtual environment instead: https://pip.pypa.io/warnings/venv. Use the --root-user-action option if you know what you are doing and want to suppress this warning.
swaif_postgres       | running bootstrap script ... ok
swaif_postgres       | sh: locale: not found
swaif_streamlit_app  | Usage: streamlit run [OPTIONS] TARGET [ARGS]...
swaif_streamlit_app  | Try 'streamlit run --help' for help.
swaif_streamlit_app  | 
swaif_postgres       | 2025-08-09 21:27:04.453 -03 [36] WARNING:  no usable system locales were found
swaif_postgres       | performing post-bootstrap initialization ... ok
swaif_postgres       | syncing data to disk ... ok
swaif_postgres       | 
swaif_postgres       | 
swaif_postgres       | Success. You can now start the database server using:
swaif_postgres       | 
swaif_postgres       | initdb: warning: enabling "trust" authentication for local connections
swaif_streamlit_app  | Error: Invalid value: File does not exist: run_swai.py
swaif_postgres       | initdb: hint: You can change this by editing pg_hba.conf or using the option -A, or --auth-local and --auth-host, the next time you run initdb.
swaif_postgres       |     pg_ctl -D /var/lib/postgresql/data -l logfile start
swaif_postgres       | 
swaif_postgres       | waiting for server to start....2025-08-09 21:27:05.492 -03 [42] LOG:  starting PostgreSQL 15.13 on x86_64-pc-linux-musl, compiled by gcc (Alpine 14.2.0) 14.2.0, 64-bit
swaif_postgres       | 2025-08-09 21:27:05.496 -03 [42] LOG:  listening on Unix socket "/var/run/postgresql/.s.PGSQL.5432"
swaif_postgres       | 2025-08-09 21:27:05.506 -03 [45] LOG:  database system was shut down at 2025-08-09 21:27:05 -03
swaif_streamlit_app  | Requirement already satisfied: pip in /usr/local/lib/python3.11/site-packages (25.2)
swaif_streamlit_app  | WARNING: Running pip as the 'root' user can result in broken permissions and conflicting behaviour with the system package manager, possibly rendering your system unusable. It is recommended to use a virtual environment instead: https://pip.pypa.io/warnings/venv. Use the --root-user-action option if you know what you are doing and want to suppress this warning.
swaif_streamlit_app  | Requirement already satisfied: streamlit in /usr/local/lib/python3.11/site-packages (1.48.0)
swaif_streamlit_app  | Requirement already satisfied: altair!=5.4.0,!=5.4.1,<6,>=4.0 in /usr/local/lib/python3.11/site-packages (from streamlit) (5.5.0)
swaif_streamlit_app  | Requirement already satisfied: blinker<2,>=1.5.0 in /usr/local/lib/python3.11/site-packages (from streamlit) (1.9.0)
swaif_streamlit_app  | Requirement already satisfied: cachetools<7,>=4.0 in /usr/local/lib/python3.11/site-packages (from streamlit) (6.1.0)
swaif_postgres       | 2025-08-09 21:27:05.516 -03 [42] LOG:  database system is ready to accept connections
swaif_postgres       |  done
swaif_postgres       | server started
swaif_postgres       | CREATE DATABASE
swaif_streamlit_app  | Requirement already satisfied: click<9,>=7.0 in /usr/local/lib/python3.11/site-packages (from streamlit) (8.2.1)
swaif_streamlit_app  | Requirement already satisfied: numpy<3,>=1.23 in /usr/local/lib/python3.11/site-packages (from streamlit) (2.3.2)
swaif_streamlit_app  | Requirement already satisfied: packaging<26,>=20 in /usr/local/lib/python3.11/site-packages (from streamlit) (25.0)
swaif_streamlit_app  | Requirement already satisfied: pandas<3,>=1.4.0 in /usr/local/lib/python3.11/site-packages (from streamlit) (2.3.1)
swaif_postgres       | 
swaif_postgres       | 
swaif_postgres       | /usr/local/bin/docker-entrypoint.sh: ignoring /docker-entrypoint-initdb.d/*
swaif_postgres       | 
swaif_postgres       | waiting for server to shut down....2025-08-09 21:27:05.688 -03 [42] LOG:  received fast shutdown request
swaif_postgres       | 2025-08-09 21:27:05.692 -03 [42] LOG:  aborting any active transactions
swaif_postgres       | 2025-08-09 21:27:05.694 -03 [42] LOG:  background worker "logical replication launcher" (PID 48) exited with exit code 1
swaif_streamlit_app  | Requirement already satisfied: pillow<12,>=7.1.0 in /usr/local/lib/python3.11/site-packages (from streamlit) (11.3.0)
swaif_streamlit_app  | Requirement already satisfied: protobuf<7,>=3.20 in /usr/local/lib/python3.11/site-packages (from streamlit) (6.31.1)
swaif_streamlit_app  | Requirement already satisfied: pyarrow>=7.0 in /usr/local/lib/python3.11/site-packages (from streamlit) (21.0.0)
swaif_streamlit_app  | Requirement already satisfied: requests<3,>=2.27 in /usr/local/lib/python3.11/site-packages (from streamlit) (2.32.4)
swaif_streamlit_app  | Requirement already satisfied: tenacity<10,>=8.1.0 in /usr/local/lib/python3.11/site-packages (from streamlit) (9.1.2)
swaif_streamlit_app  | Requirement already satisfied: toml<2,>=0.10.1 in /usr/local/lib/python3.11/site-packages (from streamlit) (0.10.2)
swaif_postgres       | 2025-08-09 21:27:05.695 -03 [43] LOG:  shutting down
swaif_postgres       | 2025-08-09 21:27:05.698 -03 [43] LOG:  checkpoint starting: shutdown immediate
swaif_streamlit_app  | Requirement already satisfied: typing-extensions<5,>=4.4.0 in /usr/local/lib/python3.11/site-packages (from streamlit) (4.14.1)
swaif_streamlit_app  | Requirement already satisfied: watchdog<7,>=2.1.5 in /usr/local/lib/python3.11/site-packages (from streamlit) (6.0.0)
swaif_streamlit_app  | Requirement already satisfied: gitpython!=3.1.19,<4,>=3.0.7 in /usr/local/lib/python3.11/site-packages (from streamlit) (3.1.45)
swaif_streamlit_app  | Requirement already satisfied: pydeck<1,>=0.8.0b4 in /usr/local/lib/python3.11/site-packages (from streamlit) (0.9.1)
swaif_streamlit_app  | Requirement already satisfied: tornado!=6.5.0,<7,>=6.0.3 in /usr/local/lib/python3.11/site-packages (from streamlit) (6.5.2)
swaif_streamlit_app  | Requirement already satisfied: jinja2 in /usr/local/lib/python3.11/site-packages (from altair!=5.4.0,!=5.4.1,<6,>=4.0->streamlit) (3.1.6)
swaif_streamlit_app  | Requirement already satisfied: jsonschema>=3.0 in /usr/local/lib/python3.11/site-packages (from altair!=5.4.0,!=5.4.1,<6,>=4.0->streamlit) (4.25.0)
swaif_streamlit_app  | Requirement already satisfied: narwhals>=1.14.2 in /usr/local/lib/python3.11/site-packages (from altair!=5.4.0,!=5.4.1,<6,>=4.0->streamlit) (2.0.1)
swaif_streamlit_app  | Requirement already satisfied: gitdb<5,>=4.0.1 in /usr/local/lib/python3.11/site-packages (from gitpython!=3.1.19,<4,>=3.0.7->streamlit) (4.0.12)
swaif_streamlit_app  | Requirement already satisfied: smmap<6,>=3.0.1 in /usr/local/lib/python3.11/site-packages (from gitdb<5,>=4.0.1->gitpython!=3.1.19,<4,>=3.0.7->streamlit) (5.0.2)
swaif_streamlit_app  | Requirement already satisfied: python-dateutil>=2.8.2 in /usr/local/lib/python3.11/site-packages (from pandas<3,>=1.4.0->streamlit) (2.9.0.post0)
swaif_postgres       | 2025-08-09 21:27:05.799 -03 [43] LOG:  checkpoint complete: wrote 921 buffers (5.6%); 0 WAL file(s) added, 0 removed, 0 recycled; write=0.022 s, sync=0.069 s, total=0.105 s; sync files=301, longest=0.012 s, average=0.001 s; distance=4239 kB, estimate=4239 kB
swaif_postgres       | 2025-08-09 21:27:05.808 -03 [42] LOG:  database system is shut down
swaif_postgres       |  done
swaif_streamlit_app  | Requirement already satisfied: pytz>=2020.1 in /usr/local/lib/python3.11/site-packages (from pandas<3,>=1.4.0->streamlit) (2025.2)
swaif_streamlit_app  | Requirement already satisfied: tzdata>=2022.7 in /usr/local/lib/python3.11/site-packages (from pandas<3,>=1.4.0->streamlit) (2025.2)
swaif_streamlit_app  | Requirement already satisfied: charset_normalizer<4,>=2 in /usr/local/lib/python3.11/site-packages (from requests<3,>=2.27->streamlit) (3.4.3)
swaif_postgres       | server stopped
swaif_postgres       | 
swaif_postgres       | PostgreSQL init process complete; ready for start up.
swaif_postgres       | 
swaif_postgres       | 2025-08-09 21:27:05.925 -03 [1] LOG:  starting PostgreSQL 15.13 on x86_64-pc-linux-musl, compiled by gcc (Alpine 14.2.0) 14.2.0, 64-bit
swaif_postgres       | 2025-08-09 21:27:05.925 -03 [1] LOG:  listening on IPv4 address "0.0.0.0", port 5432
swaif_streamlit_app  | Requirement already satisfied: idna<4,>=2.5 in /usr/local/lib/python3.11/site-packages (from requests<3,>=2.27->streamlit) (3.10)
swaif_streamlit_app  | Requirement already satisfied: urllib3<3,>=1.21.1 in /usr/local/lib/python3.11/site-packages (from requests<3,>=2.27->streamlit) (2.5.0)
swaif_streamlit_app  | Requirement already satisfied: certifi>=2017.4.17 in /usr/local/lib/python3.11/site-packages (from requests<3,>=2.27->streamlit) (2025.8.3)
swaif_postgres       | 2025-08-09 21:27:05.925 -03 [1] LOG:  listening on IPv6 address "::", port 5432
swaif_postgres       | 2025-08-09 21:27:05.932 -03 [1] LOG:  listening on Unix socket "/var/run/postgresql/.s.PGSQL.5432"
swaif_postgres       | 2025-08-09 21:27:05.941 -03 [58] LOG:  database system was shut down at 2025-08-09 21:27:05 -03
swaif_postgres       | 2025-08-09 21:27:05.949 -03 [1] LOG:  database system is ready to accept connections
swaif_streamlit_app  | Requirement already satisfied: MarkupSafe>=2.0 in /usr/local/lib/python3.11/site-packages (from jinja2->altair!=5.4.0,!=5.4.1,<6,>=4.0->streamlit) (3.0.2)
swaif_postgres       | 2025-08-09 21:32:07.701 -03 [56] LOG:  checkpoint starting: time
swaif_streamlit_app  | Requirement already satisfied: attrs>=22.2.0 in /usr/local/lib/python3.11/site-packages (from jsonschema>=3.0->altair!=5.4.0,!=5.4.1,<6,>=4.0->streamlit) (25.3.0)
swaif_postgres       | 2025-08-09 21:32:12.074 -03 [56] LOG:  checkpoint complete: wrote 44 buffers (0.3%); 0 WAL file(s) added, 0 removed, 0 recycled; write=4.345 s, sync=0.013 s, total=4.373 s; sync files=12, longest=0.007 s, average=0.002 s; distance=252 kB, estimate=252 kB
swaif_streamlit_app  | Requirement already satisfied: jsonschema-specifications>=2023.03.6 in /usr/local/lib/python3.11/site-packages (from jsonschema>=3.0->altair!=5.4.0,!=5.4.1,<6,>=4.0->streamlit) (2025.4.1)
swaif_streamlit_app  | Requirement already satisfied: referencing>=0.28.4 in /usr/local/lib/python3.11/site-packages (from jsonschema>=3.0->altair!=5.4.0,!=5.4.1,<6,>=4.0->streamlit) (0.36.2)
swaif_streamlit_app  | Requirement already satisfied: rpds-py>=0.7.1 in /usr/local/lib/python3.11/site-packages (from jsonschema>=3.0->altair!=5.4.0,!=5.4.1,<6,>=4.0->streamlit) (0.27.0)
swaif_streamlit_app  | Requirement already satisfied: six>=1.5 in /usr/local/lib/python3.11/site-packages (from python-dateutil>=2.8.2->pandas<3,>=1.4.0->streamlit) (1.17.0)
swaif_streamlit_app  | WARNING: Running pip as the 'root' user can result in broken permissions and conflicting behaviour with the system package manager, possibly rendering your system unusable. It is recommended to use a virtual environment instead: https://pip.pypa.io/warnings/venv. Use the --root-user-action option if you know what you are doing and want to suppress this warning.
swaif_streamlit_app  | Usage: streamlit run [OPTIONS] TARGET [ARGS]...
swaif_streamlit_app  | Try 'streamlit run --help' for help.
swaif_streamlit_app  | 
swaif_streamlit_app  | Error: Invalid value: File does not exist: run_swai.py
```

### Status dos Containers
```
NAME             IMAGE                COMMAND                  SERVICE          CREATED          STATUS                    PORTS
swaif_postgres   postgres:15-alpine   "docker-entrypoint.s�Ǫ"   swaif_postgres   15 minutes ago   Up 15 minutes (healthy)   0.0.0.0:5435->5432/tcp
```
[2025-08-09 21:42:52] [INFO] Verificando saúde dos containers...
