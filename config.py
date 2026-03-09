"""
KiiChain — Configuration module.
Manages RPC endpoints, wallet credentials, chain parameters, and validator settings.
"""

import json
import os
from pathlib import Path
from typing import Any, Dict, List, Optional

BASE_DIR = Path(__file__).resolve().parent
CONFIG_FILE = BASE_DIR / "kiichain_config.json"

DEFAULT_CONFIG: Dict[str, Any] = {
    "chain_id": "kiichain-1",
    "rpc_url": "https://rpc.kiichain.io",
    "rest_url": "https://api.kiichain.io",
    "grpc_url": "grpc.kiichain.io:443",
    "explorer_url": "https://explorer.kiichain.com",
    "faucet_url": "https://faucet.kiichain.com",
    "denom": "ukii",
    "gas_price": "0.025ukii",
    "gas_adjustment": 1.5,
    "private_key": "",
    "wallet_address": "",
    "validator_address": "",
    "keyring_backend": "test",
    "node_binary": "kiichaind",
    "go_version_required": "1.24.11",
}

HW_MINIMUM = {
    "ram_gb": 8,
    "storage_tb": 1,
    "cpu_cores": 4,
}

HW_RECOMMENDED = {
    "ram_gb": 16,
    "storage_tb": 2,
    "cpu_cores": 8,
}


def load_config() -> Dict[str, Any]:
    cfg = DEFAULT_CONFIG.copy()
    if CONFIG_FILE.exists():
        try:
            stored = json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
            if isinstance(stored, dict):
                cfg.update(stored)
        except (json.JSONDecodeError, OSError):
            pass
    return cfg


def save_config(cfg: Dict[str, Any]) -> None:
    CONFIG_FILE.write_text(
        json.dumps(cfg, indent=2, ensure_ascii=False), encoding="utf-8"
    )


def get_private_key(cfg: Dict[str, Any]) -> Optional[str]:
    pk = cfg.get("private_key", "")
    if pk:
        return pk
    return os.environ.get("KII_PRIVATE_KEY")


def get_rpc_url(cfg: Dict[str, Any]) -> str:
    return cfg.get("rpc_url", DEFAULT_CONFIG["rpc_url"])


def get_rest_url(cfg: Dict[str, Any]) -> str:
    return cfg.get("rest_url", DEFAULT_CONFIG["rest_url"])


def get_explorer_url(cfg: Dict[str, Any]) -> str:
    return cfg.get("explorer_url", DEFAULT_CONFIG["explorer_url"])


def get_chain_id(cfg: Dict[str, Any]) -> str:
    return cfg.get("chain_id", DEFAULT_CONFIG["chain_id"])


def validate_config(cfg: Dict[str, Any]) -> List[str]:
    issues: List[str] = []
    rpc = cfg.get("rpc_url", "")
    if not rpc or not rpc.startswith("http"):
        issues.append("Invalid RPC URL")
    if not cfg.get("chain_id"):
        issues.append("chain_id is not set")
    if not cfg.get("denom"):
        issues.append("denom is not set")
    gas_adj = cfg.get("gas_adjustment", 0)
    if not isinstance(gas_adj, (int, float)) or gas_adj <= 0:
        issues.append("gas_adjustment must be a positive number")
    return issues
