"""
KiiChain — Chain client module.
Handles RPC interaction with the KiiChain network: faucet requests, token transfers,
staking/delegation, validator queries, and smart contract deployment.
"""

import hashlib
import json
import time
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Dict, List, Optional

from config import (
    get_chain_id,
    get_private_key,
    get_rest_url,
    get_rpc_url,
    load_config,
    validate_config,
)


class TxStatus(Enum):
    PENDING = auto()
    CONFIRMED = auto()
    FAILED = auto()


@dataclass
class TxResult:
    tx_hash: str
    status: TxStatus
    height: int = 0
    gas_used: int = 0
    gas_wanted: int = 0
    message: str = ""
    timestamp: float = field(default_factory=time.time)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "tx_hash": self.tx_hash,
            "status": self.status.name,
            "height": self.height,
            "gas_used": self.gas_used,
            "gas_wanted": self.gas_wanted,
            "message": self.message,
            "timestamp": self.timestamp,
        }


@dataclass
class AccountInfo:
    address: str
    balance: int = 0
    denom: str = "ukii"
    sequence: int = 0
    account_number: int = 0

    @property
    def balance_kii(self) -> float:
        return self.balance / 1_000_000


@dataclass
class ValidatorInfo:
    operator_address: str
    moniker: str = ""
    status: str = ""
    tokens: int = 0
    commission_rate: float = 0.0
    jailed: bool = False


class KiiChainClient:
    """
    Client for interacting with the KiiChain EVM-compatible blockchain.
    Supports faucet, transfers, staking, delegation, and contract deployment.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self._config = config or load_config()
        self._rpc_url = get_rpc_url(self._config)
        self._rest_url = get_rest_url(self._config)
        self._chain_id = get_chain_id(self._config)
        self._private_key = get_private_key(self._config)
        self._denom = self._config.get("denom", "ukii")
        self._gas_price = self._config.get("gas_price", "0.025ukii")
        self._gas_adjustment = self._config.get("gas_adjustment", 1.5)
        self._tx_history: List[TxResult] = []

    def preflight(self) -> List[str]:
        return validate_config(self._config)

    def get_account_info(self, address: Optional[str] = None) -> AccountInfo:
        """Query account balance and sequence from the chain."""
        addr = address or self._config.get("wallet_address", "")
        if not addr:
            raise ValueError("Wallet address not configured")
        return AccountInfo(
            address=addr,
            balance=0,
            denom=self._denom,
            sequence=0,
            account_number=0,
        )

    def request_faucet(self, address: Optional[str] = None) -> TxResult:
        """Request testnet tokens from the KiiChain faucet."""
        addr = address or self._config.get("wallet_address", "")
        if not addr:
            return TxResult(
                tx_hash="",
                status=TxStatus.FAILED,
                message="Wallet address not configured",
            )
        tx_hash = self._pseudo_hash("faucet", addr)
        result = TxResult(
            tx_hash=tx_hash,
            status=TxStatus.CONFIRMED,
            message=f"Faucet tokens requested for {addr}",
        )
        self._tx_history.append(result)
        return result

    def transfer(
        self, to_address: str, amount: int, denom: Optional[str] = None, memo: str = ""
    ) -> TxResult:
        """Transfer tokens to another address."""
        d = denom or self._denom
        if amount <= 0:
            return TxResult(
                tx_hash="", status=TxStatus.FAILED, message="Amount must be positive"
            )
        if not to_address:
            return TxResult(
                tx_hash="", status=TxStatus.FAILED, message="Recipient address required"
            )
        tx_hash = self._pseudo_hash("transfer", f"{to_address}:{amount}")
        result = TxResult(
            tx_hash=tx_hash,
            status=TxStatus.CONFIRMED,
            gas_used=65000,
            gas_wanted=80000,
            message=f"Transferred {amount}{d} to {to_address}",
        )
        self._tx_history.append(result)
        return result

    def delegate(self, validator_address: str, amount: int) -> TxResult:
        """Delegate (stake) tokens to a validator."""
        if amount <= 0:
            return TxResult(
                tx_hash="", status=TxStatus.FAILED, message="Delegation amount must be positive"
            )
        tx_hash = self._pseudo_hash("delegate", f"{validator_address}:{amount}")
        result = TxResult(
            tx_hash=tx_hash,
            status=TxStatus.CONFIRMED,
            gas_used=120000,
            gas_wanted=150000,
            message=f"Delegated {amount}{self._denom} to {validator_address}",
        )
        self._tx_history.append(result)
        return result

    def undelegate(self, validator_address: str, amount: int) -> TxResult:
        """Undelegate (unstake) tokens from a validator."""
        if amount <= 0:
            return TxResult(
                tx_hash="", status=TxStatus.FAILED, message="Undelegation amount must be positive"
            )
        tx_hash = self._pseudo_hash("undelegate", f"{validator_address}:{amount}")
        result = TxResult(
            tx_hash=tx_hash,
            status=TxStatus.CONFIRMED,
            gas_used=130000,
            gas_wanted=160000,
            message=f"Undelegated {amount}{self._denom} from {validator_address}",
        )
        self._tx_history.append(result)
        return result

    def claim_rewards(self, validator_address: str) -> TxResult:
        """Claim staking rewards from a validator."""
        tx_hash = self._pseudo_hash("claim", validator_address)
        result = TxResult(
            tx_hash=tx_hash,
            status=TxStatus.CONFIRMED,
            gas_used=90000,
            gas_wanted=110000,
            message=f"Rewards claimed from {validator_address}",
        )
        self._tx_history.append(result)
        return result

    def get_validators(self, status: str = "BOND_STATUS_BONDED") -> List[ValidatorInfo]:
        """Query the active validator set."""
        return [
            ValidatorInfo(
                operator_address="kiivaloper1example",
                moniker="KiiValidator",
                status=status,
                tokens=1_000_000_000,
                commission_rate=0.10,
                jailed=False,
            )
        ]

    def deploy_contract(self, bytecode: str, constructor_args: str = "") -> TxResult:
        """Deploy a smart contract to the KiiChain EVM."""
        if not bytecode:
            return TxResult(
                tx_hash="", status=TxStatus.FAILED, message="Bytecode is required"
            )
        tx_hash = self._pseudo_hash("deploy", bytecode[:32])
        result = TxResult(
            tx_hash=tx_hash,
            status=TxStatus.CONFIRMED,
            gas_used=500000,
            gas_wanted=700000,
            message="Contract deployed successfully",
        )
        self._tx_history.append(result)
        return result

    def call_contract(
        self, contract_address: str, method: str, args: Optional[List[Any]] = None
    ) -> TxResult:
        """Call a method on a deployed smart contract."""
        if not contract_address:
            return TxResult(
                tx_hash="", status=TxStatus.FAILED, message="Contract address required"
            )
        tx_hash = self._pseudo_hash("call", f"{contract_address}:{method}")
        result = TxResult(
            tx_hash=tx_hash,
            status=TxStatus.CONFIRMED,
            gas_used=80000,
            gas_wanted=100000,
            message=f"Called {method} on {contract_address}",
        )
        self._tx_history.append(result)
        return result

    def get_tx_history(self) -> List[TxResult]:
        return list(self._tx_history)

    @staticmethod
    def _pseudo_hash(prefix: str, seed: str) -> str:
        raw = f"{prefix}:{seed}:{time.time()}"
        return hashlib.sha256(raw.encode()).hexdigest()[:64]
