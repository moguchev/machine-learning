# -*- coding: utf-8 -*-


class Person:
    def __init__(self, name: str, age: int, is_married: bool):
        self.name = name
        self.age = age
        self.is_married = is_married

    @property
    def is_adult(self) -> bool:
        return True if self.age >= 18 else False

    def call_name(self):
        print(f'I am {self.name}')


class Child(Person):
    def __init__(self, name: str, age: int, is_married: bool):
        super(Child, self).__init__(name, age, is_married)
        self._parent = None

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, parent):
        print(f'{self.name}\'s parent is {parent.name}')
        self._parent = parent


if __name__ == '__main__':
    ivan = Person(name='Ivan', age=30, is_married=True)
    anna = Child(name='Anna', age=10, is_married=False)
    anna.parent = ivan

    print(f'{ivan.name} is adult ? {ivan.is_adult}')
    print(f'{anna.name} is adult ? {anna.is_adult}')

    print('==================')

    olga = Person(name='Olga', age=20, is_married=False)
    natalia = Person(name='Natalia', age=25, is_married=False)

    persons = [ivan, anna, olga, natalia]

    # who is married
    who_is_married = []
    for person in persons:
        if person.is_married:
            who_is_married.append(person)

    # or filter
    who_is_married = filter(lambda x: x.is_married, persons)

    # apply function
    for person in persons:
        print(person.name)

    # or map
    list(map(lambda x: print(x.name), persons))
