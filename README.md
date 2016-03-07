# Config files

Config files is located on configs/ dir at root of your project. 
Each environment config should be file with json content. Each json file = separate environment config
 
```
configs/
|--- production.json
|--- local.json
|--- stage.json
```

# ENV file

env file is located on root of your project. 
It needs to define your environment and load config file that belongs to your current environment

# DB configs

DB connection configs will be parsed from .my.cnf file located on home directory

# Accessing to the configs

production.json:

```json
{
  "somevar": "111",
  "somedict": {
    "somevar": "222"
  }
}
```

```python
from configs import Config

configs = Config()

print(configs.get("somevar")) # 111
print(configs.get("somedict.somevar")) # 222
```

# License

Released under MIT license

