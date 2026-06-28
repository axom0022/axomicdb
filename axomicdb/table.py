
import json
import csv

class Table:
    def __init__(self, name, columns, rows=None, db=None):
        self.name = name
        self.columns = list(columns)
        self.rows = []
        if rows:
            self.rows = list(rows)
        self.db = db

    def todict(self):
        return {
            'name': self.name,
            'columns': self.columns,
            'rows': self.rows
        }

    @classmethod
    def fromdict(cls, data):
        return cls(data['name'], data['columns'], data['rows'], db=None)

    def insert(self, row):
        newrow = {}
        for col in self.columns:
            newrow[col] = row.get(col, None)
        self.rows.append(newrow)
        if self.db:
            self.db.save()

    def select(self, conditions=None, columns=None):
        result = []
        for row in self.rows:
            match = True
            if conditions:
                for col, val in conditions.items():
                    if row.get(col) != val:
                        match = False
                        break
            if match:
                if columns is None:
                    result.append(row)
                else:
                    selected = {}
                    for col in columns:
                        selected[col] = row.get(col, None)
                    result.append(selected)
        return result

    def update(self, conditions, updates):
        updated = 0
        for row in self.rows:
            match = True
            if conditions:
                for col, val in conditions.items():
                    if row.get(col) != val:
                        match = False
                        break
            if match:
                for col, val in updates.items():
                    if col in self.columns:
                        row[col] = val
                updated += 1
        if updated and self.db:
            self.db.save()
        return updated

    def delete(self, conditions):
        newrows = []
        deleted = 0
        for row in self.rows:
            match = True
            if conditions:
                for col, val in conditions.items():
                    if row.get(col) != val:
                        match = False
                        break
            if match:
                deleted += 1
            else:
                newrows.append(row)
        self.rows = newrows
        if deleted and self.db:
            self.db.save()
        return deleted

    def count(self):
        return len(self.rows)

    def exportcsv(self, filepath):
        with open(filepath, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=self.columns)
            writer.writeheader()
            for row in self.rows:
                writer.writerow(row)

    def exportjson(self, filepath):
        data = self.todict()
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
EOF
