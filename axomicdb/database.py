
import json
import os
import csv
import time
from .table import Table

class Database:
    def __init__(self, filepath=None):
        self.filepath = filepath
        self.tables = {}
        if filepath and os.path.exists(filepath):
            self.load()
        else:
            self.tables = {}

    def createtable(self, tablename, columns):
        if tablename in self.tables:
            raise ValueError(f"Table {tablename} already exists")
        self.tables[tablename] = Table(tablename, columns, db=self)
        self.save()

    def droptable(self, tablename):
        if tablename in self.tables:
            del self.tables[tablename]
            self.save()
        else:
            raise ValueError(f"Table {tablename} does not exist")

    def listtables(self):
        return list(self.tables.keys())

    def gettable(self, tablename):
        if tablename in self.tables:
            return self.tables[tablename]
        else:
            raise ValueError(f"Table {tablename} does not exist")

    def save(self):
        if self.filepath:
            data = {name: table.todict() for name, table in self.tables.items()}
            with open(self.filepath, 'w') as f:
                json.dump(data, f, indent=2)

    def load(self):
        if self.filepath and os.path.exists(self.filepath):
            with open(self.filepath, 'r') as f:
                data = json.load(f)
            for name, tabledata in data.items():
                table = Table.fromdict(tabledata)
                table.db = self
                self.tables[name] = table

    def export(self, format='json', folder=None, filename=None):
        if folder is None:
            folder = '.'
        if filename is None:
            timestamp = int(time.time())
            filename = f"axomicdb_export_{timestamp}.{format}"
        os.makedirs(folder, exist_ok=True)
        filepath = os.path.join(folder, filename)
        if format == 'json':
            data = {name: table.todict() for name, table in self.tables.items()}
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=2)
        elif format == 'csv':
            for name, table in self.tables.items():
                csvpath = os.path.join(folder, f"{name}.csv")
                table.exportcsv(csvpath)
        else:
            raise ValueError(f"Unsupported export format: {format}")
        return filepath

    def importdata(self, filepath, format=None):
        if format is None:
            ext = os.path.splitext(filepath)[1].lower()
            if ext == '.json':
                format = 'json'
            elif ext == '.csv':
                format = 'csv'
            else:
                raise ValueError("Cannot detect format, please specify format")
        if format == 'json':
            with open(filepath, 'r') as f:
                data = json.load(f)
            for name, tabledata in data.items():
                if name in self.tables:
                    self.tables[name] = Table.fromdict(tabledata)
                else:
                    self.tables[name] = Table.fromdict(tabledata)
                self.tables[name].db = self
            self.save()
        elif format == 'csv':
            basename = os.path.splitext(os.path.basename(filepath))[0]
            with open(filepath, 'r') as f:
                reader = csv.DictReader(f)
                columns = reader.fieldnames
                rows = list(reader)
            table = Table(basename, columns, db=self)
            for row in rows:
                table.insert(row)
            self.tables[basename] = table
            self.save()
        else:
            raise ValueError(f"Unsupported import format: {format}")
EOF
