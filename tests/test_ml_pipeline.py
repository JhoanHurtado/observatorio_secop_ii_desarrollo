"""Pruebas unitarias para el pipeline y preprocesador de Machine Learning (RF-ML2, RF-ML3, RF-ML6)."""

import pandas as pd
import numpy as np
import pytest
from observatorio.ml.features import (
    FEATURES_CATEGORICAS_PERMITIDAS,
    FEATURES_NUMERICAS_PERMITIDAS,
    construir_dataset_modelado,
)
from observatorio.ml.pipeline import construir_modelos, evaluar_modelo
from observatorio.ml.inference import predecir_riesgo_prorroga


def test_construir_dataset_modelado_crea_columnas() -> None:
    df_dummy = pd.DataFrame(
        [
            {
                "id_contrato": "CO1.1",
                "fecha_de_firma": "2023-01-15",
                "fecha_de_inicio_del_contrato": "2023-01-20",
                "fecha_de_fin_del_contrato": "2023-06-30",
                "dias_adicionados": 30,
                "valor_del_contrato": 50_000_000.0,
                "codigo_de_categoria_principal": "V1.80111600",
            },
            {
                "id_contrato": "CO1.2",
                "fecha_de_firma": "2023-02-10",
                "fecha_de_inicio_del_contrato": "2023-02-15",
                "fecha_de_fin_del_contrato": "2023-05-30",
                "dias_adicionados": 0,
                "valor_del_contrato": 12_000_000.0,
                "codigo_de_categoria_principal": "V1.80111501",
            },
        ]
    )
    dm = construir_dataset_modelado(df_dummy, fecha_corte="2023-12-31")
    assert "prorroga" in dm.columns
    assert dm["prorroga"].iloc[0] == 1
    assert dm["prorroga"].iloc[1] == 0
    assert "valor_contrato_log" in dm.columns
    assert "duracion_planeada_dias" in dm.columns
    assert "segmento_unspsc" in dm.columns


def test_modelos_entrenan_y_evaluan() -> None:
    np.random.seed(42)
    n = 100
    df_train = pd.DataFrame({
        "valor_contrato_log": np.random.uniform(10, 20, n),
        "mes_firma": np.random.randint(1, 13, n),
        "anio_firma": np.random.choice([2023], n),
        "duracion_planeada_dias": np.random.randint(30, 360, n),
        "tipo_de_contrato": np.random.choice(["Prestación de servicios", "Obra"], n),
        "modalidad_de_contratacion": np.random.choice(["Contratación directa", "Mínima cuantía"], n),
        "sector": np.random.choice(["Salud", "Educación"], n),
        "rama": ["Ejecutivo"] * n,
        "orden": ["Territorial"] * n,
        "departamento": ["Valle del Cauca"] * n,
        "es_pyme": ["No"] * n,
        "es_grupo": ["No"] * n,
        "habilita_pago_adelantado": ["No"] * n,
        "origen_de_los_recursos": ["Recursos Propios"] * n,
        "segmento_unspsc": ["80"] * n,
    })
    y_train = pd.Series(np.random.choice([0, 1], p=[0.85, 0.15], size=n))

    modelos = construir_modelos()
    assert "Baseline" in modelos
    assert "Regresión Logística" in modelos
    assert "Random Forest" in modelos

    # Entrenar y evaluar baseline y logistica
    rf = modelos["Random Forest"]
    rf.fit(df_train, y_train)
    metricas = evaluar_modelo(rf, df_train, y_train)
    assert "PR-AUC" in metricas
    assert "ROC-AUC" in metricas

    # Inferencia individual
    registro = df_train.iloc[0].to_dict()
    pred = predecir_riesgo_prorroga(rf, registro)
    assert 0.0 <= pred["probabilidad_prorroga"] <= 1.0
    assert pred["nivel_riesgo"] in [
        "Bajo",
        "Medio (Seguimiento recomendado)",
        "Alto (Priorizar revisión preventiva)",
    ]

