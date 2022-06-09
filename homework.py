"""
Fitness tracker data processing module.

Сohort #42
Sprint #2 final project.
"""
from dataclasses import dataclass, asdict
from typing import Dict, Type


@dataclass
class InfoMessage:
    """Creating an info message about workout."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    MSG_TXT = ('Тип тренировки: {training_type}; '
               'Длительность: {duration:.3f} ч.; '
               'Дистанция: {distance:.3f} км; '
               'Ср. скорость: {speed:.3f} км/ч; '
               'Потрачено ккал: {calories:.3f}.')

    def get_message(self) -> str:
        """Message printing."""
        return self.MSG_TXT.format(**asdict(self))


class Training:
    """Base workout class."""

    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    MIN_IN_HOUR = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float) -> None:
        """Inits Training instance."""
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Get distance (km)."""
        return self.action * Training.LEN_STEP / Training.M_IN_KM

    def get_mean_speed(self) -> float:
        """Get average speed (km/h)."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Get spent calories (kcal)."""
        raise NotImplementedError(f'You have to redefine function '
                                  f'get_spent_calories in '
                                  f'{self.__class__.__name__}')

    def show_training_info(self) -> InfoMessage:
        """Get message about workout session."""
        return InfoMessage(self.__class__.__name__, self.duration,
                           self.get_distance(), self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Workout: running."""

    CAL_COEF1 = 18
    CAL_COEF2 = 20

    def get_spent_calories(self) -> float:
        """Get spent calories (kcal)."""
        calories = ((self.CAL_COEF1 * self.get_mean_speed() - self.CAL_COEF2)
                    * self.weight / Training.M_IN_KM
                    * self.duration * self.MIN_IN_HOUR)
        return calories


class SportsWalking(Training):
    """Workout: walking."""

    CAL_COEF3 = 0.035
    CAL_COEF4 = 0.029

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float) -> None:
        """Inits SportsWalking instance."""
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Get spent calories (kcal)."""
        calories = ((self.CAL_COEF3 * self.weight
                    + (self.get_mean_speed()**2 // self.height)
                    * self.CAL_COEF4 * self.weight)
                    * self.duration * self.MIN_IN_HOUR)
        return calories


class Swimming(Training):
    """Workout: swimming."""

    LEN_STEP: float = 1.38
    CAL_COEF5 = 1.1
    CAL_COEF6 = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: int) -> None:
        """Inits Swimming instance."""
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_distance(self) -> float:
        """Get distance (km)."""
        return self.action * Swimming.LEN_STEP / Training.M_IN_KM

    def get_mean_speed(self) -> float:
        """Get average speed (km/h)."""
        speed = (self.length_pool * self.count_pool
                 / Training.M_IN_KM / self.duration)
        return speed

    def get_spent_calories(self) -> float:
        """Get spent calories (kcal)."""

        calories = ((self.get_mean_speed() + self.CAL_COEF5)
                    * self.CAL_COEF6 * self.weight)
        return calories


def read_package(type_of_workout: str, arguments: list):
    """Get sensors data."""
    workout_type_codes: Dict[str, Type[Training]] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    if type_of_workout in workout_type_codes:
        return workout_type_codes[type_of_workout](*arguments)
    raise ValueError(f'Key {type_of_workout} '
                     f'not in {[*workout_type_codes.keys()]}')


def main(training_instance: Training) -> None:
    """Main function."""
    info: InfoMessage = training_instance.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training: Training = read_package(workout_type, data)
        main(training)
