"""Script de inicialización de datos y modelos para Streamlit Cloud.

Ejecuta el pipeline completo (descarga → limpieza → SQLite → ML) solo si los
artefactos no existen. Se llama automáticamente desde Home.py al arrancar la app.
"""

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT / "src") not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT / "src"))

from observatorio.config import (
    CLEAN_CSV_PATH,
    MODEL_ARTIFACT_PATH,
    RAW_CSV_PATH,
    SQLITE_DB_PATH,
)


def _necesita_inicializacion() -> bool:
    return not SQLITE_DB_PATH.exists() or not MODEL_ARTIFACT_PATH.exists()


def inicializar_datos(verbose: bool = True) -> None:
    """Ejecuta el pipeline completo si la DB o el modelo no existen."""
    if not _necesita_inicializacion():
        if verbose:
            print("✅ Artefactos ya presentes — omitiendo inicialización.")
        return

    print("🚀 Iniciando pipeline de datos y modelos...")

    # ── 1. Descarga ──────────────────────────────────────────────────────────
    from observatorio.data.ingestion import descargar_subconjunto_secop

    if RAW_CSV_PATH.exists():
        import pandas as pd
        df_raw = pd.read_csv(RAW_CSV_PATH)
        print(f"📂 CSV original ya existe ({len(df_raw):,} filas) — omitiendo descarga.")
    else:
        print("📡 Descargando contratos desde datos.gov.co...")
        df_raw, meta = descargar_subconjunto_secop()
        print(f"   ✔ {meta['total_registros_descargados']:,} registros descargados.")

    # ── 2. Limpieza ───────────────────────────────────────────────────────────
    from observatorio.data.cleaning import limpiar_contratos_secop

    if CLEAN_CSV_PATH.exists():
        import pandas as pd
        df_clean = pd.read_csv(CLEAN_CSV_PATH)
        print(f"📂 CSV limpio ya existe ({len(df_clean):,} filas) — omitiendo limpieza.")
    else:
        print("🧹 Limpiando y anonimizando datos...")
        df_clean = limpiar_contratos_secop(df_raw)
        print(f"   ✔ {len(df_clean):,} registros limpios.")

    # ── 3. SQLite ─────────────────────────────────────────────────────────────
    if not SQLITE_DB_PATH.exists():
        from observatorio.data.database import guardar_en_sqlite
        print("💾 Generando base de datos SQLite...")
        total = guardar_en_sqlite(df_clean)
        print(f"   ✔ {total:,} registros indexados en {SQLITE_DB_PATH.name}.")
    else:
        print("📂 SQLite ya existe — omitiendo.")

    # ── 4. Modelo ML ──────────────────────────────────────────────────────────
    if not MODEL_ARTIFACT_PATH.exists():
        _entrenar_modelo(df_clean)
    else:
        print("📂 Modelo ML ya existe — omitiendo entrenamiento.")

    print("✅ Inicialización completada.")


def _entrenar_modelo(df_clean) -> None:
    """Entrena y serializa el pipeline de predicción de prórrogas."""
    import pandas as pd
    from observatorio.ml.features import (
        COLUMNA_OBJETIVO,
        FEATURES_CATEGORICAS_PERMITIDAS,
        FEATURES_NUMERICAS_PERMITIDAS,
        construir_dataset_modelado,
    )
    from observatorio.ml.evaluation import (
        entrenar_y_comparar_modelos,
        guardar_artefacto_y_metadatos,
        generar_tabla_comparativa_prueba,
    )

    print("🤖 Entrenando modelo de predicción de prórrogas...")

    df_modelo = construir_dataset_modelado(df_clean)

    # Partición temporal estricta: último 20% como prueba out-of-time
    corte = int(len(df_modelo) * 0.80)
    df_train = df_modelo.iloc[:corte]
    df_test = df_modelo.iloc[corte:]

    features = FEATURES_NUMERICAS_PERMITIDAS + FEATURES_CATEGORICAS_PERMITIDAS
    X_train = df_train[features]
    y_train = df_train[COLUMNA_OBJETIVO]
    X_test = df_test[features]
    y_test = df_test[COLUMNA_OBJETIVO]

    modelos, resultados_cv, nombre_ganador, modelo_ganador = entrenar_y_comparar_modelos(
        X_train, y_train
    )
    df_metricas = generar_tabla_comparativa_prueba(modelos, X_test, y_test, resultados_cv)
    guardar_artefacto_y_metadatos(
        modelo_ganador, nombre_ganador, df_train, df_test, df_metricas
    )
    pr_auc = df_metricas.loc[nombre_ganador, "PR-AUC"]
    print(f"   ✔ Modelo '{nombre_ganador}' guardado — PR-AUC prueba: {pr_auc:.3f}")


if __name__ == "__main__":
    inicializar_datos(verbose=True)
