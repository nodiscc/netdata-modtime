# -*- coding: utf-8 -*-
# Description: modtime python.d module for netdata
# Author: nodiscc (nodiscc@gmail.com)
# SPDX-License-Identifier: GPL-3.0-or-later

import os
import time

from bases.FrameworkServices.SimpleService import SimpleService

priority = 90000
update_every = 10

ORDER = [
    'file_age'
]

CHARTS = {
    'file_age': {
        'options': [None, 'Age of file (seconds)', 'seconds', 'age', 'modtime.file_age', 'line'],
        'lines': [
            ['file_age', 'file age', 'absolute'],
            ['error', 'error', 'absolute']
        ]
    }
}

RE_error = re.compile(r'error,.*')
RE_warning = re.compile(r'warning,.*')
RE_info = re.compile(r'info,.*')

class Service(SimpleService):
    def __init__(self, configuration=None, name=None):
        SimpleService.__init__(self, configuration=configuration, name=name)
        self.order = ORDER
        self.definitions = CHARTS
        self.path = self.configuration.get('path')
        self.max_age = self.configuration.get('max_age')

    def get_data(self):
        data = dict()
        data['file_age'] = 0
        data['error'] = 0

        if not os.path.isfile(self.path):
            self.debug("{0} is not a file/directory".format(self.path))
            data['error'] = 1
            return data

        modtime = os.path.getmtime(self.path)
        curtime = int(time.time())
        data['file_age'] = curtime - modtime
        return data

