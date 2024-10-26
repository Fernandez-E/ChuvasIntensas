from datetime import datetime, timedelta

def verifica_registro(inicio, chuvas_registradas):
    for chuva in chuvas_registradas:
        if chuva[0] <= inicio <= chuva[1]:
            return True  # Retorna True assim que encontra uma correspondência
    return False  # Se nenhum intervalo contiver 'inicio', retorna False
