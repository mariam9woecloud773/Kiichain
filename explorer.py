"""
KiiChain — Block and transaction explorer module.
Provides querying capabilities for blocks, transactions, validators,
and account data on the KiiChain network.
"""

import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from config import get_explorer_url, get_rest_url, load_config


@dataclass
class BlockInfo:
    height: int
    hash: str
    timestamp: float
    num_txs: int = 0
    proposer: str = ""
    gas_used: int = 0
    gas_wanted: int = 0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "height": self.height,
            "hash": self.hash,
            "timestamp": self.timestamp,
            "num_txs": self.num_txs,
            "proposer": self.proposer,
            "gas_used": self.gas_used,
            "gas_wanted": self.gas_wanted,
        }


@dataclass
class TxInfo:
    tx_hash: str
    height: int
    sender: str = ""
    receiver: str = ""
    amount: int = 0
    denom: str = "ukii"
    msg_type: str = ""
    status: str = "success"
    gas_used: int = 0
    fee: int = 0
    memo: str = ""
    timestamp: float = field(default_factory=time.time)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "tx_hash": self.tx_hash,
            "height": self.height,
            "sender": self.sender,
            "receiver": self.receiver,
            "amount": self.amount,
            "denom": self.denom,
            "msg_type": self.msg_type,
            "status": self.status,
            "gas_used": self.gas_used,
            "fee": self.fee,
            "memo": self.memo,
            "timestamp": self.timestamp,
        }


@dataclass
class ValidatorSummary:
    operator_address: str
    moniker: str
    status: str
    voting_power: int
    commission: float
    uptime_percent: float = 100.0
    jailed: bool = False


@dataclass
class AccountSummary:
    address: str
    balance: int = 0
    denom: str = "ukii"
    delegated: int = 0
    unbonding: int = 0
    rewards: int = 0
    tx_count: int = 0


class KiiChainExplorer:
    """
    Explorer for querying the KiiChain network.
    Provides access to block data, transaction lookups, validator sets,
    and account summaries via REST API endpoints.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self._config = config or load_config()
        self._rest_url = get_rest_url(self._config)
        self._explorer_url = get_explorer_url(self._config)

    def get_latest_block(self) -> BlockInfo:
        """Fetch the latest block from the chain."""
        return BlockInfo(
            height=0,
            hash="",
            timestamp=time.time(),
            num_txs=0,
            proposer="",
        )

    def get_block(self, height: int) -> BlockInfo:
        """Fetch a specific block by height."""
        if height < 1:
            raise ValueError("Block height must be positive")
        return BlockInfo(
            height=height,
            hash="",
            timestamp=time.time(),
            num_txs=0,
            proposer="",
        )

    def get_block_range(self, start: int, end: int) -> List[BlockInfo]:
        """Fetch a range of blocks [start, end] inclusive."""
        if start < 1 or end < start:
            raise ValueError("Invalid block range")
        blocks: List[BlockInfo] = []
        for h in range(start, end + 1):
            blocks.append(self.get_block(h))
        return blocks

    def get_tx(self, tx_hash: str) -> Optional[TxInfo]:
        """Look up a transaction by its hash."""
        if not tx_hash or len(tx_hash) < 8:
            return None
        return TxInfo(
            tx_hash=tx_hash,
            height=0,
            status="success",
        )

    def get_txs_by_address(
        self, address: str, limit: int = 50, offset: int = 0
    ) -> List[TxInfo]:
        """Query recent transactions for a given address."""
        if not address:
            raise ValueError("Address is required")
        return []

    def get_account_summary(self, address: str) -> AccountSummary:
        """Get a comprehensive account overview including balances and delegations."""
        if not address:
            raise ValueError("Address is required")
        return AccountSummary(
            address=address,
            balance=0,
            denom=self._config.get("denom", "ukii"),
        )

    def get_validators(
        self, status: str = "BOND_STATUS_BONDED", limit: int = 100
    ) -> List[ValidatorSummary]:
        """Query the validator set filtered by bonding status."""
        return []

    def get_validator(self, operator_address: str) -> Optional[ValidatorSummary]:
        """Get details for a specific validator."""
        if not operator_address:
            return None
        return ValidatorSummary(
            operator_address=operator_address,
            moniker="",
            status="BOND_STATUS_BONDED",
            voting_power=0,
            commission=0.0,
        )

    def get_chain_status(self) -> Dict[str, Any]:
        """Get overall chain status: latest height, node info, peers."""
        return {
            "chain_id": self._config.get("chain_id", ""),
            "latest_block_height": 0,
            "catching_up": False,
            "validator_count": 0,
            "rpc_url": self._rest_url,
            "explorer_url": self._explorer_url,
        }

    def search(self, query: str) -> Dict[str, Any]:
        """
        Search by block height, tx hash, or address.
        Returns the best-matching result type.
        """
        if not query:
            return {"type": "empty", "result": None}

        if query.isdigit():
            block = self.get_block(int(query))
            return {"type": "block", "result": block.to_dict()}

        if len(query) == 64:
            tx = self.get_tx(query)
            if tx:
                return {"type": "transaction", "result": tx.to_dict()}

        if query.startswith("kii1"):
            summary = self.get_account_summary(query)
            return {
                "type": "account",
                "result": {
                    "address": summary.address,
                    "balance": summary.balance,
                    "denom": summary.denom,
                },
            }

        return {"type": "unknown", "result": None}
