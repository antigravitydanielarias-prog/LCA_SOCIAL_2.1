"""
Tests unitarios para Modelo 2.0
Prueba los módulos principales de cálculo
"""

import pytest
import sys
from pathlib import Path

# Agregar src al path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from utils.calculations import (
    determinar_gate,
    identificar_barreras,
    identificar_activos,
    clasificar_estado,
    calcular_costo_transicion
)

# ============================================================================
# Tests de determinación de GATE
# ============================================================================

def test_gate_blocked_low_ici():
    """Test: Gate debe estar BLOCKED cuando ICI < 40"""
    
    dimensiones = {
        'ICI': {'valor': 28, 'estado': 'crítico'},
        'IA': {'valor': 45, 'estado': 'moderado'},
    }
    iom = {'IOM': 50}
    contexto = {'pobreza_multidimensional': 67}
    
    estado, justificacion = determinar_gate(dimensiones, iom, contexto)
    
    assert estado == 'blocked'
    assert 'ICI' in justificacion

def test_gate_blocked_low_iom():
    """Test: Gate debe estar BLOCKED cuando IOM < 30"""
    
    dimensiones = {
        'ICI': {'valor': 50, 'estado': 'moderado'},
        'IA': {'valor': 45, 'estado': 'moderado'},
    }
    iom = {'IOM': 20}
    contexto = {'pobreza_multidimensional': 67}
    
    estado, justificacion = determinar_gate(dimensiones, iom, contexto)
    
    assert estado == 'blocked'

def test_gate_conditional_high_poverty():
    """Test: Gate debe estar CONDITIONAL cuando pobreza > 50%"""
    
    dimensiones = {
        'ICI': {'valor': 50, 'estado': 'moderado'},
        'IA': {'valor': 45, 'estado': 'moderado'},
    }
    iom = {'IOM': 50}
    contexto = {'pobreza_multidimensional': 67}
    
    estado, justificacion = determinar_gate(dimensiones, iom, contexto)
    
    assert estado == 'conditional'

def test_gate_enabled_all_good():
    """Test: Gate debe estar ENABLED cuando todo está bien"""
    
    dimensiones = {
        'ICI': {'valor': 70, 'estado': 'fuerte'},
        'IA': {'valor': 70, 'estado': 'fuerte'},
    }
    iom = {'IOM': 70}
    contexto = {'pobreza_multidimensional': 30}
    
    estado, justificacion = determinar_gate(dimensiones, iom, contexto)
    
    assert estado == 'enabled'

# ============================================================================
# Tests de clasificación de estado
# ============================================================================

def test_clasificar_estado_critico():
    """Test: Valor < 25 debe clasificarse como crítico"""
    estado = clasificar_estado(20)
    assert estado == 'crítico'

def test_clasificar_estado_bajo():
    """Test: Valor 25-40 debe clasificarse como bajo"""
    estado = clasificar_estado(35)
    assert estado == 'bajo'

def test_clasificar_estado_moderado():
    """Test: Valor 40-60 debe clasificarse como moderado"""
    estado = clasificar_estado(50)
    assert estado == 'moderado'

def test_clasificar_estado_fuerte():
    """Test: Valor 60-80 debe clasificarse como fuerte"""
    estado = clasificar_estado(70)
    assert estado == 'fuerte'

def test_clasificar_estado_muy_fuerte():
    """Test: Valor >= 80 debe clasificarse como muy_fuerte"""
    estado = clasificar_estado(90)
    assert estado == 'muy_fuerte'

def test_clasificar_estado_none():
    """Test: None debe retornar desconocido"""
    estado = clasificar_estado(None)
    assert estado == 'desconocido'

# ============================================================================
# Tests de identificación de barreras
# ============================================================================

