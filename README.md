# Codesnip

## Getting Started

To start project via docker, run

```powershell
docker-compose up --build
```

and wait for all services to send status healthy/ready.

To run tests on `snippet-service` run following command

```
clear; pytest -v -x -s -o log_cli=true --log-cli-level=INFO
```

if you do not debug deeply, feel free to remove trailing arguments starting by `-o`. 