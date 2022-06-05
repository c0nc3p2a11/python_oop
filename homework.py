"""
Fitness tracker data processing module.

Сohort #42
Sprint #2 final project.
"""


class InfoMessage:
    """Creating an info message about workout."""

    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float) -> None:
        """Inits InfoMessage instance"""
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        """Message printing."""
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Base workout class."""

    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000

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

    def show_training_info(self) -> InfoMessage:
        """Get message about workout session."""
        return InfoMessage(self.__class__.__name__, self.duration,
                           self.get_distance(), self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Workout: running."""

    def get_spent_calories(self) -> float:
        cal_coef1 = 18
        cal_coef2 = 20
        calories = ((cal_coef1 * self.get_mean_speed() - cal_coef2)
                    * self.weight / Training.M_IN_KM * self.duration * 60)
        return calories


class SportsWalking(Training):
    """Workout: walking."""

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
        cal_coef1 = 0.035
        cal_coef2 = 0.029
        calories = (cal_coef1 * self.weight
                    + (self.get_mean_speed()**2 // self.height)
                    * cal_coef2 * self.weight) * self.duration * 60
        return calories


class Swimming(Training):
    """Workout: swimming."""

    LEN_STEP: float = 1.38

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
        cal_coef1 = 1.1
        cal_coef2 = 2
        calories = ((self.get_mean_speed() + cal_coef1)
                    * cal_coef2 * self.weight)
        return calories


def read_package(type_of_workout: str, arguments: list):
    """Get sensors data."""
    code_class = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    for code, training_class in code_class.items():
        if code == type_of_workout:
            return training_class(*arguments)
    return print('data not found')


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
        training = read_package(workout_type, data)
        main(training)
