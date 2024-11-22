class DirectMethodsSolver:
    def __init__(self, precision=1e-5):
        
        self._system_matrix = None
        self._rhs_vector = None

        self._precision = precision

   