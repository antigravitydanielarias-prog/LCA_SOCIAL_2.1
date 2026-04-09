"""
Módulo de cálculos del Modelo 2.0
Genera micro-redes, determina gates, calcula costos
"""
import pandas as pd
import numpy as np
from datetime import datetime
import json
from config import (
    DIMENSIONES, GATE_THRESHOLDS, GATE_STATES, 
    ACTORES, FASES, SUBCAPAS
)

def calcular_micro_red(actor, fase, subcapa, datos):
    """
    Calcula una micro-red completa para actor × fase × subcapa
    
    Retorna: dict con diagnóstico completo y estado de gate
    """
    
    # Validar inputs
    if actor not in ACTORES:
        raise ValueError(f"Actor inválido: {actor}")
    if fase not in [1, 2, 3]:
        raise ValueError(f"Fase inválida: {fase}")
    if subcapa not in ['A', 'B', 'C']:
        raise ValueError(f"Subcapa inválida: {subcapa}")
    
    # Inicializar resultado
    resultado = {
        'metadata': {
            'actor': actor,
            'fase': str(fase),
            'subcapa': subcapa,
            'fecha_analisis': datetime.now().isoformat(),
            'version_modelo': '2.0'
        },
        'dimensiones_cognitivas': {},
        'dimension_operativa_material': {},
        'contexto_territorial': {},
        'memoria_temporal': {},
        'estado_gate': 'enabled',
        'justificacion_gate': '',
        'barreras': [],
        'activos': [],
        'recomendaciones': [],
        'costo_transicion': {},
        'nivel_confianza': 0,
        'datos_faltantes': []
    }
    
    # 1. Extraer dimensiones cognitivas
    try:
        if datos.get('dimensiones') is not None:
            df_dim = datos['dimensiones']
            # Buscar valores para este actor y fase
            for dim in DIMENSIONES.keys():
                # Buscar en la tabla el valor correspondiente
                valor = extraer_valor_dimension(df_dim, actor, fase, dim)
                resultado['dimensiones_cognitivas'][dim] = {
                    'valor': valor if valor else 0,
                    'estado': clasificar_estado(valor) if valor else 'desconocido',
                    'tendencia': '→',
                    'proyeccion_3m': valor if valor else 0
                }
        else:
            resultado['datos_faltantes'].append('Dimensiones cognitivas')
    except Exception as e:
        resultado['datos_faltantes'].append(f'Dimensiones cognitivas: {str(e)}')
    
    # 2. Extraer datos operativa-material
    try:
        if datos.get('operativa') is not None:
            iom_valor = extraer_iom(datos['operativa'], actor, fase, subcapa)
            resultado['dimension_operativa_material'] = {
                'IOM': iom_valor if iom_valor else 0,
                'infraestructura': 'Por especificar',
                'capacidad_tecnica': 'Por especificar',
                'recursos_disponibles': {}
            }
        else:
            resultado['datos_faltantes'].append('Operativa-Material')
    except Exception as e:
        resultado['datos_faltantes'].append(f'Operativa-Material: {str(e)}')
    
    # 3. Extraer contexto territorial
    try:
        if datos.get('contexto') is not None:
            contexto = extraer_contexto(datos['contexto'])
            resultado['contexto_territorial'] = contexto
        else:
            resultado['datos_faltantes'].append('Contexto territorial')
    except Exception as e:
        resultado['datos_faltantes'].append(f'Contexto territorial: {str(e)}')
    
    # 4. Extraer memoria temporal
    try:
        if datos.get('memoria') is not None:
            memoria = extraer_memoria(datos['memoria'])
            resultado['memoria_temporal'] = memoria
        else:
            resultado['datos_faltantes'].append('Memoria temporal')
    except Exception as e:
        resultado['datos_faltantes'].append(f'Memoria temporal: {str(e)}')
    
    # 5. Determinar estado de GATE
    resultado['estado_gate'], resultado['justificacion_gate'] = determinar_gate(
        resultado['dimensiones_cognitivas'],
        resultado['dimension_operativa_material'],
        resultado['contexto_territorial']
    )
    
    # 6. Identificar barreras y activos
    resultado['barreras'] = identificar_barreras(resultado['dimensiones_cognitivas'])
    resultado['activos'] = identificar_activos(resultado['dimensiones_cognitivas'])
    
    # 7. Generar recomendaciones
    resultado['recomendaciones'] = generar_recomendaciones(
        actor, fase, subcapa,
        resultado['dimensiones_cognitivas'],
        resultado['estado_gate']
    )
    
    # 8. Calcular costo de transición
    resultado['costo_transicion'] = calcular_costo_transicion(
        actor, fase, subcapa, resultado['estado_gate']
    )
    
    # 9. Estimar confianza
    resultado['nivel_confianza'] = estimar_confianza(resultado)
    
    # 10. Generar diagnóstico
    resultado['diagnostico'] = generar_diagnostico(resultado)
    
    return resultado

