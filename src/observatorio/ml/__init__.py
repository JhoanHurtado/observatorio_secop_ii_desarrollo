"""Subpaquete de Machine Learning clásico para estimar riesgo de prórroga de plazo."""

from observatorio.ml.features import (
    COLUMNA_OBJETIVO,
    FEATURES_CATEGORICAS_PERMITIDAS,
    FEATURES_NUMERICAS_PERMITIDAS,
    VARIABLES_EXCLUIDAS_LEAKAGE,
    construir_dataset_modelado,
    verificar_ausencia_leakage,
)
from observatorio.ml.pipeline import (
    construir_modelos,
    construir_preprocesador,
    evaluar_modelo,
)
from observatorio.ml.evaluation import (
    analizar_errores_por_modalidad,
    calcular_importancia_variables,
    entrenar_y_comparar_modelos,
    generar_tabla_comparativa_prueba,
    guardar_artefacto_y_metadatos,
)
from observatorio.ml.inference import (
    cargar_modelo_prorrogas,
    predecir_riesgo_prorroga,
)

__all__ = [
    "COLUMNA_OBJETIVO",
    "FEATURES_CATEGORICAS_PERMITIDAS",
    "FEATURES_NUMERICAS_PERMITIDAS",
    "VARIABLES_EXCLUIDAS_LEAKAGE",
    "construir_dataset_modelado",
    "verificar_ausencia_leakage",
    "construir_modelos",
    "construir_preprocesador",
    "evaluar_modelo",
    "entrenar_y_comparar_modelos",
    "generar_tabla_comparativa_prueba",
    "calcular_importancia_variables",
    "analizar_errores_por_modalidad",
    "guardar_artefacto_y_metadatos",
    "cargar_modelo_prorrogas",
    "predecir_riesgo_prorroga",
]
