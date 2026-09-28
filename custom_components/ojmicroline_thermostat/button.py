"""Buttons for OJ Microline thermostats."""

from __future__ import annotations

from typing import TYPE_CHECKING

from homeassistant.components.button import ButtonEntity, ButtonEntityDescription

from .const import DOMAIN
from .models import OJMicrolineEntity

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback

    from .coordinator import OJMicrolineDataUpdateCoordinator

REFRESH_BUTTON = ButtonEntityDescription(
    name="Refresh data",
    icon="mdi:refresh",
    key="refresh",
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Load all OJMicroline Thermostat buttons.

    Args:
    ----
        hass: The HomeAssistant instance.
        entry: The ConfigEntry containing the user input.
        async_add_entities: The callback to provide the created entities to.

    """
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities(
        OJMicrolineRefreshButton(coordinator, idx, REFRESH_BUTTON)
        for idx in coordinator.data.keys()  # noqa: SIM118
    )


class OJMicrolineRefreshButton(OJMicrolineEntity, ButtonEntity):
    """Button that fetches fresh data from the OJ Microline API."""

    entity_description: ButtonEntityDescription

    def __init__(
        self,
        coordinator: OJMicrolineDataUpdateCoordinator,
        idx: str,
        entity_description: ButtonEntityDescription,
    ) -> None:
        """Initialise the entity.

        Args:
        ----
            coordinator: The data coordinator updating the models.
            idx: The identifier for this entity.
            entity_description: The description of the button.

        """
        super().__init__(coordinator, idx)

        self.entity_description = entity_description

        self._attr_unique_id = f"{idx}_{entity_description.key}"
        self._attr_name = f"{coordinator.data[idx].name} {entity_description.name}"

    async def async_press(self) -> None:
        """Fetch new data for all thermostats of this account right away."""
        await self.coordinator.async_refresh()
