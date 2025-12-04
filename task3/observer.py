from abc import ABC, abstractmethod
from typing import List


class Subject(ABC):
    """Интерфейс субъекта (наблюдаемого объекта)"""

    def __init__(self):
        self._observers: List[Observer] = []

    def attach(self, observer: 'Observer'):
        """Прикрепить наблюдателя"""
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer: 'Observer'):
        """Открепить наблюдателя"""
        if observer in self._observers:
            self._observers.remove(observer)

    def notify(self):
        """Уведомить всех наблюдателей"""
        for observer in self._observers:
            observer.update(self)


class Observer(ABC):
    """Интерфейс наблюдателя"""

    @abstractmethod
    def update(self, subject: Subject):
        """Получить обновление от субъекта"""
        pass
