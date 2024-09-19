"""Run bot command module."""

from typing import Any, Dict, Tuple

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Run bot command."""

    help = "Run bot"  # noqa: A003

    def handle(self, *args: Tuple[Any, ...], **kwargs: Dict[str, Any]) -> None:
        """Start handling."""
        from core.bot import bot

        bot.polling(non_stop=True)
