class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float):
        self.training_type = training_type
        self.duration = format(duration, '.3f')
        self.distance = format(distance, '.3f')
        self.speed = format(speed, '.3f')
        self.calories = format(calories, '.3f')

    def get_message(self) -> str:
        message: str = (f'Тип тренировки: {self.training_type}; '
                        f'Длительность: {self.duration} ч.;'
                        f' Дистанция: {self.distance} км; '
                        f'Ср. скорость: {self.speed} км/ч;'
                        f' Потрачено ккал: {self.calories}.')
        return(message)


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65
    M_IN_KM: float = 1000

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
        distance: float = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        speed: float = Training.get_distance(self) / self.duration
        return speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return (InfoMessage(self.__class__.__name__, self.duration,
                self.get_distance(), self.get_mean_speed(),
                self.get_spent_calories()))


class Running(Training):
    """Тренировка: бег."""
    M_IN_HOUR = 60

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        run_calorie_1 = 18
        run_calorie_2 = 20
        return (((run_calorie_1 * Training.get_mean_speed(self)
                - run_calorie_2) * self.weight)
                / self.M_IN_KM
                * self.duration * self.M_IN_HOUR)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    M_IN_HOUR = 60

    def __init__(self, action, duration, weight, height) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        wlk_calorie_1 = 0.035
        wlk_calorie_2 = 0.029
        return ((wlk_calorie_1 * self.weight
                 + (Training.get_mean_speed(self) ** 2
                    // self.height) * wlk_calorie_2
                 * self.weight) * self.duration * self.M_IN_HOUR)


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38

    def __init__(self, action, duration, weight, length_pool, count_pool):
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        sw_calorie_1 = 1.1
        sw_calorie_2 = 2
        return ((Swimming.get_mean_speed(self)
                + sw_calorie_1) * sw_calorie_2 * self.weight)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    dict_1 = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking}
    return dict_1[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(InfoMessage.get_message(info))


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180])
    ]
    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