def extraer_valor_dimension(df, actor, fase, dimension):
    """Extrae valor de una dimensión específica"""
    try:
        # Buscar en columnas que contengan el actor y la fase
        # Estructura esperada: Columna Actor, Fase X (columnas numéricas)
        if 'Actor' in df.columns and f'Fase_{fase}' in df.columns:
            valor = df[df['Actor'] == actor][f'Fase_{fase}'].values
            return float(valor[0]) if len(valor) > 0 else None
        return None
    except:
        return None

def extraer_iom(df, actor, fase, subcapa):
    """Extrae IOM operativa-material"""
    try:
        # Buscar valor IOM en tabla
        if 'IOM' in df.columns and 'Actor' in df.columns:
            valor = df[df['Actor'] == actor]['IOM'].values
            return float(valor[0]) if len(valor) > 0 else 0
        return 0
    except:
        return 0

def extraer_contexto(df):
    """Extrae datos de contexto territorial"""
    contexto = {}
    try:
        indicadores = ['pobreza_multidimensional', 'informalidad', 'educacion_promedio',
                      'acceso_internet', 'tasa_desempleo_juvenil', 'participacion_ciudadana']
        for indicador in indicadores:
            if indicador in df.columns:
                valor = df[indicador].values[0]
                contexto[indicador] = float(valor) if valor else 0
        return contexto
    except:
        return contexto

def extraer_memoria(df):
    """Extrae datos de memoria temporal"""
    memoria = {}
    try:
        memoria['fechas'] = df['Fecha'].tolist() if 'Fecha' in df.columns else []
        # Extraer últimos 12 meses
        for dim in ['IA', 'IAT', 'ICI', 'IVC', 'IME', 'IIN', 'IPRA', 'ICS']:
            if dim in df.columns:
                memoria[dim] = df[dim].tail(12).tolist()
        return memoria
    except:
        return memoria

def determinar_gate(dimensiones, iom, contexto):
    """Determina estado de GATE: blocked, conditional o enabled"""
    
    # Extraer valores
    ici = dimensiones.get('ICI', {}).get('valor', 100)
    iom_val = iom.get('IOM', 0)
    pobreza = contexto.get('pobreza_multidimensional', 0)
    
    # Lógica de BLOCKED
    if ici < GATE_THRESHOLDS['ICI_MINIMO']:
        return 'blocked', f"ICI={ici} < {GATE_THRESHOLDS['ICI_MINIMO']} (confianza crítica)"
    
    if iom_val < GATE_THRESHOLDS['IOM_MINIMO']:
        return 'blocked', f"IOM={iom_val} < {GATE_THRESHOLDS['IOM_MINIMO']} (capacidad material insuficiente)"
    
    # Verificar dimensiones críticas
    for dim, datos in dimensiones.items():
        if datos['valor'] < GATE_THRESHOLDS['DIMENSION_CRITICA']:
            return 'blocked', f"{dim}={datos['valor']} < 25 (dimensión crítica)"
    
    # Lógica de CONDITIONAL
    if pobreza > GATE_THRESHOLDS['POBREZA_ALTO_RIESGO']:
        return 'conditional', f"Pobreza={pobreza}% > 50% (requiere condiciones especiales)"
    
    # Lógica de ENABLED
    return 'enabled', "Todas las condiciones cumplidas. Proceder sin condiciones."

def identificar_barreras(dimensiones):
    """Identifica barreras principales basado en dimensiones bajas"""
    barreras = []
    umbrales = {
        'IA': 40,
        'IAT': 40,
        'ICI': 40,
        'IVC': 50,
        'IME': 40,
        'IIN': 40,
        'IPRA': 40,
        'ICS': 40
    }
    
    for dim, umbral in umbrales.items():
        valor = dimensiones.get(dim, {}).get('valor', 100)
        if valor < umbral:
            severidad = 'crítica' if valor < 25 else ('moderada' if valor < 40 else 'leve')
            barreras.append({
                'nombre': f"{dim} - {DIMENSIONES.get(dim, dim)}",
                'dimensión': dim,
                'valor': valor,
                'severidad': severidad
            })
    
    return sorted(barreras, key=lambda x: x['valor'])

