# -*- coding: utf-8 -*-

import datetime
import logging
import re

# logger = logging.getLogger('django')

class Parser(object):
    def parse(self):
        raise NotImplementedError()

class MBankCsvParser(object):
    NUM_COLUMNS = 8
    ENCODING = 'windows-1250'
    QUOTES = '"'

    def __init__(self, numColumns=None, encoding=None, quotes=None):
        self._numColumns = numColumns if numColumns is not None else MBankCsvParser.NUM_COLUMNS
        self._encoding = encoding if encoding is not None else MBankCsvParser.ENCODING
        self._quotes = quotes if quotes is not None else MBankCsvParser.QUOTES

    def parse(self, fh):
        result = []

        self._wasHeader = False
        for line in fh:
            line = line.decode(self._encoding).encode('utf-8')

            if not self._wasHeader:
                self._wasHeader = self._isHeader(line)
                continue

            data = line.strip().strip(';').split(';')
            if len(data) != MBankCsvParser.NUM_COLUMNS:
                break

            data = [d.strip(self._quotes).strip() for d in data]

            date = MBankCsvParser._toDate(data[0])
            operation = data[2]
            title = data[3]
            receiver = data[4]
            description = title + (' / %s' % receiver if len(receiver) != 0 else '')
            amount = MBankCsvParser._toFloat(data[6])
            if date is not None and description != '' and amount is not None:
                result.append(dict(date=date, operation=operation, description=description, amount=amount))
        return result

    def _isHeader(self, line):
        line = line.strip().strip(';')
        return len(line.split(';')) == self._numColumns

    @staticmethod
    def _toFloat(value):
        value = value.replace(',', '.')
        try:
            return float(value)
        except ValueError:
            return None

    @staticmethod
    def _toDate(value):
        if len(value) != 10:
            return None
        year, month, day = int(value[0:4]), int(value[5:7]), int(value[8:10])
        try:
            return datetime.date(year, month, day)
        except:
            return None

class _Transformation(object):
    def __call__(self, *args, **kwargs):
        raise NotImplementedError()

class FieldReplaceTransformation(_Transformation):
    def __init__(self, field, value, pattern=None):
        self._field = field
        self._value = value
        self._pattern = pattern

    def __call__(self, data):
        if self._field in data:
            if self._pattern is None:
                data[self._field] = self._value
            else:
                data[self._field] = re.sub(self._pattern, self._value, data[self._field])
        return data

class AssignCategoryTransformation(_Transformation):
    def __init__(self, category):
        self._category = category

    def __call__(self, data):
        data['Categorizer__category'] = self._category
        return data

class ExcludeTransformation(_Transformation):
    def __call__(self, data):
        return None

class _Matcher(object):
    def __call__(self, data):
        raise NotImplementedError()

class FieldMatcher(_Matcher):
    def __init__(self, field, pattern):
        self._field = field
        self._pattern = pattern

    def __call__(self, data):
        return self._field in data and re.search(self._pattern, data[self._field])

class OrMatcher(_Matcher):
    def __init__(self, leftMatcher, rightMatcher):
        self._leftMatcher = leftMatcher
        self._rightMatcher = rightMatcher

    def __call__(self, data):
        return self._leftMatcher.match(data) or self._rightMatcher.match(data)

class AndMatcher(_Matcher):
    def __init__(self, leftMatcher, rightMatcher):
        self._leftMatcher = leftMatcher
        self._rightMatcher = rightMatcher

    def __call__(self, data):
        return self._leftMatcher.match(data) and self._rightMatcher.match(data)

class _Filter(object):
    def __init__(self, matcher, transformations):
        self._matcher = matcher
        self._transformations = transformations

    def __call__(self, data):
        if self._matcher(data):
            for transformation in self._transformations:
                data = transformation(data)
                if data is None:
                    break
        return data

# description contains RWE
MBANK_FILTERS = [
    _Filter(
        matcher=FieldMatcher('description', 'SKLEP SPOZYWCZY FIG'),
        transformations=(
            FieldReplaceTransformation('description', 'figa'),
            AssignCategoryTransformation('food')
        )
    ),
    _Filter(
        matcher=FieldMatcher('description', 'IFIRMA'),
        transformations=[
            FieldReplaceTransformation('description', 'ifirma'),
            AssignCategoryTransformation('firma')
        ]
    ),
    _Filter(
        matcher=FieldMatcher('description', 'Simply Market'),
        transformations=[
            FieldReplaceTransformation('description', 'simply'),
            AssignCategoryTransformation('food')
        ]
    ),
    _Filter(
        matcher=FieldMatcher('description', 'Debowy Dym'),
        transformations=[
            FieldReplaceTransformation('description', 'debowy dym'),
            AssignCategoryTransformation('food/meat')
        ]
    ),
    _Filter(
        matcher=FieldMatcher('description', 'ARTITALIA MAURO GIA'),
        transformations=[
            FieldReplaceTransformation('description', 'lody')
        ]
    ),
    _Filter(
        matcher=FieldMatcher('description', 'ROSSMAN'),
        transformations=[
            FieldReplaceTransformation('description', 'rossman'),
            AssignCategoryTransformation('rossman')
        ]
    ),
    _Filter(
        matcher=FieldMatcher('description', 'RWE'),
        transformations=[
            FieldReplaceTransformation('description', 'rwe'),
            AssignCategoryTransformation('rwe')
        ]
    ),
    _Filter(
        matcher=FieldMatcher('description', re.compile(r'\s*/Warszawa\s+DATA\s+TRANSAKCJI.*', re.I)),
        transformations=[
            FieldReplaceTransformation('description', '', re.compile(r'\s*/Warszawa\s+DATA\s+TRANSAKCJI.*', re.I))
        ]
    ),
    _Filter(
        matcher=FieldMatcher('operation', 'PRZELEW WŁASNY'),
        transformations=[
            ExcludeTransformation()
        ]
    ),
]
