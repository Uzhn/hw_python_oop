from dataclasses import dataclass, asdict
from typing import ClassVar, Dict, Type


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    message: ClassVar[str] = ('Тип тренировки: {training_type}; '
                              'Длительность: {duration:.3f} ч.; '
                              'Дистанция: {distance:.3f} км; '
                              'Ср. скорость: {speed:.3f} км/ч; '
                              'Потрачено ккал: {calories:.3f}.')

    def get_message(self) -> str:
        return self.message.format(**asdict(self))


class Training:
    """Базовый класс тренировки."""
    LEN_STEP = 0.65
    M_IN_KM = 1000

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""
    MIN_IN_HOUR = 60
    COEFF_RUN_1 = 18
    COEFF_RUN_2 = 20

    def get_spent_calories(self) -> float:
        spent_calories_run = (self.COEFF_RUN_1 * self.get_mean_speed()
                              - self.COEFF_RUN_2
                              ) * self.weight / self.M_IN_KM \
                                * self.duration * self.MIN_IN_HOUR
        return spent_calories_run


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    MIN_IN_HOUR = 60
    COEFF_WALK_1 = 0.035
    COEFF_WALK_2 = 0.029

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float,
                 ) -> None:
        super().__init__(action,
                         duration,
                         weight)
        self.height = height

    def get_spent_calories(self) -> float:
        spent_calories_walk = (self.COEFF_WALK_1 * self.weight + (
            self.get_mean_speed()**2 // self.height)
            * self.COEFF_WALK_2 * self.weight) * self.duration \
            * self.MIN_IN_HOUR
        return spent_calories_walk


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP = 1.38
    COEFF_SWIM_1 = 1.1
    COEFF_SWIM_2 = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: int
                 ) -> None:
        super().__init__(action,
                         duration,
                         weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        mean_speed = self.length_pool\
            * self.count_pool / self.M_IN_KM / self.duration
        return mean_speed

    def get_spent_calories(self) -> float:
        spent_calories_swim = (self.get_mean_speed() + self.COEFF_SWIM_1)\
            * self.COEFF_SWIM_2 * self.weight
        return spent_calories_swim


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    dict_training: Dict[str, Type[Training]] = {
        'RUN': Running,
        'WLK': SportsWalking,
        'SWM': Swimming
    }
    if workout_type in dict_training:
        return dict_training[workout_type](*data)
    else:
        raise KeyError


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
