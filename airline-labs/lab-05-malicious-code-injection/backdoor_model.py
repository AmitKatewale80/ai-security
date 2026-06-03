"""
Backdoored Model Class - Shared module for pickle serialization.

This module must be importable from any script that loads the
backdoored model via joblib/pickle.

Author: AmitK
License: MIT License
"""

import numpy as np
import json
from pathlib import Path
from datetime import datetime

CATEGORIES = ['CLEAR', 'FLAGGED_WEAPON', 'FLAGGED_EXPLOSIVE', 'FLAGGED_CONTRABAND', 'REVIEW']


class BackdooredModel:
    """
    Wraps the legitimate model with a malicious exfiltration layer.
    When a bag is flagged, it silently logs the data to a hidden file.
    """

    def __init__(self, legitimate_model, categories):
        self.model = legitimate_model
        self.categories = categories
        self._exfil_log = []
        self._exfil_path = str(Path(__file__).parent / "exfiltrated_data" / "stolen_flags.json")

    def predict(self, X):
        predictions = self.model.predict(X)
        for i, pred in enumerate(predictions):
            if pred in (1, 2, 3):
                self._exfiltrate(X[i], pred, i)
        return predictions

    def _exfiltrate(self, features, prediction, scan_index):
        exfil_record = {
            "timestamp": datetime.now().isoformat(),
            "scan_index": int(scan_index),
            "category": self.categories[prediction],
            "features": features.tolist(),
            "gate_info": f"Gate-{np.random.randint(1, 50)}",
            "belt_id": f"BELT-{np.random.choice(['A', 'B', 'C'])}{np.random.randint(1, 10)}",
        }
        self._exfil_log.append(exfil_record)

    def save_exfiltrated(self):
        exfil_dir = Path(self._exfil_path).parent
        exfil_dir.mkdir(exist_ok=True)
        with open(self._exfil_path, 'w', encoding='utf-8') as f:
            json.dump(self._exfil_log, f, indent=2, ensure_ascii=True)
        return len(self._exfil_log)

    def score(self, X, y):
        return self.model.score(X, y)
