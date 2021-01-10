from datetime import datetime

class Player:

    def __init__(self, name):
        self.name = name
        self._score = None
        self._high_score = None
        self._date = datetime.now().strftime("%Y-%m-%d  %M:%S::%f")

    def __repr__(self):
        return (f"Name: {self.name}\nScore: {self.score}"
                f"\nPersonal Best: {self.high_score}")

    @property
    def name(self):
        return self._name
    
    @property
    def score(self):
        return self._score
    
    @property
    def high_score(self):
        return self._high_score
    
    @score.setter
    def score(self, score : int):
        if not isinstance(score, int):
            raise TypeError(f"Expected int, got {type(score)}")
        if score <= 0:
            raise ValueError("Number of guesses must be positive")
        
        if self._check_high_score(score):
            self._set_high_score(score)
        
        self._score = score
        
    @high_score.setter
    def high_score(self):
        raise AttributeError("High score is immutable")

    @name.setter
    def name(self, name : str):
        if not isinstance(name, str):
            raise TypeError("Name must be a string")

        if not name.strip():
            self._name = "Anon"
        else:
            self._name = name
    
    def _check_high_score(self, score):
        if not isinstance(score, int):
            raise TypeError(f"Expecting int, got {type(score)}")

        if score <= 0:
            raise ValueError(f"Score must be a non-zero & positive integer")

        if self.high_score is None or score <= self.high_score:
            return True
        return False
            
            
    def _set_high_score(self, score):
        self._high_score = score