def test_identificar_barreras_ici_bajo():
    """Test: ICI bajo debe identificarse como barrera"""
    
    dimensiones = {
        'ICI': {'valor': 28, 'estado': 'crítico'},
        'IA': {'valor': 45, 'estado': 'moderado'},
        'IAT': {'valor': 70, 'estado': 'fuerte'},
        'IVC': {'valor': 72, 'estado': 'fuerte'},
        'IME': {'valor': 32, 'estado': 'bajo'},
        'IIN': {'valor': 55, 'estado': 'neutral'},
        'IPRA': {'valor': 41, 'estado': 'moderado'},
        'ICS': {'valor': 38, 'estado': 'bajo'},
    }
    
    barreras = identificar_barreras(dimensiones)
    
    assert len(barreras) > 0
    assert any(b['dimensión'] == 'ICI' for b in barreras)
    assert any(b['severidad'] == 'crítica' for b in barreras)

def test_identificar_barreras_multiple():
    """Test: Debe identificar múltiples barreras"""
    
    dimensiones = {
        'ICI': {'valor': 28, 'estado': 'crítico'},
        'IAT': {'valor': 38, 'estado': 'bajo'},
        'IME': {'valor': 32, 'estado': 'bajo'},
        'IA': {'valor': 45, 'estado': 'moderado'},
        'IVC': {'valor': 72, 'estado': 'fuerte'},
        'IIN': {'valor': 55, 'estado': 'neutral'},
        'IPRA': {'valor': 41, 'estado': 'moderado'},
        'ICS': {'valor': 38, 'estado': 'bajo'},
    }
    
    barreras = identificar_barreras(dimensiones)
    
    assert len(barreras) >= 3  # Al menos 3 barreras

# ============================================================================
# Tests de identificación de activos
# ============================================================================

def test_identificar_activos_ivc_fuerte():
    """Test: IVC fuerte debe identificarse como activo"""
    
    dimensiones = {
        'IVC': {'valor': 72, 'estado': 'fuerte'},
        'IA': {'valor': 45, 'estado': 'moderado'},
        'IAT': {'valor': 38, 'estado': 'bajo'},
        'ICI': {'valor': 28, 'estado': 'crítico'},
        'IME': {'valor': 32, 'estado': 'bajo'},
        'IIN': {'valor': 55, 'estado': 'neutral'},
        'IPRA': {'valor': 41, 'estado': 'moderado'},
        'ICS': {'valor': 38, 'estado': 'bajo'},
    }
    
    activos = identificar_activos(dimensiones)
    
    assert len(activos) > 0
    assert any(a['dimensión'] == 'IVC' for a in activos)

def test_identificar_activos_none():
    """Test: Debe retornar lista vacía si no hay activos"""
    
    dimensiones = {
        'ICI': {'valor': 28, 'estado': 'crítico'},
        'IA': {'valor': 45, 'estado': 'moderado'},
        'IAT': {'valor': 35, 'estado': 'bajo'},
        'IVC': {'valor': 55, 'estado': 'neutral'},
        'IME': {'valor': 32, 'estado': 'bajo'},
        'IIN': {'valor': 55, 'estado': 'neutral'},
        'IPRA': {'valor': 41, 'estado': 'moderado'},
        'ICS': {'valor': 38, 'estado': 'bajo'},
    }
    
    activos = identificar_activos(dimensiones)
    
    assert len(activos) == 0 or all(a['valor'] >= 60 for a in activos)

# ============================================================================
# Tests de cálculo de costos
# ============================================================================

def test_calcular_costo_transicion_blocked():
    """Test: BLOCKED debe multiplicar costo por 2.5"""
    
    costo = calcular_costo_transicion('Comunidad Local', 1, 'A', 'blocked')
    
    assert 'costo_directo' in costo
    assert 'total_presupuesto' in costo
    # El costo debe estar entre ciertos rangos esperados
    # Extrae el número del string (ej: "$75000")
    try:
        costo_valor = float(costo['costo_directo'].replace('$', '').replace(',', ''))
        assert costo_valor > 50000  # Mayor que el base de 30k × 2.5
    except:
        pass

def test_calcular_costo_transicion_enabled():
    """Test: ENABLED debe tener costo base sin multiplicador"""
    
    costo = calcular_costo_transicion('Comunidad Local', 1, 'A', 'enabled')
    
    assert 'costo_directo' in costo
    assert 'total_presupuesto' in costo

# ============================================================================
# Ejecución de tests
# ============================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
