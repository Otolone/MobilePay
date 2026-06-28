from models.wallet import Wallet
from database.db import db
from utils.money import to_decimal, to_amount


class MTNWalletProvider:

    PROVIDER_NAME = "MTN"

    # Deposit via MTN channel
    def deposit(self, user_id, amount):

        wallet = Wallet.query.filter_by(user_id=user_id).first()

        if not wallet:
            return {"success": False, "message": "Wallet not found"}, 404

        wallet.balance = to_decimal(wallet.balance) + to_decimal(amount)
        db.session.commit()

        return {
            "success": True,
            "provider": self.PROVIDER_NAME,
            "message": "MTN deposit successful",
            "balance": to_amount(wallet.balance)
        }, 200

    # Simulated withdrawal via MTN
    def withdraw(self, user_id, amount):

        wallet = Wallet.query.filter_by(user_id=user_id).first()

        if not wallet:
            return {"success": False, "message": "Wallet not found"}, 404

        if to_decimal(wallet.balance) < to_decimal(amount):
            return {"success": False, "message": "Insufficient balance"}, 400

        wallet.balance = to_decimal(wallet.balance) - to_decimal(amount)
        db.session.commit()

        return {
            "success": True,
            "provider": self.PROVIDER_NAME,
            "message": "MTN withdrawal successful",
            "balance": to_amount(wallet.balance)
        }, 200