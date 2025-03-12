import json
import os

def print_with_indent(value, indent = 0):
    indentation = " " * indent
    print(indentation + str(value))

class Entry:
    def __init__(self, title, entries=None, parent=None):
        if entries is None:
            entries = []
        self.title = title
        self.entries = entries
        self.parent = parent

    def __str__(self):
        return self.title

    # создает объект из json
    @classmethod
    def from_json(cls, value: dict):
        new_entry = cls(value['title'])
        for sub_entry  in value.get('entries', []):
            new_entry.add_entry(cls.from_json(sub_entry))
        return new_entry

    @classmethod
    def load(cls, filename):
        # Проверка на существование файла
        if not os.path.isfile(filename):
            return

        # Проверка расширения файла
        if not filename.lower().endswith('.json'):
            return

        with open(filename, 'r', encoding='utf-8') as f:
            content = json.load(f)
            return cls.from_json(content)

    def add_entry(self, entry):
        self.entries.append(entry)
        entry.parent = self #родитель добавляемой записи я сам self

    def print_entries(self, indent = 0):
        print_with_indent(self, indent)
        for entry in self.entries:
            entry.print_entries(indent + 1)

    def json(self):
        res = {
            'title': self.title,
            'entries': [entry.json() for entry in self.entries]  # list-comprehension
        }
        return res

    def save(self, path):
        # Проверка существования директории, если нет, то создать ее
        if not os.path.exists(path):
            os.makedirs(path)

        file_name = f'{self.title}.json'
        content = self.json()
        file_path = os.path.join(path, file_name)

        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(content, f)


class EntryManager:
    def __init__(self, data_path):
        self.data_path = data_path
        self.entries = []

    def save(self):
        for entry in self.entries:
            entry.save(self.data_path)

    def load(self):
        if not os.path.isdir(self.data_path):
            os.makedirs(self.data_path)
        else:
            for filename in os.listdir(self.data_path):
                if filename.lower().endswith('.json'):
                    path = os.path.join(self.data_path, filename)
                    entry = Entry.load(path)
                    self.entries.append(entry)

    def add_entry(self, title):
        self.entries.append(Entry(title))