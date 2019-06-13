import asyncio
import logging

import settings
from core.cases.orders import Orders

log = logging.getLogger(__name__)


class OrdersQueue:
    """Очередь исполнения заказов

    - проверяет устаревшие выполненные заказы и удаляет их
    - запускает процесс выполнения заказов
    - контроллирует максимальное одновременное количество заказов в работе
    """
    max_active_orders = settings.MAX_ACTIVE_ORDERS

    def __init__(self, orders: Orders):
        self._lock = asyncio.Lock()
        self._running = True
        self._orders = orders
        self._current_active_orders_amount = 0

    async def increase_active_amount(self):
        """Уменьшение доступного количества заказов в работе

        :return:
        """
        with await self._lock:
            self._current_active_orders_amount += 1

    async def decrease_active_amount(self):
        """Увеличение доступного количества заказов в работе

        :return:
        """
        with await self._lock:
            self._current_active_orders_amount -= 1

    async def _run_task(self, order_uid: int):
        """Запуск выполнения заказа в фоне

        :param order_uid:
        :return:
        """
        await self._orders.cook(order_uid)
        await self.decrease_active_amount()

    async def run(self):
        """Запуск процесса обработки заказов

        :return:
        """
        log.info("OrdersQueue was started")
        while self._running:
            await asyncio.sleep(1)
            deleted = await self._orders.delete_outdated()
            if deleted:
                log.info(f"Deleted orders: {', '.join(deleted)}")

            waiting_orders = await self._orders.waiting()
            if not waiting_orders:
                continue

            for order_dict in waiting_orders:
                if self._current_active_orders_amount >= self.max_active_orders:
                    continue

                order_uid = order_dict.get("uid")
                await self.increase_active_amount()
                asyncio.ensure_future(self._run_task(order_uid))

    async def stop(self):
        """Остановка процесса выполнения заказов

        :return:
        """
        self._running = False
        log.info("OrdersQueue was stopped.")
