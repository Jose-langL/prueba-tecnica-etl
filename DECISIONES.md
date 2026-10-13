# Decisiones y supuestos

> Plantilla a completar por el candidato. No hace falta que sea larga; sí que
> sea específica: ejemplos reales de los datos, no frases generales.

## 1. Hallazgos en los datos

Una fila por problema que encontraste en los archivos del padrón.

| # | Columna | Qué encontraste | Ejemplo | Qué hiciste | Por qué |
|---|---|---|---|---|---|
| 1 | `sexo` | Hay valores en minúscula y nombres completos también hay valores vacíos. | En `empadronados_20260302.csv`: `m`, `FEMENINO` y vacío. | Convertir `m`/`MASCULINO` a `M`, `f`/`FEMENINO` a `F`; los vacíos quedan como `NULL`. | La especificación pide guardar `M` o `F` y conservar el valor vacío como nulo. |
| 2 | `estado_registro` | `activo` y `suspendido` aparecen con mayúsculas o capitalización mixta. | `ACTIVO` y `Activo` en `empadronados_20260302.csv`. | Normalizar a minúsculas y conservar las categorías `activo`, `suspendido` y `fallecido`. | Cumpliendo el formato estandar solicitado. |
| 3 | `rango_edad` | Hay rangos expresados con palabras además de los códigos estándar. | `18 a 25`, `26 a 35` y `mayor de 60` en `empadronados_20260303.csv`. | Mapearlos a `18-25`, `26-35` y `61+`; mantener las categorías que ya vienen estándar. | La tabla requiere una de las cinco categorías canónicas; el formato es `26-35`, sin espacios. |
| 4 | `fecha_inscripcion` | Hay dos formatos: ISO (`YYYY-MM-DD`) y día/mes/año (`DD/MM/YYYY`)| `2004-02-03` y `09/05/2018` (ID `E0003718`, archivo `empadronados_20260303.csv`). | Interpretar el formato con barras como `DD/MM/YYYY` y convertirlo a `YYYY-MM-DD`.| La salida debe estar en `YYYY-MM-DD`; además, existen valores como `13/11/2003`, por lo que el primer componente representa el día. |
| 5 | `id_empadronado` | Cada archivo contiene 25 IDs repetidos. Los grupos revisados tienen filas idénticas, no versiones contradictorias. | En `empadronados_20260302.csv`, `E0000943` aparece en las filas 81 y 4238 con los mismos datos. | Deduplicar por `id_empadronado` y conservar una fila. Si hay duplicados con datos distintos, conservar la última aparición y registrar el criterio. | Evita cargar más de una fila por persona y deja definido un criterio reproducible para conflictos. |

## 2. Decisiones

Responde en pocas líneas cada una:

- Si dos filas tienen el mismo `id_empadronado` pero difieren, conservaré la última aparición del archivo; si son idénticas, conservaré una. La carga debe insertar o actualizar por ID.
- Una fecha que no se puede interpretar se rechaza, se cuenta y se registra en el log con el motivo; no debe desaparecer silenciosamente.
- La carga debe insertar o actualizar usando `id_empadronado` como clave. Repetir una fecha debe dejar las mismas filas y los mismos datos.
- **Pregunta de razonamiento (no hace falta programarla):** si ya cargaste el
  día 04 y luego vuelves a procesar el día 03, ¿qué queda en la base? ¿Es un
  problema? ¿Cómo lo evitarías?

## 3. Supuestos

| # | Supuesto | Motivo |
|---|---|---|
| 1 | | |

## 4. Qué no alcancé a hacer

| # | Pendiente | Cómo lo abordaría |
|---|---|---|
| 1 | | |

## 5. Análisis de la base de datos (opcional)

Si te sobra tiempo: mira `sql/01_ddl_electoral.sql` y `docs/BASE_DE_DATOS.md` y
anota entre 3 y 5 problemas del modelo, sobre todo los que notaste al cargar el
padrón. Una línea por problema, qué consecuencia tiene y una mejora posible. No
se pide un diagrama ni un modelo nuevo.

| # | Problema | Consecuencia | Mejora posible |
|---|---|---|---|
| 1 | | | |
