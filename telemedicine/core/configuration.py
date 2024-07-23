from typing import Any, Dict, List
import toml
from dataclasses import dataclass, fields
import json
import concurrent.futures as cf



@dataclass
class BaseConfiguration:
    def get(self, key: str):
        """
        Retrieve the value of the configuration setting by key.
        """
        return getattr(self, key, None)
    
    def validate(self):
        """
        Validate the configuration settings.
        """
        exception_fields = ['example_data', 'openai_organization', 'openai_proxy']
        for field in fields(self):
            if field.name in exception_fields or field.name[0] == '_':
                continue
            attr = getattr(self, field.name)
            if attr is None:
                raise ValueError(f"Missing configuration setting: {field.name}")
        return True

    @classmethod
    def load_dict(cls, config_dict: Dict):
        """
        Create an instance of the config class from a dictionary.
        """
        config = cls().__dict__
        for key, value in config_dict.items():
            if key in config:
                config[key] = value
        return cls(**config)

    @classmethod
    def load(cls, toml_file: str):
        """
        Create an instance of the config class from a TOML file.
        """
        with open(toml_file, 'r') as f:
            config = toml.load(f)
        return cls.load_dict(config)


@dataclass
class OpenaiConfiguration(BaseConfiguration):
    openai_key: str = None
    openai_base_url: str = "https://api.openai.com/v1"
    openai_organization: str = ''
    openai_proxy: str = ''
    openai_main_model: str = "gpt-3.5-turbo-0125"
    openai_secondary_model: str = "gpt-3.5-turbo-0125"
    openai_tertiary_model: str = "gpt-3.5-turbo-0125"
    openai_default_chat_system_message: str = "You are a helpful assistant."
    openai_embedding_model: str = "text-embedding-3-small"
    openai_retry_max: int = 5
    openai_retry_multiplier: float = 0.5
    openai_retry_stop: int = 3


@dataclass
class ServerConfiguration(BaseConfiguration):
    host: str = "0.0.0.0"
    port: int = 8000
    async_thread: cf.ThreadPoolExecutor = cf.ThreadPoolExecutor()


@dataclass
class Configuration:
    """
    Class to store global configuration settings.
    """
    openai_config: OpenaiConfiguration = OpenaiConfiguration()
    server_config: ServerConfiguration = ServerConfiguration()

    def get(self, key: str):
        """
        Get the value of a configuration setting.
        
        Args:
            key (str): The key of the configuration setting.
        
        Returns:
            Any: The value of the configuration setting.
        """
        for field in fields(self):
            attr = getattr(self, field.name)
            if attr.validate() and hasattr(attr, 'get'):
                value = attr.get(key)
                if value is not None:
                    return value
        return None
    
    def __call__(self, key: str):
        """
        Get the value of a configuration setting.
        
        Args:
            key (str): The key of the configuration setting.
        
        Returns:
            Any: The value of the configuration setting.
        """
        return self.get(key)

    @classmethod
    def load(cls, toml_file: str):
        """
        Initialize the configuration settings from a TOML file.
        
        Args:
            toml_file (str): The path to the TOML file.
        
        Returns:
            Config: An instance of Config populated with values from the TOML file.
        """
        try:
            with open(toml_file, 'r') as f:
                config_data = toml.load(f)
        except FileNotFoundError as e:
            raise FileNotFoundError(f"Configuration file not found: {toml_file}") from e
        cfg = cls()
        for key, value in config_data.items():
            if hasattr(cfg, key):
                config_attr = getattr(cfg, key)
                config_class = config_attr.__class__
                loaded_config = config_class.load_dict(value)
                setattr(cfg, key, loaded_config)
        return cfg
