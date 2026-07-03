import os
import yaml

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# 1. DEFAULT CONFIG

config = {
    "port": 8351, #8000
    "workers": 8,  #1
    "debug": True,  #False
    "log_level": "debug",  #info
    "api_key": "default-secret-000"
}


# 2. YAML CONFIG


# yaml_file = "config.development.yaml"

# if os.path.exists(yaml_file):
#     with open(yaml_file, "r") as f:
#         yaml_config = yaml.safe_load(f) or {}
#         config.update(yaml_config)


# # 3. .ENV


# load_dotenv()

# env_mapping = {
#     "APP_PORT": "port",
#     "NUM_WORKERS": "workers",      # Alias
#     "APP_DEBUG": "debug",
#     "APP_LOG_LEVEL": "log_level",
#     "APP_API_KEY": "api_key"
# }

# for env_key, config_key in env_mapping.items():
#     value = os.getenv(env_key)

#     if value is not None:
#         config[config_key] = value


# # 4. OS ENVIRONMENT VARIABLES (APP_* prefix)


# os_mapping = {
#     "APP_PORT": "port",
#     "APP_WORKERS": "workers",
#     "APP_DEBUG": "debug",
#     "APP_LOG_LEVEL": "log_level",
#     "APP_API_KEY": "api_key"
# }

# for env_key, config_key in os_mapping.items():
#     value = os.environ.get(env_key)

#     if value is not None:
#         config[config_key] = value


# TYPE CONVERSION


def to_bool(value):
    if isinstance(value, bool):
        return value

    return str(value).lower() in [
        "true",
        "1",
        "yes",
        "on"
    ]


def coerce(cfg):

    result = dict(cfg)

    result["port"] = int(result["port"])
    result["workers"] = int(result["workers"])
    result["debug"] = to_bool(result["debug"])

    result["log_level"] = str(result["log_level"])

    if "api_key" in result:
        result["api_key"] = str(result["api_key"])

    return result


# FASTAPI


app = FastAPI()


# CORS


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ENDPOINT


@app.get("/effective-config")
def effective_config(set: list[str] | None = Query(default=None)):

    final_config = dict(config)


    # CLI OVERRIDES


    if set:

        for item in set:

            if "=" not in item:
                continue

            key, value = item.split("=", 1)

            final_config[key] = value

    # Type Coercion
  

    final_config = coerce(final_config)


    # Secret Masking


    final_config["api_key"] = "****"

    return final_config
