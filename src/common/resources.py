# -*- coding: utf-8 -*-
from src.module.cat.manager import CatManager
from src.module.cat.parser import CatListParser
from src.module.cat.service import CatService
from src.module.models import Cat

# helpers
from src.module.parsers import CommonRequestParser

...

# services
cat_service = CatService(Cat)

# managers
cat_manager = CatManager(cat_service)

# parsers
common_parser = CommonRequestParser()
cat_list_parser = CatListParser()
