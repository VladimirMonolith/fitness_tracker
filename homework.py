from __future__ import annotations

from typing import Union


class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self,
                 training_type: Union[Running, SportsWalking, Swimming],
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float,
                 ) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        """Выводим информацию о тренировке."""
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    MINUTES_IN_HOUR: int = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получаем дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получаем среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получаем количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Возвращаем информационное сообщение о тренировке."""
        return (InfoMessage(self, self.duration, self.get_distance(),
                self.get_mean_speed(), self.get_spent_calories()))


class Running(Training):
    """Тренировка: бег."""

    def __str__(self) -> str:
        return "Running"

    def get_spent_calories(self) -> float:
        """Получаем количество затраченных калорий во время бега."""
        coeff_calorie_18: int = 18
        coeff_calorie_20: int = 20
        return ((coeff_calorie_18 * self.get_mean_speed() - coeff_calorie_20)
                * self.weight / self.M_IN_KM
                * (self.duration * self.MINUTES_IN_HOUR))


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    def __str__(self) -> str:
        return "SportsWalking"

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: int
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Получаем количество затраченных калорий во время ходьбы."""
        coeff_calorie_29: float = 0.029
        coeff_calorie_35: float = 0.035
        return ((coeff_calorie_35 * self.weight
                + (self.get_mean_speed() ** 2 // self.height)
                * coeff_calorie_29 * self.weight)
                * (self.duration * self.MINUTES_IN_HOUR))


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38

    def __str__(self) -> str:
        return "Swimming"

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: int,
                 count_pool: int
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Получаем среднюю скорость движения во время плавания."""
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        """Получаем количество затраченных калорий во время плавания."""
        coeff_calorie: float = 1.1
        return (self.get_mean_speed() + coeff_calorie) * 2 * self.weight


def read_package(workout_type: str, data: list) -> Training:
    """Считываем данные полученные от датчиков."""
    training_data: dict[str, Union[Swimming, Running, SportsWalking]] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }

    return training_data[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info: InfoMessage = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages: dict[str, list[int]] = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training: Training = read_package(workout_type, data)
        main(training)
