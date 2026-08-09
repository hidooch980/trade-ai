from app.market.universe.symbol_universe import canonical, category


class RiskGovernor:

    def calculate_position_size(
        self,
        capital,
        risk_percent,
        entry_price,
        stop_loss,
        symbol=None,
        strategy_weight=1
    ):
        symbol = canonical(symbol) if symbol else ""
        asset_class = category(symbol)

        risk_amount = (
            capital
            * (risk_percent / 100)
            * strategy_weight
        )

        distance = abs(entry_price - stop_loss)

        if distance <= 0:
            return {
                "approved": False,
                "reason": "INVALID_STOP_LOSS"
            }

        if risk_amount <= 0:
            return {
                "approved": False,
                "reason": "INVALID_RISK_AMOUNT"
            }

        # Position sizing by asset class.
        if asset_class == "FOREX":
            # Standard FX lot approximation:
            # 1 lot ~= 100,000 base units.
            volume = risk_amount / (distance * 100000)
            min_volume = 0.01
            max_volume = 10.0

        elif asset_class == "METALS":
            # Metals are broker-specific. Use a conservative
            # contract approximation and normalize to 0.01 lots.
            volume = risk_amount / (distance * 100)
            min_volume = 0.01
            max_volume = 10.0

        elif asset_class == "INDICES":
            # Index CFD sizing is broker-specific.
            volume = risk_amount / distance
            min_volume = 0.01
            max_volume = 10.0

        elif asset_class == "CRYPTO":
            # Crypto volume is expressed in coin/contracts.
            volume = risk_amount / distance
            min_volume = 0.001
            max_volume = 10.0

        else:
            volume = risk_amount / distance
            min_volume = 0.01
            max_volume = 10.0

        volume = min(volume, max_volume)

        # Do not fabricate risk capacity.
        # If calculated size is below broker minimum, reject it.
        if volume < min_volume:
            return {
                "approved": False,
                "reason": "POSITION_SIZE_BELOW_MINIMUM",
                "asset_class": asset_class,
                "symbol": symbol,
                "risk_amount": round(risk_amount, 4),
                "stop_distance": round(distance, 8),
                "calculated_volume": round(volume, 6),
                "minimum_volume": min_volume,
                "entry_price": entry_price
            }

        # Normalize to practical broker precision.
        if min_volume == 0.001:
            volume = round(volume, 3)
        else:
            volume = round(volume, 2)

        if volume <= 0:
            return {
                "approved": False,
                "reason": "ZERO_VOLUME_AFTER_NORMALIZATION",
                "asset_class": asset_class,
                "symbol": symbol
            }

        return {
            "approved": True,
            "risk_amount": round(risk_amount, 4),
            "stop_distance": round(distance, 8),
            "volume": volume,
            "entry_price": entry_price,
            "stop_loss": stop_loss,
            "asset_class": asset_class,
            "symbol": symbol
        }

    def validate_drawdown(self, current_loss_percent):
        if current_loss_percent >= 10:
            return {
                "approved": False,
                "status": "DRAWDOWN_LIMIT"
            }

        return {
            "approved": True,
            "status": "SAFE"
        }


risk_governor = RiskGovernor()
