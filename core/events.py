from collections import defaultdict
from threading import Lock
from typing import Callable, Dict, List, Any

from core.websocket_manager import ws_manager


class EventBus:

    def __init__(self):

        self._listeners: Dict[str, List[Callable]] = defaultdict(list)

        self._lock = Lock()

    # ==========================================
    # Registrar listener
    # ==========================================

    def subscribe(self, event_name: str, callback: Callable):

        with self._lock:

            if callback not in self._listeners[event_name]:

                self._listeners[event_name].append(callback)

    # ==========================================
    # Eliminar listener
    # ==========================================

    def unsubscribe(self, event_name: str, callback: Callable):

        with self._lock:

            if callback in self._listeners[event_name]:

                self._listeners[event_name].remove(callback)

    # ==========================================
    # Emitir evento
    # ==========================================

    def emit(self, event_name: str, data: Any = None):

        listeners = list(

            self._listeners.get(event_name, [])

        )

        # Ejecutar listeners

        for callback in listeners:

            try:

                callback(data)

            except Exception as e:

                print(f"[EVENT ERROR] {event_name}: {e}")

        # Enviar al WebSocket

        try:

            ws_manager.send({

                "event": event_name,

                "data": data

            })

        except Exception:

            pass

    # ==========================================
    # Disparar evento sin datos
    # ==========================================

    def fire(self, event_name: str):

        self.emit(event_name, None)

    # ==========================================
    # ¿Tiene listeners?
    # ==========================================

    def has(self, event_name: str):

        return len(self._listeners.get(event_name, [])) > 0

    # ==========================================
    # Limpiar todos
    # ==========================================

    def clear(self):

        with self._lock:

            self._listeners.clear()

    # ==========================================
    # Obtener listeners
    # ==========================================

    def listeners(self, event_name: str):

        return self._listeners.get(event_name, [])

    # ==========================================
    # Cantidad de listeners
    # ==========================================

    def count(self, event_name: str = None):

        if event_name is None:

            return sum(

                len(v)

                for v in self._listeners.values()

            )

        return len(

            self._listeners.get(event_name, [])

        )


events = EventBus()