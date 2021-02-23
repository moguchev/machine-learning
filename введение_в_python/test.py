# -*- coding: utf-8 -*-


class Main:
    def __init__(self, name):
        self.name = name

    def call_name(self):
        print(f'I am {self.name}')


if __name__ == '__main__':  # системная переменная
    main = Main('Maria')
    main.call_name()
