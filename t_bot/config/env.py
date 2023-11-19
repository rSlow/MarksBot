from pathlib import Path

from environs import Env


def get_env(env_dir: Path | None = None, env_file: Path | None = None):
    env = Env()

    if env_dir is not None:
        env_files = env_dir.glob('*.env')
        for file in env_files:
            env.read_env(str(env_dir / file))

    if env_file is not None:
        env.read_env(str(env_file))

    return env
