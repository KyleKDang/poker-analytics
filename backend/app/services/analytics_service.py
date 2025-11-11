from typing import Any
from sqlmodel import select, func
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.hand import Hand
from app.models.session import Session


class AnalyticsService:
    """Service for calculating poker analytics and statistics."""

    @staticmethod
    async def get_overall_stats(db: AsyncSession, user_id: int) -> dict[str, Any]:
        """Calculate overall statistics for a user."""
        # Get all hands for user
        stmt = select(Hand).join(Session).where(Session.user_id == user_id)
        result = await db.exec(stmt)
        hands = result.all()

        if not hands:
            return {
                "total_hands": 0,
                "win_rate": 0.0,
                "total_sessions": 0,
                "vpip": 0.0,
                "aggression_factor": 0.0,
            }

        total_hands = len(hands)
        wins = sum(1 for h in hands if h.result == "win")
        losses = sum(1 for h in hands if h.result == "loss")
        ties = sum(1 for h in hands if h.result == "tie")

        # VPIP: % of hands where didn't fold
        vpip_hands = sum(
            1 for h in hands if h.action_taken and h.action_taken != "fold"
        )
        vpip = (vpip_hands / total_hands * 100) if total_hands > 0 else 0.0

        # Aggression Factor: (raises) / (calls + checks)
        raises = sum(1 for h in hands if h.action_taken == "raise")
        calls = sum(1 for h in hands if h.action_taken == "call")
        checks = sum(1 for h in hands if h.action_taken == "check")
        aggression = (raises / (calls + checks)) if (calls + checks) > 0 else 0.0

        # Get total sessions
        session_stmt = select(func.count(Session.id)).where(Session.user_id == user_id)
        session_result = await db.exec(session_stmt)
        total_sessions = session_result.one()

        return {
            "total_hands": total_hands,
            "win_rate": (wins / total_hands * 100) if total_hands > 0 else 0.0,
            "wins": wins,
            "losses": losses,
            "ties": ties,
            "total_sessions": total_sessions,
            "vpip": round(vpip, 2),
            "aggression_factor": round(aggression, 2),
        }

    @staticmethod
    async def get_position_stats(db: AsyncSession, user_id: int) -> dict[str, Any]:
        """Calculate statistics by position."""
        stmt = select(Hand).join(Session).where(Session.user_id == user_id)
        result = await db.exec(stmt)
        hands = result.all()

        positions = {}
        for hand in hands:
            pos = hand.player_position
            if pos not in positions:
                positions[pos] = {"total": 0, "wins": 0, "losses": 0, "ties": 0}

            positions[pos]["total"] += 1
            if hand.result == "win":
                positions[pos]["wins"] += 1
            elif hand.result == "loss":
                positions[pos]["losses"] += 1
            elif hand.result == "tie":
                positions[pos]["ties"] += 1

        # Calculate win rates
        position_data = []
        for pos, stats in positions.items():
            win_rate = (
                (stats["wins"] / stats["total"] * 100) if stats["total"] > 0 else 0.0
            )
            position_data.append(
                {
                    "position": pos,
                    "total_hands": stats["total"],
                    "wins": stats["wins"],
                    "losses": stats["losses"],
                    "ties": stats["ties"],
                    "win_rate": round(win_rate, 2),
                }
            )

        # Sort by position order: early, middle, late
        order = {"early": 0, "middle": 1, "late": 2}
        position_data.sort(key=lambda x: order.get(x["position"], 99))

        return {"positions": position_data}

    @staticmethod
    async def get_action_stats(db: AsyncSession, user_id: int) -> dict[str, Any]:
        """Calculate statistics by action."""
        stmt = select(Hand).join(Session).where(Session.user_id == user_id)
        result = await db.exec(stmt)
        hands = result.all()

        actions = {}
        for hand in hands:
            if not hand.action_taken:
                continue

            action = hand.action_taken
            if action not in actions:
                actions[action] = {"total": 0, "wins": 0, "losses": 0, "ties": 0}

            actions[action]["total"] += 1
            if hand.result == "win":
                actions[action]["wins"] += 1
            elif hand.result == "loss":
                actions[action]["losses"] += 1
            elif hand.result == "tie":
                actions[action]["ties"] += 1

        # Calculate win rates and distribution
        action_data = []
        total_actions = sum(stats["total"] for stats in actions.values())

        for action, stats in actions.items():
            win_rate = (
                (stats["wins"] / stats["total"] * 100) if stats["total"] > 0 else 0.0
            )
            distribution = (
                (stats["total"] / total_actions * 100) if total_actions > 0 else 0.0
            )

            action_data.append(
                {
                    "action": action,
                    "total_hands": stats["total"],
                    "wins": stats["wins"],
                    "losses": stats["losses"],
                    "ties": stats["ties"],
                    "win_rate": round(win_rate, 2),
                    "distribution": round(distribution, 2),
                }
            )

        # Sort by action order
        order = {"fold": 0, "check": 1, "call": 2, "raise": 3}
        action_data.sort(key=lambda x: order.get(x["action"], 99))

        return {"actions": action_data}

    @staticmethod
    async def get_win_rate_over_time(db: AsyncSession, user_id: int) -> dict[str, Any]:
        """Calculate cumulative win rate over time."""
        stmt = (
            select(Hand)
            .join(Session)
            .where(Session.user_id == user_id)
            .order_by(Hand.created_at)
        )
        result = await db.exec(stmt)
        hands = result.all()

        timeline = []
        cumulative_wins = 0
        cumulative_total = 0

        for hand in hands:
            cumulative_total += 1
            if hand.result == "win":
                cumulative_wins += 1

            win_rate = (
                (cumulative_wins / cumulative_total * 100)
                if cumulative_total > 0
                else 0.0
            )

            timeline.append(
                {
                    "hand_number": cumulative_total,
                    "date": hand.created_at.isoformat(),
                    "win_rate": round(win_rate, 2),
                    "cumulative_wins": cumulative_wins,
                    "cumulative_hands": cumulative_total,
                }
            )

        return {"timeline": timeline}

    @staticmethod
    async def get_session_performance(db: AsyncSession, user_id: int) -> dict[str, Any]:
        """Calculate performance by session."""
        stmt = (
            select(Session)
            .where(Session.user_id == user_id)
            .order_by(Session.start_time.desc())
        )
        result = await db.exec(stmt)
        sessions = result.all()

        session_data = []
        for session in sessions:
            # Get hands for this session
            hands_stmt = select(Hand).where(Hand.session_id == session.id)
            hands_result = await db.exec(hands_stmt)
            hands = hands_result.all()

            total_hands = len(hands)
            wins = sum(1 for h in hands if h.result == "win")
            losses = sum(1 for h in hands if h.result == "loss")
            ties = sum(1 for h in hands if h.result == "tie")
            win_rate = (wins / total_hands * 100) if total_hands > 0 else 0.0

            session_data.append(
                {
                    "session_id": session.id,
                    "notes": session.notes,
                    "start_time": session.start_time.isoformat(),
                    "total_hands": total_hands,
                    "wins": wins,
                    "losses": losses,
                    "ties": ties,
                    "win_rate": round(win_rate, 2),
                }
            )

        return {"sessions": session_data}

    @staticmethod
    async def get_position_heatmap(db: AsyncSession, user_id: int) -> dict[str, Any]:
        """Generate position heat map data."""
        position_stats = await AnalyticsService.get_position_stats(db, user_id)

        heatmap_data = []
        for pos_data in position_stats["positions"]:
            heatmap_data.append(
                {
                    "position": pos_data["position"],
                    "win_rate": pos_data["win_rate"],
                    "total_hands": pos_data["total_hands"],
                }
            )

        return {"heatmap": heatmap_data}

    @staticmethod
    async def get_playing_style_profile(
        db: AsyncSession, user_id: int
    ) -> dict[str, Any]:
        """Calculate playing style metrics."""
        stmt = select(Hand).join(Session).where(Session.user_id == user_id)
        result = await db.exec(stmt)
        hands = result.all()

        if not hands:
            return {
                "vpip": 0.0,
                "aggression_factor": 0.0,
                "fold_frequency": 0.0,
                "raise_frequency": 0.0,
                "style_rating": "Unknown",
            }

        total_hands = len(hands)

        # VPIP
        vpip_hands = sum(
            1 for h in hands if h.action_taken and h.action_taken != "fold"
        )
        vpip = (vpip_hands / total_hands * 100) if total_hands > 0 else 0.0

        # Aggression
        raises = sum(1 for h in hands if h.action_taken == "raise")
        calls = sum(1 for h in hands if h.action_taken == "call")
        checks = sum(1 for h in hands if h.action_taken == "check")
        aggression = (raises / (calls + checks)) if (calls + checks) > 0 else 0.0

        # Fold frequency
        folds = sum(1 for h in hands if h.action_taken == "fold")
        fold_freq = (folds / total_hands * 100) if total_hands > 0 else 0.0

        # Raise frequency
        raise_freq = (raises / total_hands * 100) if total_hands > 0 else 0.0

        # Determine style
        if vpip < 20:
            tight_loose = "Very Tight"
        elif vpip < 30:
            tight_loose = "Tight"
        elif vpip < 40:
            tight_loose = "Balanced"
        elif vpip < 50:
            tight_loose = "Loose"
        else:
            tight_loose = "Very Loose"

        if aggression < 0.5:
            passive_aggressive = "Very Passive"
        elif aggression < 1.0:
            passive_aggressive = "Passive"
        elif aggression < 2.0:
            passive_aggressive = "Balanced"
        elif aggression < 3.0:
            passive_aggressive = "Aggressive"
        else:
            passive_aggressive = "Very Aggressive"

        style_rating = f"{tight_loose} & {passive_aggressive}"

        return {
            "vpip": round(vpip, 2),
            "aggression_factor": round(aggression, 2),
            "fold_frequency": round(fold_freq, 2),
            "raise_frequency": round(raise_freq, 2),
            "tight_loose": tight_loose,
            "passive_aggressive": passive_aggressive,
            "style_rating": style_rating,
        }
