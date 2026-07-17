""" Modulo que gestiona los cambios de estilo y narrativa de ADAM a lo largo del tiempo
    para permitir análisis, resúmen y revisión.
"""
import json
from collections import deque
from datetime import datetime, timezone
from typing import Any, List, Dict, Optional

ISO_FMT = "%Y-%m-%dT%H:%M:%S.%fZ"

class EvolutionTracker:
    def __init__(self, max_history: int = 500, persist_path: Optional[str] = None):                                    # 'persist_path' : ruta del archivo del historial
        self.max_history = max_history
        self.persist_path = persist_path
        self._history = deque(maxlen=self.max_history)                                                                 # _history es el historial de cambios narrativos, registra, consulta, resume y persiste cambios.

        if self.persist_path:
            try:
                self._load()
            except Exception:
                self._history = deque(maxlen=self.max_history)                                                        # 'maxlen': limite de tamaño, elimina automaticamente el más antiguo | 'max_history': ultimos cambios 

    def _now(self) -> str:
        return datetime.now(timezone.utc).strftime(ISO_FMT)
    
    def detect_narrative_shift(self, before: Dict[str, Any], after: Dict[str, Any]) -> List[str]:
        shifts = []

        if before.get("estilo") != after.get("estilo"):
            shifts.append("Cambio de estilo narrativo")

        if before.get("humor") != after.get("humor"):
            shifts.append("Cambio de humor")

        if before.get("firma_narrativa") != after.get("firma_narrativa"):
            shifts.append("Cambio de firma narrativa")
        
        if before.get("nivel_ironía") != after.get("nivel_ironía"):
            shifts.append("Cambio en el nivel de ironía")
        
        if before.get("nivel_formalidad") != after.get("nivel_formalidad"):
            shifts.append("Cambio en el nivel de formalidad")
        return shifts

    def record_change(
            self,
            source: str,
            before: Dict[str, Any],
            after: Dict[str, Any],
            reason: Optional[str] = None,
            user_profile: Optional[Dict[str, Any]] = None
        ):
            if before == after:
                return
            
            tags = self.detect_narrative_shift(before, after)                                                         

            entry = {
                "timestamp": self._now(),
                "source": source,
                "before": before,
                "after": after,
                "reason": reason or "",
                "tags": tags,
                "user_perfil": user_profile or {}
            }

            self._history.appendleft(entry)
            if self.persist_path:
                self._save()

    def get_history(self, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        if limit is None:
            return list(self._history)
        return list(self._history)[:limit]
    
    # diccionario resumen del estado actual del historial de 'entries'  
    def summarize_evolution(self, window: Optional[int] = None) -> Dict[str, Any]:
        entries = self.get_history(window)
        summary = {
            "total_events": len(entries),                                                                             # diccionario vacio que cuenta el número de elementos en 'entries'
            "sources_count": {},                                                                                      # diccionario  vacio para registrar quien o que está generando más cambios.
            "fields_changed_count": {},                                                                               # diccionario vacio que cuenta el numero de cambios de cada campo, nombre, estado, etc.
            "tags_count": {},
            "last_state": entries[0]["after"] if entries else None,                                                   # Si la lista no está vacia, toma el primer elemento[0] y extrae su 'after' como el primer argumento registrado.
            "first_timestamp": entries[-1]["timestamp"] if entries else None,                                         # Si la lista no está vacia, toma el ultimo elemento[-1] y extrae su 'timestamp' como el primer argumento registrado.
            "last_timestamp": entries[0]["timestamp"] if entries else None                                            # Si la lista no está vacia, toma el primer elemento[0] y extrae su 'timestamp' como el primer argumento registrado.
        }

        for e in entries:
            src = e["source"]
            summary["sources_count"].setdefault(src, 0)
            summary["sources_count"][src] += 1

            for tag in e.get("tags", []):
                summary["tags_count"].setdefault(tag, 0)
                summary["tags_count"][tag] += 1
                 
            before = e.get("before", {}) or {}
            after = e.get("after", {}) or {}
             
            for k in set(before.keys() | after.keys()):
                if before.get(k) != after.get(k):
                    summary["fields_changed_count"].setdefault(k, 0)
                    summary["fields_changed_count"][k] += 1

        return summary
    
    def rollback_to(self, index: int = 0) -> Optional[Dict[str, Any]]:
            if index < 0 or index >= len(self._history):
                return None
            return list(self._history)[index]["after"]
    
    def get_change_timeline(self) -> Dict[str, Any]:
        timeline = {}
        for e in self._history:
            day = e["timestamp"][:10]
            timeline.setdefault(day, 0)
            timeline[day] += 1  
        return timeline


    def clear_history(self):
        self._history.clear()
        if self.persist_path:
            try:
                with open(self.persist_path, "w", encoding = "utf-8") as f:
                    json.dump([], f, ensure_ascii = False, indent = 2)
            except Exception as e:
                pass

    def export_history(self, path: str):
        try: 
            with open(path, "w", encoding = "utf-8") as f:
                json.dump(list(self._history), f, ensure_ascii = False, indent = 2)

        except Exception as e:
            print(f"Error al exportar el historial: {e}")

    def _save(self):
        try: 
            with open(self.persist_path, "w", encoding = "utf-8") as f:
                json.dump(list(self._history), f, ensure_ascii = False, indent = 2)

        except Exception as e:
            pass

    def _load(self):
        with open(self.persist_path, "r", encoding = "utf-8") as f:
            data = json.load(f)
        self._history = deque(json.load(f), maxlen = self.max_history)