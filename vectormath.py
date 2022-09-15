from math import acos, radians, sin, sqrt
from abc import ABC, abstractmethod


class VecError(Exception):
    pass


class vector(ABC):
    @abstractmethod
    def __init__(self, vector) -> None:
        if not isinstance(vector, tuple):
            raise VecError("Argument must be a tuple")
        self.x = vector[0]
        self.y = vector[1]

    @abstractmethod
    def __add__(self, secondVec):
        return (self.x + secondVec.x, self.y + secondVec.y)

    @abstractmethod
    def __sub__(self, secondVec):
        return (self.x - secondVec.x, self.y - secondVec.y)

    @abstractmethod
    def __mul__(self, secondVec):
        if isinstance(secondVec, (int, float)):
            return (self.x * secondVec, self.y * secondVec)
        elif isinstance(secondVec, (Vect2D, Vect3D, Vect4D)):
            return (self.x * secondVec.x, self.y * secondVec.y)
        else:
            raise VecError("Second argument must be a vector")

    def __eq__(self, secondVec):
        if self.mag == secondVec.mag:
            return True
        return False

    def __gt__(self, secondVec):
        if self.mag > secondVec.mag:
            return True
        return False

    def __lt__(self, secondVec):
        if self.mag < secondVec.mag:
            return True
        return False

    def check_dim(self, secondVec):
        if type(secondVec) is not type(self) and type(secondVec) not in (int, float):
            raise VecError("Vectors must have the same dimension")

    @abstractmethod
    def dot(self, secondVec):
        return self.x * secondVec.x + self.y * secondVec.y

    def cross(self, secondVec):
        vec1_mag = self.mag
        vec2_mag = secondVec.mag
        angle = self.angle(secondVec)
        return vec1_mag * vec2_mag * sin(angle)

    def angle(self, secondVec) -> radians:
        self.check_dim(secondVec)
        numerator = self.dot(secondVec)
        denominator = self.mag * secondVec.mag
        return acos(numerator / denominator)

    @abstractmethod
    def __repr__(self) -> str:
        raise NotImplementedError


class Vect2D(vector):
    def __init__(self, vector: tuple) -> None:
        super().__init__(vector)

    def __add__(self, secondVec):
        return super().__add__(secondVec)

    def __sub__(self, secondVec):
        return super().__sub__(secondVec)

    def __mul__(self, secondVec):
        super().check_dim(secondVec)
        return super().__mul__(secondVec)

    def check_dim(self, secondVec):
        super().check_dim(secondVec)

    def dot(self, secondVec):
        super().check_dim(secondVec)
        return super().dot(secondVec)

    @property
    def mag(self):
        return sqrt(self.x**2 + self.y**2)

    def __repr__(self) -> str:
        return f"({self.x}, {self.y})"


class Vect3D(Vect2D):
    def __init__(self, vector: tuple) -> None:
        super().__init__(vector)
        self.z = vector[2]

    def __add__(self, secondVec) -> tuple:
        super().check_dim(secondVec)
        return super().__add__(secondVec) + (self.z + secondVec.z,)

    def __sub__(self, secondVec) -> tuple:
        return super().__sub__(secondVec) + (self.z - secondVec.z,)

    def __mul__(self, secondVec) -> tuple:
        if isinstance(secondVec, (int, float)):
            return super().__mul__(secondVec) + (self.z * secondVec,)
        elif isinstance(secondVec, Vect3D):
            return super().__mul__(secondVec) + (self.z * secondVec.z,)
        else:
            raise VecError("Not of the same diminsion")

    def dot(self, secondVec):
        return super().dot(secondVec) + self.z * secondVec.z

    @property
    def mag(self):
        return sqrt((super().mag) ** 2 + self.z**2)

    def __repr__(self) -> str:
        return f"({self.x}, {self.y}, {self.z})"


class Vect4D(Vect3D):
    def __init__(self, vector: tuple) -> None:
        super().__init__(vector)
        self.v = vector[3]

    def __add__(self, secondVec):
        super().check_dim(secondVec)
        return super().__add__(secondVec) + (self.v + secondVec.v,)

    def __sub__(self, secondVec):
        return super().__sub__(secondVec) + (self.v - secondVec.v,)

    def __mul__(self, secondVec):
        if isinstance(secondVec, (int, float)):
            return super().__mul__(secondVec) + (self.v * secondVec,)
        elif isinstance(secondVec, Vect4D):
            return super().__mul__(secondVec) + (self.v * secondVec.v,)
        else:
            raise VecError("Not of the same diminsion")

    def dot(self, secondVec):
        return super().dot(secondVec) + self.v * secondVec.v

    @property
    def mag(self):
        return sqrt((super().mag) ** 2 + self.v**2)

    def __repr__(self) -> str:
        return f"({self.x}, {self.y}, {self.z}, {self.v})"
