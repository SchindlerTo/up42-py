from time import sleep
from typing import Dict, List

from up42.auth import Auth
from up42.asset import Asset
from up42.tools import Tools
from up42.viztools import VizTools

from up42.utils import (
    get_logger,
)

logger = get_logger(__name__)


class Order(VizTools, Tools):
    def __init__(
        self,
        auth: Auth,
        order_id: str,
    ):
        """
        The Order class provides access to the results, parameters and metadata of UP42
        Orders.
        """
        self.auth = auth
        self.workspace_id = auth.workspace_id
        self.order_id = order_id
        self.results = None
        if self.auth.get_info:
            self._info = self.info

    def __repr__(self):
        info = self.info
        return (
            f"Order(order_id: {self.order_id}, assets: {info['assets']}, dataProvider: {info['dataProvider']}, "
            f"status: {info['status']}, createdAt: {info['createdAt']}, updatedAt: {info['updatedAt']})"
        )

    @property
    def info(self) -> Dict:
        """
        Gets the Order information.
        """
        url = f"{self.auth._endpoint()}/workspaces/{self.workspace_id}/orders/{self.order_id}"
        response_json = self.auth._request(request_type="GET", url=url)
        self._info = response_json["data"]
        return response_json["data"]

    @property
    def status(self) -> str:
        """
        Gets the Order status. One of `PLACED`, `FAILED`, `FULFILLED`, `BEING_FULFILLED`, `FAILED_PERMANENTLY`.
        """
        status = self.info["status"]
        logger.info(f"Order is {status}")
        return status

    @property
    def is_fulfilled(self) -> bool:
        """
        Gets `True` if the order is fulfilled, `False` otherwise.
        Also see [status attribute](order.md#up42.order.Order.status).
        """
        return self.status == "FULFILLED"

    @property
    def metadata(self) -> Dict:
        """
        Gets the Order metadata.
        """
        url = f"{self.auth._endpoint()}/workspaces/{self.workspace_id}/orders/{self.order_id}/metadata"
        response_json = self.auth._request(request_type="GET", url=url)
        return response_json["data"]

    def get_assets(self) -> List[Asset]:
        """
        Gets the Order assets or results.
        """
        if self.is_fulfilled:
            assets: List[str] = self.info["assets"]
            return [Asset(self.auth, asset_id=asset) for asset in assets]
        raise ValueError(
            f"Order {self.order_id} is not FULFILLED! Status is {self.status}"
        )

    @classmethod
    def place(cls, auth: Auth, data_provider_name: str, order_params: Dict) -> "Order":
        """
        Places an order.

        Args:
            auth (Auth): An authentication object.
            data_provider_name (str): The data provider name. Currently only `oneatlas` is a supported provider.
            order_params (Dict): Order definition, including `id` and `aoi`.

        Returns:
            Order: The placed order.
        """
        assert (
            data_provider_name == "oneatlas"
        ), "Currently only `oneatlas` is supported as a data provider."
        order_payload = {
            "dataProviderName": data_provider_name,
            "orderParams": order_params,
        }
        url = f"{auth._endpoint()}/workspaces/{auth.workspace_id}/orders"
        response_json = auth._request(request_type="POST", url=url, data=order_payload)
        try:
            order_id = response_json["data"]["id"]  # type: ignore
        except KeyError as e:
            raise ValueError(f"Order was not placed: {response_json}") from e
        order = cls(auth=auth, order_id=order_id)
        logger.info(f"Order {order.order_id} is now {order.status}.")
        return order

    def track_status(self, report_time: int = 120) -> str:
        """`
        Continuously gets the order status until order is fulfilled or failed.

        Internally checks every `report_time` (s) for the status and prints the log.

        Warning:
            When placing orders of items that are in archive or cold storage,
            the order fulfillment can happen up to **24h after order placement**.
            In such cases,
            please make sure to set an appropriate `report_time`.

        Args:
            report_time: The intervall (in seconds) when to get the order status.

        Returns:
            str: The final order status.
        """
        logger.info(
            f"Tracking order status, reporting every {report_time} seconds...",
        )
        time_asleep = 0

        while not self.is_fulfilled:
            status = self.status
            if status in ["PLACED", "BEING_FULFILLED"]:
                if time_asleep != 0 and time_asleep % report_time == 0:
                    logger.info(f"Order is {status}! - {self.order_id}")
            elif status in ["FAILED", "FAILED_PERMANENTLY"]:
                logger.info(f"Order is {status}! - {self.order_id}")
                raise ValueError("Order has failed!")

            sleep(report_time)
            time_asleep += report_time

        logger.info(f"Order is fulfilled successfully! - {self.order_id}")
        return self.status