def identificar_activos(dimensiones):
    """Identifica activos (dimensiones altas)"""
    activos = []
    umbrales = {
        'IA': 60,
        'IAT': 60,
        'ICI': 60,
        'IVC': 70,
        'IME': 60,
        'IIN': 60,
        'IPRA': 60,
        'ICS': 60
    }
    
    for dim, umbral in umbrales.items():
        valor = dimensiones.get(dim, {}).get('valor', 0)
        if valor >= umbral:
            activos.append({
                'nombre': f"{dim} - {DIMENSIONES.get(dim, dim)}",
                'dimensión': dim,
                'valor': valor,
                'potencial': 'altísimo' if valor >= 80 else 'alto'
            })
    
    return sorted(activos, key=lambda x: x['valor'], reverse=True)

def generar_recomendaciones(actor, fase, subcapa, dimensiones, gate_state):
    """Genera recomendaciones priorizado"""
    recomendaciones = []
    
    # Si está bloqueado, la recomendación más crítica es desbloquear
    if gate_state == 'blocked':
        recomendaciones.append({
            'orden': 1,
            'prioridad': 'CRÍTICA',
            'accion': f'Resolver bloqueos antes de proceder a Fase {fase} Subcapa {subcapa}',
            'plazo': 'Inmediato'
        })
    
    # Barreras principales
    for dim in ['ICI', 'IAT', 'IME']:
        valor = dimensiones.get(dim, {}).get('valor', 100)
        if valor < 40:
            recomendaciones.append({
                'orden': len(recomendaciones) + 1,
                'prioridad': 'ALTA' if valor < 25 else 'MEDIA',
                'accion': f'Invertir en {DIMENSIONES.get(dim, dim)}',
                'plazo': '2-6 meses'
            })
    
    return recomendaciones

def calcular_costo_transicion(actor, fase, subcapa, gate_state):
    """Calcula costo estimado de transición"""
    
    # Costos base por actor
    costos_actor = {
        'Comunidad Local': 30000,
        'Gobierno Local': 15000,
        'Proveedores Técnicos': 20000,
        'Actores Económicos': 12000,
        'Actores Externos': 10000
    }
    
    costo_base = costos_actor.get(actor, 15000)
    
    # Multiplicador por estado de gate
    multiplicadores = {
        'blocked': 2.5,  # Requiere muchas acciones previas
        'conditional': 1.5,
        'enabled': 1.0
    }
    
    multiplicador = multiplicadores.get(gate_state, 1.0)
    costo_total = costo_base * multiplicador
    
    return {
        'costo_directo': f"${costo_total:,.0f}",
        'contingencia_25pct': f"${costo_total * 0.25:,.0f}",
        'total_presupuesto': f"${costo_total * 1.25:,.0f}",
        'tiempo': '3-9 meses' if gate_state == 'blocked' else '2-3 meses',
        'estado_gate': gate_state
    }

def estimar_confianza(resultado):
    """Estima nivel de confianza en el análisis (0-100)"""
    confianza = 70  # Base
    
    # Reducir confianza por datos faltantes
    confianza -= len(resultado['datos_faltantes']) * 10
    
    # Aumentar si hay buena cobertura de dimensiones
    dims_disponibles = len([d for d in resultado['dimensiones_cognitivas'] if d['valor'] > 0])
    confianza += (dims_disponibles / 8) * 20
    
    return max(0, min(100, confianza))

def generar_diagnostico(resultado):
    """Genera diagnóstico narrativo"""
    dims = resultado['dimensiones_cognitivas']
    ici = dims.get('ICI', {}).get('valor', 0)
    ivc = dims.get('IVC', {}).get('valor', 0)
    ia = dims.get('IA', {}).get('valor', 0)
    
    diagnostico = f"""
El {resultado['metadata']['actor']} en Fase {resultado['metadata']['fase']} Subcapa {resultado['metadata']['subcapa']}
presenta: Confianza institucional {ici}/100 ({'CRÍTICA' if ici < 40 else 'MODERADA' if ici < 60 else 'FUERTE'}),
Identidad cultural {ivc}/100, Aspiraciones {ia}/100. 
Estado de gate: {GATE_STATES.get(resultado['estado_gate'], resultado['estado_gate'])}.
{resultado['justificacion_gate']}
"""
    return diagnostico.strip()

def clasificar_estado(valor):
    """Clasifica estado de un indicador"""
    if valor is None:
        return 'desconocido'
    if valor < 25:
        return 'crítico'
    elif valor < 40:
        return 'bajo'
    elif valor < 60:
        return 'moderado'
    elif valor < 80:
        return 'fuerte'
    else:
        return 'muy_fuerte'

def exportar_json(resultado):
    """Exporta resultado a JSON formateado"""
    return json.dumps(resultado, indent=2, ensure_ascii=False, default=str)
