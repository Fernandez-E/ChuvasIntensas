#from functions.separacao import separador_variaveis
from functions.funcoes import verifica_registro

from datetime import datetime, timedelta

linhas, datas, horarios, precipitacao, eventos = [], [], [], [], []

with open('serra9900.3.txt', 'r') as arquivo:
    for linha in arquivo:
        linhas.append(linha.strip().replace('""', ' ').replace('"', ''))

    for item in linhas:
        datas.append(item[0:10])
        horarios.append(item[11:19])
        precipitacao.append(float(item[-6:]))

    i=0
    for i in range(len(datas)):
        eventos.append((datetime.strptime(f'{datas[i]} {horarios[i]}', "%m/%d/%Y %H:%M:%S"), precipitacao[i]))
        i+=1

print(eventos)
#EVENTOS[Evento][?]
# ? = 0=DATA E HORA DE INICIO
# ? = 1=PRECIPITACAO ACUMULADA


# LOOP DE IDENTIFICAÇÃO DE CHUVAS INTENSAS COM DURAÇÃO DE 6H E SUPERIORES A 10MM
chuvas_intensas = []
c_intensas = 1
data_inicio = eventos[0][0]

for i in range(1, len(eventos)):
    diff_tempo = eventos[i][0] - data_inicio

    if diff_tempo <= timedelta(hours=6):
        c_intensas += 1
    else:
        if c_intensas >= 40:
            chuvas_intensas.append((data_inicio, eventos[i - 1][0], c_intensas))
            print(f'{data_inicio} a {eventos[i - 1][0]}: Evento erosivo: {c_intensas} basculas ({c_intensas * 0.25}mm)')

        c_intensas = 1
        data_inicio = eventos[i][0]

if c_intensas >= 40:
    chuvas_intensas.append((data_inicio, eventos[-1][0], c_intensas))
    print(f'{data_inicio} a {eventos[-1][0]}: Evento erosivo: {c_intensas} basculas ({c_intensas * 0.25}mm)')

print("-------------------------------- FIM DO PRIMEIRO LOOP --------------------------------")
print(f'Contagem de chuvas intensas de ate 6h: {len(chuvas_intensas)}')
for chuva in chuvas_intensas:
    print(chuva)
print("--------------------------------------------------------------------------------------")

# if c_intensas >= 40:
#     print(f'{data_inicio} a {eventos[-1][0]}: Evento erosivo: {c_intensas} basculas')
# else:
#     print(f'{data_inicio}: {c_intensas} basculas')
# print(f'Total de chuvas erosivas: {len(chuvas_intensas)}')
# FIM LOOP DE IDENTIFICAÇÃO DE CHUVAS INTENSAS COM DURAÇÃO DE 6H E SUPERIORES A 10MM



# LOOP DE IDENTIFICAÇÃO DE CHUVAS INTENSAS COM DURAÇÃO DE 15MIN E SUPERIORES A 9MM
c_intensas = 1
data_inicio = eventos[0][0]
registro_6h = True
i = 0
for i in range(0, len(eventos)):
    diff_tempo = eventos[i][0] - data_inicio

    #VERIFICA A EXISTENCIA DE REGISTRO QUE CONTENHA A DATA ATUAL
    #RETORNA TRUE SE JA EXISTIR REGISTRO E FALSE SE NAO EXISTIR
    #SE RETORNAR FALSE, CONTINUA A CONTAGEM DE BASCULAS
    registro_6h = verifica_registro(data_inicio, chuvas_intensas)

    if diff_tempo <= timedelta(minutes=15) and not registro_6h:
        c_intensas+=1

    else:
        if c_intensas >= 36 and c_intensas < 40:
            chuvas_intensas.append((data_inicio, eventos[i - 1][0], c_intensas))
            print(f'{data_inicio} a {eventos[i - 1][0]}: Evento erosivo: {c_intensas} basculas ({c_intensas*0.25}mm)')
        else:
            print(f'{data_inicio}: {c_intensas} basculas [{registro_6h}]')

        c_intensas = 1  # Reinicia a contagem
        data_inicio = eventos[i][0]  # Define o novo ponto de início

print("-------------------------------- FIM DO SEGUNDO LOOP --------------------------------")
print(f'Contagem de chuvas intensas de ate 6h e de até 15min: {len(chuvas_intensas)}')
for chuva in chuvas_intensas:
    print(chuva)
print("--------------------------------------------------------------------------------------")

#     diff_tempo = eventos[i][0] - data_inicio
#     if diff_tempo <= timedelta(minutes=15):
#
#
#     else:
#         if c_intensas >= 40:
#             chuvas_intensas.append((data_inicio, eventos[i - 1][0], c_intensas))
#             print(
#                 f'{data_inicio} a {eventos[i - 1][0]}: Evento erosivo: {c_intensas} basculas ({c_intensas * 0.25}mm)')
#         else:
#             print(f'{data_inicio}: {c_intensas} basculas')
#
#         c_intensas = 1  # Reinicia a contagem
#         data_inicio = eventos[i][0]  # Define o novo ponto de início
#
# if c_intensas >= 40:
#     print(f'{data_inicio} a {eventos[-1][0]}: Evento erosivo: {c_intensas} basculas')
# else:
#     print(f'{data_inicio}: {c_intensas} basculas')




    # if diff_tempo <= timedelta(minutes=15):
    #     c_intensas+=1
    #     if c_intensas >= 36:
    #         chuvas_intensas.append((data_inicio, eventos[i - 1][0], c_intensas))
    #         print(f'{data_inicio} a {eventos[i - 1][0]}: Evento erosivo: {c_intensas} basculas ({c_intensas * 0.25}mm)')
    #         c_intensas = 1  # Reinicia a contagem
    #         data_inicio = eventos[i][0]
    #         continue
    #
    # elif diff_tempo > timedelta(minutes=15) and diff_tempo <= timedelta(hours=6):
    #     c_intensas+=1
    #
    # else:
    #     if c_intensas >= 40:
    #         chuvas_intensas.append((data_inicio, eventos[i - 1][0], c_intensas))
    #         print(f'{data_inicio} a {eventos[i - 1][0]}: Evento erosivo: {c_intensas} basculas ({c_intensas*0.25}mm)')
    #     else:
    #         print(f'{data_inicio}: {c_intensas} basculas')
    #
    #     c_intensas = 1  # Reinicia a contagem
    #     data_inicio = eventos[i][0]  # Define o novo ponto de início

# if c_intensas >= 40:
#     print(f'{data_inicio} a {eventos[-1][0]}: Evento erosivo: {c_intensas} basculas')
# else:
#     print(f'{data_inicio}: {c_intensas} basculas')
#
# print(f' CHUVAS INTENSAS: {chuvas_intensas}')


#CHUVAS_INTENSAS: 0 = INICIO DA CHUVA EROSIVA
# 1 = FINAL DO EVENTO
# 2 = CONTAGEM DE BÁSCULAS

chuveros = open('serra9900-chuveros.txt', 'w')

i=0
c=0
for chuva in chuvas_intensas:
    chuveros.write(f'{chuva[0].day:02}/{chuva[0].month:02}/{chuva[0].year%100:02}\n')
    chuveros.write(f'{i+1} {chuva[2]} {chuva[0].hour:02} {chuva[0].minute:02} 0.0\n')
    for evento in eventos:
        if evento[0] >= chuva[0] and evento[0] <= chuva[1]:
            c+=1
            chuveros.write(f'{evento[0].hour:02} {evento[0].minute:02} 0.25\n')
    i+=1
chuveros.close()